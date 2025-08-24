import { NextResponse } from 'next/server';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';

// Mock database - in production, use a real database
const users = new Map();

// Initialize with demo users
const initDemoUsers = async () => {
    if (users.size === 0) {
        const demoPassword = await bcrypt.hash('password123', 10);

        users.set('demo@example.com', {
            id: '1',
            firstName: 'Demo',
            lastName: 'User',
            email: 'demo@example.com',
            phone: '+1234567890',
            company: 'Demo Company',
            password: demoPassword,
            createdAt: new Date().toISOString()
        });

        users.set('john@example.com', {
            id: '2',
            firstName: 'John',
            lastName: 'Doe',
            email: 'john@example.com',
            phone: '+1987654321',
            company: 'Tech Corp',
            password: demoPassword,
            createdAt: new Date().toISOString()
        });
    }
};

export async function POST(request) {
    try {
        // Initialize demo users
        await initDemoUsers();

        const { email, password } = await request.json();

        // Validate input
        if (!email || !password) {
            return NextResponse.json(
                { message: 'Email and password are required' },
                { status: 400 }
            );
        }

        // Check if user exists
        const user = users.get(email);
        if (!user) {
            return NextResponse.json(
                { message: 'Invalid email or password' },
                { status: 401 }
            );
        }

        // Verify password
        const isPasswordValid = await bcrypt.compare(password, user.password);
        if (!isPasswordValid) {
            return NextResponse.json(
                { message: 'Invalid email or password' },
                { status: 401 }
            );
        }

        // Generate JWT token
        const token = jwt.sign(
            { userId: user.id, email: user.email },
            process.env.JWT_SECRET || 'your-secret-key',
            { expiresIn: '7d' }
        );

        // Return user data (without password) and token
        const { password: _, ...userWithoutPassword } = user;

        return NextResponse.json({
            user: userWithoutPassword,
            token
        });

    } catch (error) {
        console.error('Login error:', error);
        return NextResponse.json(
            { message: 'Internal server error' },
            { status: 500 }
        );
    }
}
