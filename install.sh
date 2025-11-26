#!/bin/bash

echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║   PYTHON DEOBFUSCATOR TELEGRAM BOT - INSTALLER                  ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found!"
    echo "Install Python first: apt install python3 (Debian/Ubuntu) or pkg install python3 (Termux)"
    exit 1
fi

echo "✓ Python $(python3 --version 2>&1 | cut -d' ' -f2) detected"
echo ""

# Check if pip is installed
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "❌ pip not found!"
    echo "Install pip first: apt install python3-pip (Debian/Ubuntu) or pip install --upgrade pip (Termux)"
    exit 1
fi

echo "✓ pip detected"
echo ""

# Install requirements
echo "📦 Installing dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Dependencies installed successfully!"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🚀 NEXT STEPS:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "1️⃣  Setup bot token:"
    echo "   python3 setup_bot.py"
    echo ""
    echo "2️⃣  Run the bot:"
    echo "   python3 telegram_bot.py"
    echo ""
    echo "OR use the start script:"
    echo "   ./start.sh"
    echo ""
else
    echo "❌ Failed to install dependencies"
    exit 1
fi
