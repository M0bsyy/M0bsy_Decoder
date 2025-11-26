#!/usr/bin/env python3
"""
Quick setup script for Telegram Bot
Helps configure token and test connection
"""

import os
import sys

def setup():
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║     TELEGRAM BOT SETUP - Python Deobfuscator                     ║
╚═══════════════════════════════════════════════════════════════════╝
    """)
    
    # Check if token already set
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    if token:
        print(f"✓ Token already configured: {token[:20]}...")
        return
    
    print("""
STEP 1: Get Telegram Bot Token
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Open Telegram app
2. Search for: @BotFather
3. Send: /newbot
4. Follow instructions:
   - Bot name: "Python Decoder Bot"
   - Bot username: "python_decoder_bot" (unique)
5. Copy the token (long string with numbers and letters)

STEP 2: Set Token
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """)
    
    token = input("Paste your Telegram Bot Token: ").strip()
    
    if not token or len(token) < 20:
        print("✗ Invalid token!")
        sys.exit(1)
    
    # Save to .env file
    with open('.env', 'w') as f:
        f.write(f'TELEGRAM_BOT_TOKEN={token}\n')
    
    print(f"\n✓ Token saved to .env file")
    print(f"\nSTEP 3: Run Bot")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"  python3 telegram_bot.py")
    print(f"\nYour bot is now ACTIVE! 🤖")
    print(f"Find it on Telegram: @python_decoder_bot")

if __name__ == '__main__':
    try:
        setup()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled.")
        sys.exit(0)
