'use client';

import { motion } from 'framer-motion';
import LandingPage from '../landing/LandingPage';

const HomePage = ({ onGetStarted }) => {
    return <LandingPage onGetStarted={onGetStarted} />;
};

export default HomePage;
