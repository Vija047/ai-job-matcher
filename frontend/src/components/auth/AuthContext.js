'use client';

import { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';
import toast from 'react-hot-toast';

const AuthContext = createContext();

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};

// Create axios instance for auth API calls
const authApi = axios.create({
    baseURL: typeof window !== 'undefined' ? window.location.origin : 'http://localhost:3000',
    headers: {
        'Content-Type': 'application/json',
    },
});

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    // Initialize auth state
    useEffect(() => {
        const token = localStorage.getItem('authToken');
        const userData = localStorage.getItem('userData');

        if (token && userData) {
            try {
                setUser(JSON.parse(userData));
                setIsAuthenticated(true);
                // Set default axios header
                authApi.defaults.headers.common['Authorization'] = `Bearer ${token}`;
            } catch (error) {
                console.error('Error parsing stored user data:', error);
                localStorage.removeItem('authToken');
                localStorage.removeItem('userData');
            }
        }
        setLoading(false);
    }, []);

    const login = async (email, password) => {
        try {
            setLoading(true);
            const response = await authApi.post('/api/auth/login', {
                email,
                password
            });

            const { user: userData, token } = response.data;

            // Store auth data
            localStorage.setItem('authToken', token);
            localStorage.setItem('userData', JSON.stringify(userData));

            // Set default axios header
            authApi.defaults.headers.common['Authorization'] = `Bearer ${token}`;

            setUser(userData);
            setIsAuthenticated(true);

            toast.success('Login successful!');
            return { success: true };
        } catch (error) {
            const message = error.response?.data?.message || 'Login failed';
            toast.error(message);
            return { success: false, error: message };
        } finally {
            setLoading(false);
        }
    };

    const signup = async (userData) => {
        try {
            setLoading(true);
            const response = await authApi.post('/api/auth/signup', userData);

            const { user: newUser, token } = response.data;

            // Store auth data
            localStorage.setItem('authToken', token);
            localStorage.setItem('userData', JSON.stringify(newUser));

            // Set default axios header
            authApi.defaults.headers.common['Authorization'] = `Bearer ${token}`;

            setUser(newUser);
            setIsAuthenticated(true);

            toast.success('Account created successfully!');
            return { success: true };
        } catch (error) {
            const message = error.response?.data?.message || 'Signup failed';
            toast.error(message);
            return { success: false, error: message };
        } finally {
            setLoading(false);
        }
    };

    const logout = () => {
        localStorage.removeItem('authToken');
        localStorage.removeItem('userData');
        delete authApi.defaults.headers.common['Authorization'];

        setUser(null);
        setIsAuthenticated(false);

        toast.success('Logged out successfully');
    };

    const forgotPassword = async (email) => {
        try {
            setLoading(true);
            await authApi.post('/api/auth/forgot-password', { email });
            toast.success('Password reset email sent!');
            return { success: true };
        } catch (error) {
            const message = error.response?.data?.message || 'Failed to send reset email';
            toast.error(message);
            return { success: false, error: message };
        } finally {
            setLoading(false);
        }
    };

    const resetPassword = async (token, newPassword) => {
        try {
            setLoading(true);
            await authApi.post('/api/auth/reset-password', {
                token,
                newPassword
            });
            toast.success('Password reset successful!');
            return { success: true };
        } catch (error) {
            const message = error.response?.data?.message || 'Password reset failed';
            toast.error(message);
            return { success: false, error: message };
        } finally {
            setLoading(false);
        }
    };

    const value = {
        user,
        isAuthenticated,
        loading,
        login,
        signup,
        logout,
        forgotPassword,
        resetPassword
    };

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
};
