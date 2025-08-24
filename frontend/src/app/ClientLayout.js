'use client';

import { AuthProvider } from '../components/auth/AuthContext';
import { NavigationProvider } from '../components/navigation/NavigationContext';

export default function ClientLayout({ children }) {
    return (
        <AuthProvider>
            <NavigationProvider>
                {children}
            </NavigationProvider>
        </AuthProvider>
    );
}
