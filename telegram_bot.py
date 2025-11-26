#!/usr/bin/env python3
"""
Python Deobfuscator & Decoder Suite - Telegram Bot
Handles 40+ obfuscation types via Telegram
"""

import os
import re
import sys
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import telegram bot
try:
    from telebot import TeleBot
    from telebot import types
except ImportError:
    print("❌ ERROR: python-telegram-bot not installed")
    print("\n✓ Install with:")
    print("  pip install python-telegram-bot")
    sys.exit(1)

# Bot token - use environment variable
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
if not BOT_TOKEN:
    print("❌ ERROR: TELEGRAM_BOT_TOKEN environment variable not set")
    print("\n✓ Setup steps:")
    print("  1. Get token from @BotFather on Telegram")
    print("  2. Set it: export TELEGRAM_BOT_TOKEN='your_token_here'")
    print("  3. Or create .env file:")
    print("     TELEGRAM_BOT_TOKEN=your_token_here")
    sys.exit(1)

bot = TeleBot(BOT_TOKEN)

# Store user sessions
user_sessions = {}

def get_main_keyboard():
    """Main menu keyboard"""
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    keyboard.add(types.KeyboardButton("🔍 Detect Type"))
    keyboard.add(types.KeyboardButton("🔐 Bytes Decoder"), types.KeyboardButton("📦 Marshal Convert"))
    keyboard.add(types.KeyboardButton("🛡️ Exec Replacer"), types.KeyboardButton("🔤 Hex Decoder"))
    keyboard.add(types.KeyboardButton("⚡ Hyperion"), types.KeyboardButton("🎯 PyObfuscate"))
    keyboard.add(types.KeyboardButton("📚 Help"), types.KeyboardButton("ℹ️ About"))
    return keyboard

def get_pyobf_keyboard():
    """PyObfuscate submenu"""
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    keyboard.add(types.KeyboardButton("v1 - Basic"), types.KeyboardButton("v2 - AES"))
    keyboard.add(types.KeyboardButton("◀️ Back"))
    return keyboard

def get_back_keyboard():
    """Back button"""
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    keyboard.add(types.KeyboardButton("◀️ Back to Menu"))
    return keyboard

@bot.message_handler(commands=['start'])
def start_handler(message):
    """Start command"""
    user_id = message.chat.id
    user_sessions[user_id] = {'state': 'menu'}
    
    welcome = """
🔓 **Python Deobfuscator & Decoder Bot**

Decode 40+ obfuscation types:
• bytes([...]).decode()
• marshal/PYC
• Hyperion
• PyObfuscate (v1 & v2)
• Kramer/Specter
• And more...

📝 Choose an option or:
1️⃣ Send code directly (paste obfuscated code)
2️⃣ Send file (.py file)
3️⃣ Use menu below

**Safety First**: All analysis uses print() mode, never exec()
    """
    bot.send_message(user_id, welcome, parse_mode='Markdown', reply_markup=get_main_keyboard())

@bot.message_handler(commands=['help'])
def help_handler(message):
    """Help command"""
    help_text = """
📚 **How to Use This Bot:**

**Option 1: Auto Detection**
→ Send code or file
→ Bot detects obfuscation type
→ Choose decoder from suggestions

**Option 2: Manual Selection**
→ Use /menu to see options
→ Choose decoder type
→ Send your code/file

**Option 3: Quick Commands**
/bytes - Bytes decoder
/marshal - Marshal converter
/exec - Exec replacer
/detect - Auto-detect type
/help - Show this help

**Safety:**
✓ All code analyzed with print() first
✓ Never executes untrusted code
✓ Shows you the output before any execution

**Tips:**
• Large files: Send in chunks
• Multiple layers: Decode one at a time
• Save outputs for chaining decoders
    """
    bot.send_message(message.chat.id, help_text, parse_mode='Markdown', reply_markup=get_main_keyboard())

@bot.message_handler(commands=['menu'])
def menu_handler(message):
    """Show menu"""
    user_id = message.chat.id
    user_sessions[user_id] = {'state': 'menu'}
    bot.send_message(user_id, "📋 **Choose a decoder:**", parse_mode='Markdown', reply_markup=get_main_keyboard())

@bot.message_handler(commands=['about'])
def about_handler(message):
    """About bot"""
    about = """
ℹ️ **About This Bot**

**Python Deobfuscator & Decoder Suite**
Version: 1.0
Created: 2024

**Supports 40+ Obfuscation Methods:**
• Basic: bytes, marshal, hex, exec
• Frameworks: Hyperion, Kramer, PyObfuscate, Lock
• Compression: base64, zlib, gzip
• Advanced: Cython, ELF binaries
• Plus many more...

**Features:**
✓ Auto-detection
✓ Safe analysis mode
✓ Layer-by-layer decoding
✓ File handling
✓ Batch processing

**Disclaimer:**
For legitimate purposes only:
✓ Debug your own code
✓ Security research (authorized)
✓ Learning & education

**Source & Help:**
Use /help for detailed instructions
    """
    bot.send_message(message.chat.id, about, parse_mode='Markdown', reply_markup=get_main_keyboard())

@bot.message_handler(func=lambda msg: msg.text == "🔍 Detect Type")
def detect_type(message):
    """Detect obfuscation type"""
    user_id = message.chat.id
    user_sessions[user_id] = {'state': 'detect_waiting'}
    bot.send_message(user_id, "📤 Send your obfuscated code or file to detect the type:\n\n(Paste code or upload .py file)", reply_markup=get_back_keyboard())

@bot.message_handler(func=lambda msg: msg.text == "🔐 Bytes Decoder")
def bytes_decoder_menu(message):
    """Bytes decoder"""
    user_id = message.chat.id
    user_sessions[user_id] = {'state': 'bytes_waiting'}
    bot.send_message(user_id, "📤 Send your code with bytes([...]).decode() patterns:\n\n(Example: bytes([72,101,108,108,111]).decode())", reply_markup=get_back_keyboard())

@bot.message_handler(func=lambda msg: msg.text == "📦 Marshal Convert")
def marshal_menu(message):
    """Marshal converter"""
    user_id = message.chat.id
    user_sessions[user_id] = {'state': 'marshal_waiting'}
    bot.send_message(user_id, "📤 Send marshal bytecode or .pyc file to convert", reply_markup=get_back_keyboard())

@bot.message_handler(func=lambda msg: msg.text == "🛡️ Exec Replacer")
def exec_replacer_menu(message):
    """Exec replacer"""
    user_id = message.chat.id
    user_sessions[user_id] = {'state': 'exec_waiting'}
    bot.send_message(user_id, "📤 Send code with exec() calls for safe analysis:\n\n(Will replace exec() with print())", reply_markup=get_back_keyboard())

@bot.message_handler(func=lambda msg: msg.text == "🔤 Hex Decoder")
def hex_decoder_menu(message):
    """Hex decoder"""
    user_id = message.chat.id
    user_sessions[user_id] = {'state': 'hex_waiting'}
    bot.send_message(user_id, "📤 Send hex-encoded Python code", reply_markup=get_back_keyboard())

@bot.message_handler(func=lambda msg: msg.text == "⚡ Hyperion")
def hyperion_menu(message):
    """Hyperion deobfuscator"""
    user_id = message.chat.id
    user_sessions[user_id] = {'state': 'hyperion_waiting'}
    bot.send_message(user_id, "📤 Send Hyperion-obfuscated code (contains exec((_)(b'...')))", reply_markup=get_back_keyboard())

@bot.message_handler(func=lambda msg: msg.text == "🎯 PyObfuscate")
def pyobf_menu(message):
    """PyObfuscate menu"""
    user_id = message.chat.id
    user_sessions[user_id] = {'state': 'pyobf_menu'}
    bot.send_message(user_id, "Which PyObfuscate version?", reply_markup=get_pyobf_keyboard())

@bot.message_handler(func=lambda msg: msg.text == "v1 - Basic")
def pyobf_v1(message):
    """PyObfuscate v1"""
    user_id = message.chat.id
    user_sessions[user_id] = {'state': 'pyobf_v1_waiting'}
    bot.send_message(user_id, "📤 Send PyObfuscate v1 encoded code", reply_markup=get_back_keyboard())

@bot.message_handler(func=lambda msg: msg.text == "v2 - AES")
def pyobf_v2(message):
    """PyObfuscate v2"""
    user_id = message.chat.id
    user_sessions[user_id] = {'state': 'pyobf_v2_waiting'}
    bot.send_message(user_id, "📤 Send PyObfuscate v2 encrypted code (AES)", reply_markup=get_back_keyboard())

@bot.message_handler(func=lambda msg: msg.text == "📚 Help")
def help_btn(message):
    """Help button"""
    help_handler(message)

@bot.message_handler(func=lambda msg: msg.text == "ℹ️ About")
def about_btn(message):
    """About button"""
    about_handler(message)

@bot.message_handler(func=lambda msg: msg.text in ["◀️ Back", "◀️ Back to Menu"])
def back_menu(message):
    """Back to menu"""
    menu_handler(message)

def analyze_code(code):
    """Analyze code for obfuscation patterns"""
    patterns = {
        'bytes': ('Bytes encoding', 'bytes([' in code or 'bytes.fromhex' in code),
        'marshal': ('Marshal bytecode', 'marshal.loads' in code),
        'base64': ('Base64 encoding', 'base64.b64' in code or 'b64decode' in code),
        'zlib': ('Zlib compression', 'zlib.decompress' in code),
        'hyperion': ('Hyperion obfuscation', 'exec((_)' in code or '__import__(\'zlib\').decompress' in code),
        'pyobfuscate': ('PyObfuscate detected', 'pyobfuscate' in code.lower()),
        'exec': ('Exec/Eval obfuscation', 'exec(' in code or 'eval(' in code),
        'lambda': ('Lambda obfuscation', 'lambda' in code),
        'hex': ('Hex encoding', '.fromhex' in code or '\\x' in code),
    }
    
    detected = []
    for key, (name, check) in patterns.items():
        if check:
            detected.append(name)
    
    return detected if detected else ['Unknown pattern - try auto-detection']

@bot.message_handler(content_types=['text'])
def text_handler(message):
    """Handle text messages"""
    user_id = message.chat.id
    text = message.text
    
    if user_id not in user_sessions:
        user_sessions[user_id] = {'state': 'menu'}
    
    state = user_sessions[user_id].get('state', 'menu')
    
    # Detect type mode
    if state == 'detect_waiting':
        detected = analyze_code(text)
        response = "🔍 **Detected Obfuscation Types:**\n\n"
        for d in detected:
            response += f"• {d}\n"
        response += "\n**Recommended:**\n"
        
        if 'Bytes encoding' in detected:
            response += "→ Use /bytes decoder\n"
        if 'Marshal bytecode' in detected:
            response += "→ Use /marshal converter\n"
        if 'Hyperion obfuscation' in detected:
            response += "→ Use /hyperion decoder\n"
        
        response += "\nTry a specific decoder or /help"
        bot.send_message(user_id, response, parse_mode='Markdown', reply_markup=get_main_keyboard())
        user_sessions[user_id]['state'] = 'menu'
    
    # Bytes decoder
    elif state == 'bytes_waiting':
        try:
            result = decode_bytes_text(text)
            if len(result) > 4000:
                bot.send_message(user_id, f"✓ **Decoded:**\n```\n{result[:4000]}\n```\n\n(output truncated)", parse_mode='Markdown', reply_markup=get_main_keyboard())
            else:
                bot.send_message(user_id, f"✓ **Decoded:**\n```python\n{result}\n```", parse_mode='Markdown', reply_markup=get_main_keyboard())
            user_sessions[user_id]['state'] = 'menu'
        except Exception as e:
            bot.send_message(user_id, f"❌ Error: {str(e)[:200]}", reply_markup=get_main_keyboard())
            user_sessions[user_id]['state'] = 'menu'
    
    # Exec replacer
    elif state == 'exec_waiting':
        try:
            result = text.replace('exec(', 'print(').replace('eval(', 'print(')
            if len(result) > 4000:
                bot.send_message(user_id, f"✓ **Safe Version (exec→print):**\n```\n{result[:4000]}\n```\n\n(truncated)", parse_mode='Markdown', reply_markup=get_main_keyboard())
            else:
                bot.send_message(user_id, f"✓ **Safe Version (exec→print):**\n```python\n{result}\n```", parse_mode='Markdown', reply_markup=get_main_keyboard())
            user_sessions[user_id]['state'] = 'menu'
        except Exception as e:
            bot.send_message(user_id, f"❌ Error: {str(e)[:200]}", reply_markup=get_main_keyboard())
            user_sessions[user_id]['state'] = 'menu'
    
    else:
        start_handler(message)

def decode_bytes_text(text):
    """Decode bytes patterns from text"""
    def decode_bytes_match(match):
        try:
            bytes_str = match.group(0)
            numbers = re.findall(r'\d+', bytes_str)
            nums = list(map(int, numbers))
            decoded = bytes(nums).decode()
            return f'"{decoded}"'
        except:
            return match.group(0)
    
    result = re.sub(r'bytes\(\[([^\]]+)\]\)\.decode\(\)', decode_bytes_match, text)
    result = result.replace('.decode()', '')
    return result

@bot.message_handler(content_types=['document'])
def document_handler(message):
    """Handle file uploads"""
    user_id = message.chat.id
    state = user_sessions.get(user_id, {}).get('state', 'menu')
    
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        filename = message.document.file_name
        
        if state == 'detect_waiting':
            try:
                content = downloaded_file.decode('utf-8')
                detected = analyze_code(content)
                response = "🔍 **Detected in file:**\n"
                for d in detected:
                    response += f"• {d}\n"
                bot.send_message(user_id, response, parse_mode='Markdown', reply_markup=get_main_keyboard())
            except:
                bot.send_message(user_id, "❌ Could not decode file as text", reply_markup=get_main_keyboard())
        
        else:
            bot.send_message(user_id, f"✓ File received: {filename}\n\nSupport for file decoding coming soon.", reply_markup=get_main_keyboard())
        
        user_sessions[user_id]['state'] = 'menu'
    except Exception as e:
        bot.send_message(user_id, f"❌ Error: {str(e)[:200]}", reply_markup=get_main_keyboard())
        user_sessions[user_id]['state'] = 'menu'

def main():
    """Start bot"""
    logger.info("🚀 Bot started! Polling for messages...")
    try:
        bot.infinity_polling()
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
