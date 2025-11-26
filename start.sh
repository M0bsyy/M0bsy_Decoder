#!/bin/bash

echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║   PYTHON DEOBFUSCATOR TELEGRAM BOT - STARTER                    ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""

# Check if Python installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found!"
    exit 1
fi

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
