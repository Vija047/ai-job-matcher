#!/usr/bin/env node

/**
 * Pre-deployment verification script
 * Checks if the project is ready for Vercel deployment
 */

const fs = require('fs');
const path = require('path');

console.log('🔍 Pre-deployment verification...\n');

let checks = 0;
let passed = 0;

function check(name, condition, message) {
    checks++;
    if (condition) {
        console.log(`✅ ${name}: ${message}`);
        passed++;
    } else {
        console.log(`❌ ${name}: ${message}`);
    }
}

// Check required files
check(
    'Package.json',
    fs.existsSync('package.json'),
    fs.existsSync('package.json') ? 'Found' : 'Missing package.json'
);

check(
    'Vercel config',
    fs.existsSync('vercel.json'),
    fs.existsSync('vercel.json') ? 'Found' : 'Missing vercel.json'
);

check(
    'API handler',
    fs.existsSync('api/app.py'),
    fs.existsSync('api/app.py') ? 'Found' : 'Missing api/app.py'
);

check(
    'Requirements',
    fs.existsSync('requirements.txt'),
    fs.existsSync('requirements.txt') ? 'Found' : 'Missing requirements.txt'
);

check(
    'Next.js config',
    fs.existsSync('next.config.mjs'),
    fs.existsSync('next.config.mjs') ? 'Found' : 'Missing next.config.mjs'
);

// Check package.json scripts
if (fs.existsSync('package.json')) {
    const pkg = JSON.parse(fs.readFileSync('package.json', 'utf8'));

    check(
        'Build script',
        pkg.scripts && pkg.scripts.build,
        pkg.scripts && pkg.scripts.build ? 'Found build script' : 'Missing build script'
    );

    check(
        'Start script',
        pkg.scripts && pkg.scripts.start,
        pkg.scripts && pkg.scripts.start ? 'Found start script' : 'Missing start script'
    );
}

// Check API structure
const apiDir = 'api';
if (fs.existsSync(apiDir)) {
    const apiFiles = fs.readdirSync(apiDir);
    check(
        'API files',
        apiFiles.length > 0,
        `Found ${apiFiles.length} API file(s)`
    );
}

// Check source structure
const srcDir = 'src';
check(
    'Source directory',
    fs.existsSync(srcDir),
    fs.existsSync(srcDir) ? 'Source directory exists' : 'Missing src directory'
);

console.log(`\n📊 Verification complete: ${passed}/${checks} checks passed\n`);

if (passed === checks) {
    console.log('🎉 Project is ready for Vercel deployment!');
    console.log('\n📋 Next steps:');
    console.log('1. Run: vercel --prod');
    console.log('2. Configure environment variables in Vercel dashboard');
    console.log('3. Test your deployed application');
} else {
    console.log('⚠️  Please fix the issues above before deploying');
    process.exit(1);
}
