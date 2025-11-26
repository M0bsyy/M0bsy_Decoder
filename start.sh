#!/bin/bash

echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║   PYTHON DEOBFUSCATOR TELEGRAM BOT - STARTER                    ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""

# Check if Python installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found!"
    echo "Install with: pkg install python3 (Termux) or apt install python3 (Linux)"
    exit 1
fi

echo "✓ Python $(python3 --version 2>&1 | cut -d' ' -f2) detected"

# Check if pip installed
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "❌ pip not found!"
    echo "Install with: pkg install python3-pip (Termux) or apt install python3-pip (Linux)"
    exit 1
fi

# Check if python-telegram-bot is installed
echo "🔍 Checking dependencies..."
python3 -c "import telegram" 2>/dev/null

if [ $? -ne 0 ]; then
    echo "📦 Installing python-telegram-bot==20.7..."
    pip install python-telegram-bot==20.7
    
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install python-telegram-bot"
        echo "Try manually: pip install python-telegram-bot"
        exit 1
    fi
    echo "✓ Dependencies installed successfully!"
else
    echo "✓ All dependencies found"
fi

echo ""

# Check if token setup done
if [ ! -f .env ]; then
    echo "📝 First time setup detected..."
    echo ""
    echo "Run setup first:"
    echo "  python3 setup_bot.py"
    echo ""
    exit 1
fi

# Load token
set -a
source .env
set +a

# Check if token exists
if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo "❌ Token not configured!"
    echo "Run: python3 setup_bot.py"
    exit 1
fi

echo "✓ Token configured"
echo "✓ Starting bot..."
echo ""

# Run bot
python3 telegram_bot.py
