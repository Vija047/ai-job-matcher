import { NextResponse } from 'next/server';
import bcrypt from 'bcryptjs';

// Mock database - in production, use a real database
const users = new Map();
const resetTokens = new Map();

export async function POST(request) {
    try {
        const { token, newPassword } = await request.json();

        // Validate input
        if (!token || !newPassword) {
            return NextResponse.json(
                { message: 'Token and new password are required' },
                { status: 400 }
            );
        }

        // Validate password length
        if (newPassword.length < 6) {
            return NextResponse.json(
                { message: 'Password must be at least 6 characters long' },
                { status: 400 }
            );
        }

        // Check if reset token exists and is valid
        const resetData = resetTokens.get(token);
        if (!resetData) {
            return NextResponse.json(
                { message: 'Invalid or expired reset token' },
                { status: 400 }
            );
        }

        // Check if token has expired
        if (new Date() > resetData.expiresAt) {
            resetTokens.delete(token);
            return NextResponse.json(
                { message: 'Reset token has expired' },
                { status: 400 }
            );
        }

        // Get user
        const user = users.get(resetData.email);
        if (!user) {
            return NextResponse.json(
                { message: 'User not found' },
                { status: 404 }
            );
        }

        // Hash new password
        const hashedPassword = await bcrypt.hash(newPassword, 10);

        // Update user password
        user.password = hashedPassword;
        user.updatedAt = new Date().toISOString();
        users.set(resetData.email, user);

        // Remove used reset token
        resetTokens.delete(token);

        return NextResponse.json({
            message: 'Password reset successfully'
        });

    } catch (error) {
        console.error('Reset password error:', error);
        return NextResponse.json(
            { message: 'Internal server error' },
            { status: 500 }
        );
    }
}
