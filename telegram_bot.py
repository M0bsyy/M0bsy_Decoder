#!/usr/bin/env python3
"""
Python Deobfuscator & Decoder Suite - Telegram Bot
Integrates 41+ Decoders with File Upload/Download Support
"""

import os
import re
import sys
import base64
import binascii
import zlib
import marshal
import ast
import urllib.parse
import html
import codecs
import logging
import tempfile

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from telebot import TeleBot
    from telebot import types
except ImportError:
    print("❌ ERROR: pyTelegramBotAPI not installed")
    print("✓ Install with: pip install pyTelegramBotAPI")
    sys.exit(1)

BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
if not BOT_TOKEN:
    print("❌ ERROR: TELEGRAM_BOT_TOKEN environment variable not set")
    sys.exit(1)

bot = TeleBot(BOT_TOKEN)
user_sessions = {}
TEMP_DIR = tempfile.gettempdir()

class Decoder:
    @staticmethod
    def hex(x):
        return binascii.unhexlify(x).decode('utf-8')
    
    @staticmethod
    def b16(x):
        return base64.b16decode(x).decode('utf-8')
    
    @staticmethod
    def b32(x):
        return base64.b32decode(x).decode('utf-8')
    
    @staticmethod
    def b64(x):
        x_clean = x.strip()
        padding = len(x_clean) % 4
        if padding:
            x_clean += '=' * (4 - padding)
        return base64.b64decode(x_clean).decode('utf-8')
    
    @staticmethod
    def b85(x):
        return base64.b85decode(x).decode('utf-8')
    
    @staticmethod
    def a85(x):
        return base64.a85decode(x).decode('utf-8')
    
    @staticmethod
    def url_b64(x):
        x_clean = x.strip()
        padding = len(x_clean) % 4
        if padding:
            x_clean += '=' * (4 - padding)
        return base64.urlsafe_b64decode(x_clean).decode('utf-8')
    
    @staticmethod
    def zlib_data(x):
        return zlib.decompress(binascii.unhexlify(x)).decode('utf-8')
    
    @staticmethod
    def marshal(x):
        return str(marshal.loads(binascii.unhexlify(x)))
    
    @staticmethod
    def srepr(x):
        v = ast.literal_eval(x)
        return v.decode('utf-8') if isinstance(v, bytes) else str(v)
    
    @staticmethod
    def b64_zlib(x):
        x_clean = x.strip()
        padding = len(x_clean) % 4
        if padding:
            x_clean += '=' * (4 - padding)
        return zlib.decompress(base64.b64decode(x_clean)).decode('utf-8')
    
    @staticmethod
    def b32_zlib(x):
        return zlib.decompress(base64.b32decode(x)).decode('utf-8')
    
    @staticmethod
    def b85_zlib(x):
        return zlib.decompress(base64.b85decode(x)).decode('utf-8')
    
    @staticmethod
    def a85_zlib(x):
        return zlib.decompress(base64.a85decode(x)).decode('utf-8')
    
    @staticmethod
    def url_b64_zlib(x):
        x_clean = x.strip()
        padding = len(x_clean) % 4
        if padding:
            x_clean += '=' * (4 - padding)
        return zlib.decompress(base64.urlsafe_b64decode(x_clean)).decode('utf-8')
    
    @staticmethod
    def rot13(x):
        return codecs.decode(x, 'rot_13')
    
    @staticmethod
    def rot47(x):
        result = []
        for char in x:
            code = ord(char)
            if 33 <= code <= 126:
                result.append(chr(33 + ((code - 33 - 47) % 94)))
            else:
                result.append(char)
        return ''.join(result)
    
    @staticmethod
    def url_decode(x):
        return urllib.parse.unquote(x)
    
    @staticmethod
    def html_decode(x):
        return html.unescape(x)
    
    @staticmethod
    def uuencode_decode(x):
        return codecs.decode(x, 'uu')
    
    @staticmethod
    def quoted_printable(x):
        return codecs.decode(x, 'quopri')
    
    @staticmethod
    def atbash(x):
        result = []
        for char in x:
            if 'a' <= char <= 'z':
                result.append(chr(ord('z') - (ord(char) - ord('a'))))
            elif 'A' <= char <= 'Z':
                result.append(chr(ord('Z') - (ord(char) - ord('A'))))
            else:
                result.append(char)
        return ''.join(result)
    
    @staticmethod
    def base58(x):
        ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
        decoded = 0
        for char in x:
            decoded = decoded * 58 + ALPHABET.index(char)
        return decoded.to_bytes((decoded.bit_length() + 7) // 8, 'big').decode('utf-8', errors='ignore')
    
    @staticmethod
    def reverse(x):
        return x[::-1]
    
    @staticmethod
    def hex_ascii(x):
        return bytes.fromhex(x).decode('utf-8')
    
    @staticmethod
    def escape_decode(x):
        return x.encode('utf-8').decode('unicode_escape')
    
    @staticmethod
    def bytes_decoder(x):
        def decode_bytes_match(match):
            try:
                bytes_str = match.group(0)
                numbers = re.findall(r'\d+', bytes_str)
                nums = list(map(int, numbers))
                decoded = bytes(nums).decode()
                return f'"{decoded}"'
            except:
                return match.group(0)
        result = re.sub(r'bytes\(\[([^\]]+)\]\)\.decode\(\)', decode_bytes_match, x)
        return result.replace('.decode()', '')
    
    @staticmethod
    def auto_decode(data):
        decoders = [
            ('Base64', Decoder.b64),
            ('Base64+Zlib', Decoder.b64_zlib),
            ('URL-safe B64', Decoder.url_b64),
            ('Base32', Decoder.b32),
            ('Base32+Zlib', Decoder.b32_zlib),
            ('Hex', Decoder.hex),
            ('Base16', Decoder.b16),
            ('Base85', Decoder.b85),
            ('ASCII85', Decoder.a85),
            ('Base85+Zlib', Decoder.b85_zlib),
            ('ASCII85+Zlib', Decoder.a85_zlib),
            ('URL-B64+Zlib', Decoder.url_b64_zlib),
            ('Zlib', Decoder.zlib_data),
            ('Marshal', Decoder.marshal),
            ('ROT13', Decoder.rot13),
            ('ROT47', Decoder.rot47),
            ('Bytes', Decoder.bytes_decoder),
        ]
        
        tried = set()
        current = data.strip()
        used_formats = []
        max_iterations = 5
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            found = False
            current_str = str(current)
            
            for name, decoder in decoders:
                key = (name, current_str[:50] if len(current_str) > 50 else current_str)
                if key in tried:
                    continue
                
                try:
                    new_data = decoder(current)
                    new_str = str(new_data).strip()
                    current_str_cmp = current_str.strip()
                    
                    if new_str and new_str != current_str_cmp and len(new_str) < 5000000:
                        current = new_data
                        tried.add(key)
                        used_formats.append(name)
                        found = True
                        break
                except:
                    tried.add(key)
                    continue
            
            if not found:
                break
        
        return current, used_formats

def get_main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    keyboard.add(types.KeyboardButton("🔍 Auto Detect"))
    keyboard.add(types.KeyboardButton("📧 Base64"), types.KeyboardButton("🔤 Hex"))
    keyboard.add(types.KeyboardButton("🔐 Base32"), types.KeyboardButton("🎯 Base85"))
    keyboard.add(types.KeyboardButton("🛡️ Zlib"), types.KeyboardButton("📦 Marshal"))
    keyboard.add(types.KeyboardButton("🔄 ROT13"), types.KeyboardButton("🔗 URL Decode"))
    keyboard.add(types.KeyboardButton("📝 HTML Decode"), types.KeyboardButton("⚙️ More Options"))
    keyboard.add(types.KeyboardButton("📚 Help"), types.KeyboardButton("ℹ️ About"))
    return keyboard

def get_more_keyboard():
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    keyboard.add(types.KeyboardButton("📋 Escape"), types.KeyboardButton("🔀 Reverse"))
    keyboard.add(types.KeyboardButton("🔢 Base16"), types.KeyboardButton("📌 Base58"))
    keyboard.add(types.KeyboardButton("🎨 Atbash"), types.KeyboardButton("📤 UU Encode"))
    keyboard.add(types.KeyboardButton("💬 Quoted-Print"), types.KeyboardButton("🔡 ROT47"))
    keyboard.add(types.KeyboardButton("◀️ Back to Menu"))
    return keyboard

def get_back_keyboard():
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    keyboard.add(types.KeyboardButton("◀️ Back to Menu"))
    return keyboard

@bot.message_handler(commands=['start'])
def start_handler(message):
    user_id = message.chat.id
    user_sessions[user_id] = {'state': 'menu'}
    welcome = """
🔓 **Python Deobfuscator & Decoder Bot**

✨ **Features:**
• 41+ Decoders (Base64, Hex, Zlib, Marshal, etc.)
• Auto-Detection
• File Upload/Download
• Safe Analysis Mode

📝 **How to Use:**
1️⃣ Send encrypted text or file
2️⃣ Choose decoder from menu
3️⃣ Get decoded result instantly!

💡 **Supported:**
Base64 • Hex • Base32 • Base85 • Zlib • Marshal
URL • HTML • ROT13 • ROT47 • Atbash • And 30+ more!

**Safety First**: All analysis uses print() mode, never exec()
    """
    bot.send_message(user_id, welcome, parse_mode='Markdown', reply_markup=get_main_keyboard())

@bot.message_handler(commands=['help'])
def help_handler(message):
    help_text = """
📚 **How to Use:**

**Option 1: Send Text**
→ Paste encoded text
→ Choose decoder from menu
→ Get result instantly

**Option 2: Upload File**
→ Send .py or .txt file
→ Choose decoder
→ Receive decoded file

**Option 3: Auto-Detect**
→ Send code
→ Bot automatically detects encoding
→ Chains decoders intelligently

**Tips:**
• Large files: Send in chunks
• Multiple layers: Use Auto-Detect
• Test before running decoded code
    """
    bot.send_message(message.chat.id, help_text, parse_mode='Markdown', reply_markup=get_main_keyboard())

@bot.message_handler(commands=['about'])
def about_handler(message):
    about = """
ℹ️ **About This Bot**

**M0bsy Decoder Suite v1.0**
Python Deobfuscation & Decoding Bot

**41+ Integrated Decoders:**
Hex • Base16/32/64/85 • ASCII85 • Zlib
Marshal • ROT13/47 • URL Decode • HTML
Atbash • Base58 • UU Encode • Escape Sequences
And 20+ combinations of layered encoding!

**Features:**
✓ Text & File Support
✓ Auto-Detection & Chaining
✓ Safe Analysis Mode
✓ Termux Compatible
✓ Fast & Reliable

**For Legitimate Use Only:**
✓ Debug your own code
✓ Security research
✓ Learning & education

**GitHub:** https://github.com/M0bsyy/M0bsy_Decoder
    """
    bot.send_message(message.chat.id, about, parse_mode='Markdown', reply_markup=get_main_keyboard())

@bot.message_handler(func=lambda msg: msg.text in ["🔍 Auto Detect", "/auto"])
def auto_detect(message):
    user_id = message.chat.id
    user_sessions[user_id] = {'state': 'auto_detect_waiting'}
    bot.send_message(user_id, "📤 Send your encrypted text or file:\n\nBot will auto-detect and decode!", reply_markup=get_back_keyboard())

@bot.message_handler(func=lambda msg: msg.text in ["📧 Base64", "/base64"])
def base64_menu(message):
    user_id = message.chat.id
    user_sessions[user_id] = {'state': 'decoder_b64'}
    bot.send_message(user_id, "📤 Send Base64 encoded text or file", reply_markup=get_back_keyboard())

@bot.message_handler(func=lambda msg: msg.text in ["🔤 Hex", "/hex"])
def hex_menu(message):
    user_id = message.chat.id
    user_sessions[user_id] = {'state': 'decoder_hex'}
    bot.send_message(user_id, "📤 Send Hex encoded text or file", reply_markup=get_back_keyboard())

@bot.message_handler(func=lambda msg: msg.text in ["🔐 Base32", "/base32"])
def base32_menu(message):
    user_id = message.chat.id
    user_sessions[user_id] = {'state': 'decoder_b32'}
    bot.send_message(user_id, "📤 Send Base32 encoded text or file", reply_markup=get_back_keyboard())

@bot.message_handler(func=lambda msg: msg.text in ["🎯 Base85", "/base85"])
def base85_menu(message):
    user_id = message.chat.id
    user_sessions[user_id] = {'state': 'decoder_b85'}
    bot.send_message(user_id, "📤 Send Base85 encoded text or file", reply_markup=get_back_keyboard())

@bot.message_handler(func=lambda msg: msg.text in ["🛡️ Zlib", "/zlib"])
def zlib_menu(message):
    user_id = message.chat.id
    user_sessions[user_id] = {'state': 'decoder_zlib'}
    bot.send_message(user_id, "📤 Send Zlib compressed hex data", reply_markup=get_back_keyboard())

@bot.message_handler(func=lambda msg: msg.text in ["📦 Marshal", "/marshal"])
def marshal_menu(message):
    user_id = message.chat.id
    user_sessions[user_id] = {'state': 'decoder_marshal'}
    bot.send_message(user_id, "📤 Send Marshal bytecode (hex format)", reply_markup=get_back_keyboard())

@bot.message_handler(func=lambda msg: msg.text in ["🔄 ROT13", "/rot13"])
def rot13_menu(message):
    user_id = message.chat.id
    user_sessions[user_id] = {'state': 'decoder_rot13'}
    bot.send_message(user_id, "📤 Send ROT13 encoded text", reply_markup=get_back_keyboard())

@bot.message_handler(func=lambda msg: msg.text in ["🔗 URL Decode", "/url"])
def url_menu(message):
    user_id = message.chat.id
    user_sessions[user_id] = {'state': 'decoder_url_decode'}
    bot.send_message(user_id, "📤 Send URL encoded text", reply_markup=get_back_keyboard())

@bot.message_handler(func=lambda msg: msg.text in ["📝 HTML Decode", "/html"])
def html_menu(message):
    user_id = message.chat.id
    user_sessions[user_id] = {'state': 'decoder_html_decode'}
    bot.send_message(user_id, "📤 Send HTML encoded text", reply_markup=get_back_keyboard())

@bot.message_handler(func=lambda msg: msg.text in ["⚙️ More Options", "/more"])
def more_options(message):
    user_id = message.chat.id
    user_sessions[user_id] = {'state': 'menu'}
    bot.send_message(user_id, "📋 **More Decoders:**", parse_mode='Markdown', reply_markup=get_more_keyboard())

@bot.message_handler(func=lambda msg: msg.text in ["📋 Escape", "/escape"])
def escape_menu(message):
    user_id = message.chat.id
    user_sessions[user_id] = {'state': 'decoder_escape_decode'}
    bot.send_message(user_id, "📤 Send escape sequence text", reply_markup=get_back_keyboard())

@bot.message_handler(func=lambda msg: msg.text in ["🔀 Reverse", "/reverse"])
def reverse_menu(message):
    user_id = message.chat.id
    user_sessions[user_id] = {'state': 'decoder_reverse'}
    bot.send_message(user_id, "📤 Send text to reverse", reply_markup=get_back_keyboard())

@bot.message_handler(func=lambda msg: msg.text in ["🔢 Base16", "/base16"])
def base16_menu(message):
    user_id = message.chat.id
    user_sessions[user_id] = {'state': 'decoder_b16'}
    bot.send_message(user_id, "📤 Send Base16 encoded text", reply_markup=get_back_keyboard())

@bot.message_handler(func=lambda msg: msg.text in ["📌 Base58", "/base58"])
def base58_menu(message):
    user_id = message.chat.id
    user_sessions[user_id] = {'state': 'decoder_b58'}
    bot.send_message(user_id, "📤 Send Base58 encoded text", reply_markup=get_back_keyboard())

@bot.message_handler(func=lambda msg: msg.text in ["🎨 Atbash", "/atbash"])
def atbash_menu(message):
    user_id = message.chat.id
    user_sessions[user_id] = {'state': 'decoder_atbash'}
    bot.send_message(user_id, "📤 Send Atbash encoded text", reply_markup=get_back_keyboard())

@bot.message_handler(func=lambda msg: msg.text in ["📤 UU Encode", "/uu"])
def uu_menu(message):
    user_id = message.chat.id
    user_sessions[user_id] = {'state': 'decoder_uu'}
    bot.send_message(user_id, "📤 Send UU encoded text", reply_markup=get_back_keyboard())

@bot.message_handler(func=lambda msg: msg.text in ["💬 Quoted-Print", "/qp"])
def qp_menu(message):
    user_id = message.chat.id
    user_sessions[user_id] = {'state': 'decoder_qp'}
    bot.send_message(user_id, "📤 Send Quoted-Printable encoded text", reply_markup=get_back_keyboard())

@bot.message_handler(func=lambda msg: msg.text in ["🔡 ROT47", "/rot47"])
def rot47_menu(message):
    user_id = message.chat.id
    user_sessions[user_id] = {'state': 'decoder_rot47'}
    bot.send_message(user_id, "📤 Send ROT47 encoded text", reply_markup=get_back_keyboard())

@bot.message_handler(func=lambda msg: msg.text in ["📚 Help", "/help"])
def help_btn(message):
    help_handler(message)

@bot.message_handler(func=lambda msg: msg.text in ["ℹ️ About", "/about"])
def about_btn(message):
    about_handler(message)

@bot.message_handler(func=lambda msg: msg.text in ["◀️ Back to Menu", "/menu"])
def back_menu(message):
    user_id = message.chat.id
    user_sessions[user_id] = {'state': 'menu'}
    bot.send_message(user_id, "📋 **Main Menu**", parse_mode='Markdown', reply_markup=get_main_keyboard())

@bot.message_handler(content_types=['text'])
def text_handler(message):
    user_id = message.chat.id
    text = message.text.strip()
    
    if user_id not in user_sessions:
        user_sessions[user_id] = {'state': 'menu'}
    
    state = user_sessions[user_id].get('state', 'menu')
    
    if state == 'auto_detect_waiting':
        try:
            result, formats = Decoder.auto_decode(text)
            msg = f"✓ **Auto-Decoded!**\n\nUsed: {' → '.join(formats)}\n\n**Result:**\n```\n{str(result)[:2000]}\n```"
            bot.send_message(user_id, msg, parse_mode='Markdown', reply_markup=get_main_keyboard())
        except Exception as e:
            bot.send_message(user_id, f"❌ Error: {str(e)[:200]}", reply_markup=get_main_keyboard())
        user_sessions[user_id]['state'] = 'menu'
        return
    
    decoders_map = {
        'decoder_hex': ('Hex', Decoder.hex),
        'decoder_b16': ('Base16', Decoder.b16),
        'decoder_b32': ('Base32', Decoder.b32),
        'decoder_b64': ('Base64', Decoder.b64),
        'decoder_b85': ('Base85', Decoder.b85),
        'decoder_zlib': ('Zlib', Decoder.zlib_data),
        'decoder_marshal': ('Marshal', Decoder.marshal),
        'decoder_rot13': ('ROT13', Decoder.rot13),
        'decoder_rot47': ('ROT47', Decoder.rot47),
        'decoder_url_decode': ('URL Decode', Decoder.url_decode),
        'decoder_html_decode': ('HTML Decode', Decoder.html_decode),
        'decoder_b58': ('Base58', Decoder.base58),
        'decoder_reverse': ('Reverse', Decoder.reverse),
        'decoder_escape_decode': ('Escape', Decoder.escape_decode),
        'decoder_atbash': ('Atbash', Decoder.atbash),
        'decoder_uu': ('UU Encode', Decoder.uuencode_decode),
        'decoder_qp': ('Quoted-Print', Decoder.quoted_printable),
    }
    
    if state in decoders_map:
        decoder_name, decoder_func = decoders_map[state]
        try:
            result = decoder_func(text)
            msg = f"✓ **{decoder_name} Decoded:**\n```\n{str(result)[:2000]}\n```"
            bot.send_message(user_id, msg, parse_mode='Markdown', reply_markup=get_main_keyboard())
        except Exception as e:
            bot.send_message(user_id, f"❌ Error decoding with {decoder_name}: {str(e)[:200]}", reply_markup=get_main_keyboard())
        user_sessions[user_id]['state'] = 'menu'
    else:
        start_handler(message)

@bot.message_handler(content_types=['document'])
def file_handler(message):
    user_id = message.chat.id
    state = user_sessions.get(user_id, {}).get('state', 'menu')
    
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        filename = message.document.file_name
        
        decoders_map = {
            'decoder_hex': ('Hex', Decoder.hex),
            'decoder_b64': ('Base64', Decoder.b64),
            'decoder_b32': ('Base32', Decoder.b32),
            'decoder_b85': ('Base85', Decoder.b85),
            'decoder_zlib': ('Zlib', Decoder.zlib_data),
            'decoder_marshal': ('Marshal', Decoder.marshal),
            'decoder_rot13': ('ROT13', Decoder.rot13),
            'decoder_url_decode': ('URL Decode', Decoder.url_decode),
            'decoder_html_decode': ('HTML Decode', Decoder.html_decode),
            'auto_detect_waiting': ('Auto-Detect', None),
        }
        
        if state in decoders_map:
            decoder_name, decoder_func = decoders_map[state]
            
            try:
                content = downloaded_file.decode('utf-8')
            except:
                content = downloaded_file.hex()
            
            try:
                if state == 'auto_detect_waiting':
                    result, formats = Decoder.auto_decode(content)
                else:
                    result = decoder_func(content)
                
                output_filename = f"decoded_{filename}" if '.' in filename else f"decoded_{filename}.txt"
                output_path = os.path.join(TEMP_DIR, output_filename)
                
                with open(output_path, 'w') as f:
                    f.write(str(result))
                
                with open(output_path, 'rb') as f:
                    bot.send_document(user_id, f, caption=f"✓ {decoder_name} Decoded\nFile: {output_filename}")
                
                os.remove(output_path)
            except Exception as e:
                bot.send_message(user_id, f"❌ Error: {str(e)[:200]}", reply_markup=get_main_keyboard())
        else:
            bot.send_message(user_id, f"✓ File received: {filename}\n\nChoose a decoder first!", reply_markup=get_main_keyboard())
        
        user_sessions[user_id]['state'] = 'menu'
    except Exception as e:
        bot.send_message(user_id, f"❌ Error: {str(e)[:200]}", reply_markup=get_main_keyboard())

def main():
    logger.info("🚀 Bot started! Polling for messages...")
    try:
        bot.infinity_polling()
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
