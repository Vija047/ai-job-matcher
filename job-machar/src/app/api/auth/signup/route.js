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

        const { firstName, lastName, email, phone, company, password } = await request.json();

        // Validate input
        if (!firstName || !lastName || !email || !password) {
            return NextResponse.json(
                { message: 'First name, last name, email, and password are required' },
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

        // Validate password length
        if (password.length < 6) {
            return NextResponse.json(
                { message: 'Password must be at least 6 characters long' },
                { status: 400 }
            );
        }

        // Check if user already exists
        if (users.has(email)) {
            return NextResponse.json(
                { message: 'User already exists with this email' },
                { status: 409 }
            );
        }

        // Hash password
        const hashedPassword = await bcrypt.hash(password, 10);

        // Create user
        const user = {
            id: Date.now().toString(),
            firstName,
            lastName,
            email,
            phone: phone || null,
            company: company || null,
            password: hashedPassword,
            createdAt: new Date().toISOString()
        };

        // Store user in mock database
        users.set(email, user);

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
        }, { status: 201 });

    } catch (error) {
        console.error('Signup error:', error);
        return NextResponse.json(
            { message: 'Internal server error' },
            { status: 500 }
        );
    }
}
