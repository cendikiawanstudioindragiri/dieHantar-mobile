#!/bin/bash
# Setup script for dieHantar-mobile primary codespace

echo "🚀 Setting up dieHantar-mobile primary codespace..."

# Install Python dependencies for backend
echo "📦 Installing Python dependencies..."
cd /workspaces/dieHantar-mobile
python -m pip install --upgrade pip
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt

# Install Node.js dependencies for frontend
if [ -d "frontend" ] && [ -f "frontend/package.json" ]; then
    echo "📦 Installing Node.js dependencies..."
    cd frontend
    npm install
    cd ..
fi

# Install Flutter dependencies if present
if [ -d "flutter_app" ] && [ -f "flutter_app/pubspec.yaml" ]; then
    echo "📱 Setting up Flutter app..."
    cd flutter_app
    flutter pub get
    cd ..
fi

# Set up Git configuration
echo "🔧 Configuring Git..."
git config --global user.name "dieHantar Developer"
git config --global user.email "developer@diehantar.com"
git config --global init.defaultBranch main

# Create environment files from examples
echo "⚙️ Setting up environment files..."
if [ -f ".env.example" ]; then
    cp .env.example .env
fi
if [ -f "backend/.env.example" ]; then
    cp backend/.env.example backend/.env
fi

# Make scripts executable
echo "🔒 Setting script permissions..."
find . -name "*.sh" -type f -exec chmod +x {} \;

echo "✅ dieHantar-mobile primary codespace setup complete!"
echo "🎯 Ready for development!"