'use client';

import { createContext, useContext, useState } from 'react';

const NavigationContext = createContext();

export const useNavigation = () => {
    const context = useContext(NavigationContext);
    if (!context) {
        throw new Error('useNavigation must be used within a NavigationProvider');
    }
    return context;
};

export const NavigationProvider = ({ children }) => {
    const [currentPage, setCurrentPage] = useState('home');

    const navigateTo = (page) => {
        setCurrentPage(page);
    };

    return (
        <NavigationContext.Provider value={{
            currentPage,
            navigateTo
        }}>
            {children}
        </NavigationContext.Provider>
    );
};
