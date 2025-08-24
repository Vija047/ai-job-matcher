import { NextResponse } from 'next/server';

// Mock database - in production, use a real database
const users = new Map();
const resetTokens = new Map();

export async function POST(request) {
    try {
        const { email } = await request.json();

        // Validate input
        if (!email) {
            return NextResponse.json(
                { message: 'Email is required' },
                { status: 400 }
            );
        }

        // Validate email format
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            return NextResponse.json(
                { message: 'Invalid email format' },
                { status: 400 }
            );
        }

        // Check if user exists
        const user = users.get(email);
        if (!user) {
            // For security, we return success even if user doesn't exist
            // This prevents email enumeration attacks
            return NextResponse.json({
                message: 'If an account with that email exists, we have sent a password reset link'
            });
        }

        // Generate reset token
        const resetToken = Math.random().toString(36).substring(2, 15) +
            Math.random().toString(36).substring(2, 15);

        // Store reset token with expiration (1 hour)
        resetTokens.set(resetToken, {
            email: user.email,
            expiresAt: new Date(Date.now() + 3600000) // 1 hour from now
        });

        // In production, send actual email here
        // For demo purposes, we'll just log the reset link
        console.log(`Password reset link for ${email}: /auth/reset-password?token=${resetToken}`);

        return NextResponse.json({
            message: 'Password reset email sent successfully',
            // In production, remove this resetToken from response
            resetToken: resetToken // Only for demo purposes
        });

    } catch (error) {
        console.error('Forgot password error:', error);
        return NextResponse.json(
            { message: 'Internal server error' },
            { status: 500 }
        );
    }
}
