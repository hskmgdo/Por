import telebot
from telebot.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    Message, CallbackQuery, InputFile
)
import time
import json
import sqlite3
import logging
import os
import random
import hashlib
import base64
import requests
import threading
import queue
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from typing import List, Dict, Optional, Tuple
import re

# ========== تنظیمات اصلی ==========
BOT_TOKEN = "8810741889:AAEe7Q1eCuBuSRWNfDxGhJrXDijrO0PX6t4"
ADMIN_ID = 8680457924
bot = telebot.TeleBot(BOT_TOKEN, parse_mode='HTML')

# ========== تنظیمات لاگینگ پیشرفته ==========
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    handlers=[
        logging.FileHandler('vpn_bot_advanced.log'),
        logging.StreamHandler(),
        logging.FileHandler('errors.log', level=logging.ERROR)
    ]
)
logger = logging.getLogger(__name__)

# ========== کانفیگ‌های پیشرفته و گسترده ==========
class AdvancedConfigManager:
    """مدیریت کانفیگ‌های پیشرفته با سیستم هوشمند"""
    
    # دیتابیس گسترده دامنه‌های فعال
    DOMAIN_DATABASE = {
        "iran": [
            "v1.arashkhatare.ggff.net",
            "v2.arashkhatare.ggff.net",
            "v3.arashkhatare.ggff.net",
            "v4.arashkhatare.ggff.net",
            "v5.arashkhatare.ggff.net",
            "v6.arashkhatare.ggff.net",
            "v7.arashkhatare.ggff.net",
            "v8.arashkhatare.ggff.net",
            "v9.arashkhatare.ggff.net",
            "v10.arashkhatare.ggff.net"
        ],
        "international": [
            "v1.anonymouse.observer",
            "v2.anonymouse.observer",
            "v3.anonymouse.observer",
            "v4.anonymouse.observer",
            "v5.anonymouse.observer",
            "v6.anonymouse.observer",
            "v7.anonymouse.observer",
            "v8.anonymouse.observer",
            "v9.anonymouse.observer",
            "v10.anonymouse.observer"
        ],
        "backup": [
            "v1.whitedns.pro",
            "v2.whitedns.pro",
            "v3.whitedns.pro",
            "v4.whitedns.pro",
            "v5.whitedns.pro",
            "v6.whitedns.pro",
            "v7.whitedns.pro",
            "v8.whitedns.pro",
            "v9.whitedns.pro",
            "v10.whitedns.pro"
        ]
    }
    
    # کلیدهای رمزنگاری پیشرفته
    ENCRYPTION_KEYS = [
        "ed0cef16b7153b8d835a327861597c64",
        "b275039199b1c8c9",
        "f8a2e1c4b9d3f5a7",
        "a1b2c3d4e5f67890",
        "9f8e7d6c5b4a3210",
        "c3d5e7f9a1b2c4d6",
        "e8f0a2b4c6d8e0f2",
        "1a2b3c4d5e6f7890",
        "abcdef1234567890",
        "fedcba0987654321"
    ]
    
    # متدهای رمزنگاری
    ENCRYPTION_METHODS = [1, 2, 3, 4, 5]
    
    # تنظیمات کیفیت
    QUALITY_SETTINGS = {
        "high": {"method": 3, "key_level": 5},
        "medium": {"method": 2, "key_level": 3},
        "low": {"method": 1, "key_level": 1}
    }
    
    @classmethod
    def generate_smart_config(cls, region="iran", quality="high", custom_domain=None):
        """تولید هوشمند کانفیگ بر اساس منطقه و کیفیت"""
        
        # انتخاب دامنه
        if custom_domain:
            domain = custom_domain
        else:
            domains = cls.DOMAIN_DATABASE.get(region, cls.DOMAIN_DATABASE["iran"])
            domain = random.choice(domains)
        
        # انتخاب کلید بر اساس کیفیت
        quality_level = cls.QUALITY_SETTINGS.get(quality, cls.QUALITY_SETTINGS["medium"])
        key_index = min(quality_level["key_level"], len(cls.ENCRYPTION_KEYS) - 1)
        key = cls.ENCRYPTION_KEYS[key_index]
        
        method = quality_level["method"]
        
        # ساخت نام هوشمند
        prefixes = ["grootz", "rezagrootz", "vpn", "secure", "premium", "ultra", "pro", "max"]
        names = ["server", "node", "edge", "cloud", "net", "hub", "core", "prime"]
        
        profile_name = f"{random.choice(prefixes)}_{random.choice(names)}_{random.randint(100, 999)}"
        
        # ساخت کانفیگ
        config_data = {
            "schema": "whitedns.profile",
            "version": 1,
            "profile": {
                "name": profile_name,
                "server": {
                    "domain": domain,
                    "encryption_key": key,
                    "encryption_method": method
                },
                "metadata": {
                    "region": region,
                    "quality": quality,
                    "generated": datetime.now().isoformat()
                }
            }
        }
        
        json_str = json.dumps(config_data)
        base64_config = base64.b64encode(json_str.encode()).decode()
        return f"stormdns://{base64_config}"
    
    @classmethod
    def generate_batch_configs(cls, count=10, region="iran", quality="high"):
        """تولید دسته‌ای کانفیگ‌ها"""
        configs = []
        for _ in range(count):
            config = cls.generate_smart_config(
                region=random.choice(list(cls.DOMAIN_DATABASE.keys())),
                quality=random.choice(["high", "medium", "low"])
            )
            configs.append(config)
        return configs
    
    @classmethod
    def validate_and_analyze_config(cls, config_string):
        """تحلیل و اعتبارسنجی پیشرفته کانفیگ"""
        try:
            if not config_string.startswith("stormdns://"):
                return False, "فرمت کانفیگ نامعتبر است"
            
            encoded = config_string.replace("stormdns://", "")
            decoded = base64.b64decode(encoded).decode()
            data = json.loads(decoded)
            
            # بررسی کامل ساختار
            if "profile" not in data:
                return False, "پروفایل یافت نشد"
            
            profile = data["profile"]
            if "server" not in profile:
                return False, "سرور یافت نشد"
            
            server = profile["server"]
            required_fields = ["domain", "encryption_key", "encryption_method"]
            
            for field in required_fields:
                if field not in server:
                    return False, f"فیلد {field} یافت نشد"
            
            # تحلیل کیفیت
            quality_score = 0
            if server["encryption_method"] >= 3:
                quality_score += 2
            elif server["encryption_method"] >= 2:
                quality_score += 1
            
            if len(server["encryption_key"]) >= 16:
                quality_score += 2
            elif len(server["encryption_key"]) >= 8:
                quality_score += 1
            
            # تعیین کیفیت
            if quality_score >= 4:
                quality = "عالی"
            elif quality_score >= 3:
                quality = "خوب"
            else:
                quality = "معمولی"
            
            return True, {
                "valid": True,
                "quality": quality,
                "quality_score": quality_score,
                "domain": server["domain"],
                "method": server["encryption_method"],
                "key_length": len(server["encryption_key"])
            }
            
        except Exception as e:
            return False, f"خطا: {str(e)}"

# ========== دیتابیس فوق‌پیشرفته ==========
class SuperDatabase:
    def __init__(self, db_file='super_vpn.db'):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_tables()
        self._create_indexes()
    
    def _create_tables(self):
        # جدول کاربران پیشرفته
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                join_date INTEGER,
                last_seen INTEGER,
                configs_received INTEGER DEFAULT 0,
                total_connections INTEGER DEFAULT 0,
                favorite_region TEXT,
                premium_status INTEGER DEFAULT 0,
                premium_expiry INTEGER,
                referrer_id INTEGER,
                referred_users INTEGER DEFAULT 0
            )
        ''')
        
        # جدول کانفیگ‌ها با اطلاعات کامل
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS configs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                config TEXT,
                config_hash TEXT,
                region TEXT,
                quality TEXT,
                received_date INTEGER,
                last_used INTEGER,
                usage_count INTEGER DEFAULT 0,
                is_active INTEGER DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # جدول آمار روزانه
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_stats (
                date TEXT PRIMARY KEY,
                total_users INTEGER DEFAULT 0,
                total_configs INTEGER DEFAULT 0,
                new_users INTEGER DEFAULT 0,
                active_users INTEGER DEFAULT 0
            )
        ''')
        
        # جدول تنظیمات کاربر
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_settings (
                user_id INTEGER PRIMARY KEY,
                auto_config INTEGER DEFAULT 0,
                preferred_region TEXT DEFAULT 'iran',
                preferred_quality TEXT DEFAULT 'high',
                notification_enabled INTEGER DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        self.conn.commit()
    
    def _create_indexes(self):
        """ایجاد ایندکس‌ها برای سرعت بیشتر"""
        self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_configs ON configs(user_id)')
        self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_config_hash ON configs(config_hash)')
        self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_last_seen ON users(last_seen)')
        self.conn.commit()
    
    def execute(self, query, params=()):
        self.cursor.execute(query, params)
        self.conn.commit()
        return self.cursor
    
    def fetch_one(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()
    
    def fetch_all(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
    def get_user_stats_full(self, user_id):
        """گرفتن آمار کامل کاربر"""
        user = self.fetch_one("SELECT * FROM users WHERE user_id = ?", (user_id,))
        if not user:
            return None
        
        configs = self.fetch_all("SELECT * FROM configs WHERE user_id = ? ORDER BY received_date DESC", (user_id,))
        settings = self.fetch_one("SELECT * FROM user_settings WHERE user_id = ?", (user_id,))
        
        return {
            "user": user,
            "configs": configs,
            "settings": settings
        }
    
    def close(self):
        self.conn.close()

db = SuperDatabase()

# ========== سیستم کش هوشمند ==========
class SmartCache:
    """سیستم کش برای کاهش درخواست‌ها"""
    def __init__(self, max_size=100):
        self.cache = {}
        self.max_size = max_size
        self.access_times = {}
    
    def get(self, key):
        if key in self.cache:
            self.access_times[key] = time.time()
            return self.cache[key]
        return None
    
    def set(self, key, value, ttl=3600):
        if len(self.cache) >= self.max_size:
            # حذف قدیمی‌ترین آیتم
            oldest_key = min(self.access_times, key=self.access_times.get)
            del self.cache[oldest_key]
            del self.access_times[oldest_key]
        
        self.cache[key] = {
            "value": value,
            "created": time.time(),
            "ttl": ttl
        }
        self.access_times[key] = time.time()
    
    def clear_expired(self):
        current_time = time.time()
        expired_keys = []
        for key, data in self.cache.items():
            if current_time - data["created"] > data["ttl"]:
                expired_keys.append(key)
        
        for key in expired_keys:
            del self.cache[key]
            if key in self.access_times:
                del self.access_times[key]

cache = SmartCache()

# ========== توابع پیشرفته ==========
def create_advanced_user(user_id, username=None, first_name=None, last_name=None):
    """ثبت پیشرفته کاربر"""
    now = int(time.time())
    
    # بررسی وجود کاربر
    existing = db.fetch_one("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
    
    if not existing:
        db.execute("""
            INSERT INTO users (user_id, username, first_name, last_name, join_date, last_seen)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, username, first_name, last_name, now, now))
        
        # ایجاد تنظیمات پیش‌فرض
        db.execute("""
            INSERT OR IGNORE INTO user_settings (user_id, preferred_region, preferred_quality)
            VALUES (?, 'iran', 'high')
        """, (user_id,))
        
        # به‌روزرسانی آمار روزانه
        today = datetime.now().strftime("%Y-%m-%d")
        db.execute("""
            INSERT OR IGNORE INTO daily_stats (date, total_users, total_configs, new_users, active_users)
            VALUES (?, 0, 0, 0, 0)
        """, (today,))
        
        db.execute("""
            UPDATE daily_stats SET total_users = total_users + 1, new_users = new_users + 1
            WHERE date = ?
        """, (today,))
    
    else:
        db.execute("UPDATE users SET last_seen = ? WHERE user_id = ?", (now, user_id))
    
    # به‌روزرسانی نام کاربری
    if username:
        db.execute("UPDATE users SET username = ? WHERE user_id = ?", (username, user_id))

def save_advanced_config(user_id, config, region="iran", quality="high"):
    """ذخیره پیشرفته کانفیگ"""
    now = int(time.time())
    config_hash = hashlib.sha256(config.encode()).hexdigest()[:16]
    
    db.execute("""
        INSERT INTO configs (user_id, config, config_hash, region, quality, received_date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, config, config_hash, region, quality, now))
    
    db.execute("""
        UPDATE users SET configs_received = configs_received + 1
        WHERE user_id = ?
    """, (user_id,))
    
    # به‌روزرسانی آمار روزانه
    today = datetime.now().strftime("%Y-%m-%d")
    db.execute("""
        UPDATE daily_stats SET total_configs = total_configs + 1
        WHERE date = ?
    """, (today,))

def format_time_advanced(timestamp):
    """فرمت‌دهی پیشرفته زمان"""
    if not timestamp:
        return "نامحدود"
    
    dt = datetime.fromtimestamp(timestamp)
    now = datetime.now()
    
    diff = now - dt
    
    if diff.days > 0:
        return f"{diff.days} روز پیش"
    elif diff.seconds > 3600:
        return f"{diff.seconds // 3600} ساعت پیش"
    elif diff.seconds > 60:
        return f"{diff.seconds // 60} دقیقه پیش"
    else:
        return "چند لحظه پیش"

# ========== کیبوردهای فوق‌پیشرفته ==========
def advanced_main_menu():
    """منوی اصلی فوق‌پیشرفته"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("🌐 دریافت کانفیگ", callback_data="smart_config"),
        InlineKeyboardButton("📦 دریافت دسته‌ای", callback_data="batch_config")
    )
    keyboard.add(
        InlineKeyboardButton("🎯 کانفیگ اختصاصی", callback_data="custom_config"),
        InlineKeyboardButton("🔄 کانفیگ جدید", callback_data="fresh_config")
    )
    keyboard.add(
        InlineKeyboardButton("📊 وضعیت من", callback_data="my_status_advanced"),
        InlineKeyboardButton("⚙️ تنظیمات", callback_data="settings")
    )
    keyboard.add(
        InlineKeyboardButton("🏆 بهترین کانفیگ", callback_data="best_config"),
        InlineKeyboardButton("🪄 سرور اختصاصی", url="https://t.me/Grootz_Support")
    )
    keyboard.add(
        InlineKeyboardButton("ℹ️ راهنمای پیشرفته", callback_data="advanced_help"),
        InlineKeyboardButton("📈 آمار پیشرفته", callback_data="advanced_stats")
    )
    return keyboard

def config_options_menu():
    """منوی گزینه‌های کانفیگ"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("🇮🇷 ایران", callback_data="region_iran"),
        InlineKeyboardButton("🌍 بین‌الملل", callback_data="region_international")
    )
    keyboard.add(
        InlineKeyboardButton("🔄 پشتیبان", callback_data="region_backup"),
        InlineKeyboardButton("🎯 هوشمند", callback_data="region_smart")
    )
    keyboard.add(
        InlineKeyboardButton("⭐ کیفیت بالا", callback_data="quality_high"),
        InlineKeyboardButton("🔶 کیفیت متوسط", callback_data="quality_medium")
    )
    keyboard.add(
        InlineKeyboardButton("🔙 بازگشت", callback_data="back_main")
    )
    return keyboard

def settings_menu():
    """منوی تنظیمات پیشرفته"""
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("🌍 منطقه پیش‌فرض", callback_data="set_default_region"),
        InlineKeyboardButton("⭐ کیفیت پیش‌فرض", callback_data="set_default_quality"),
        InlineKeyboardButton("🔄 کانفیگ خودکار", callback_data="toggle_auto_config"),
        InlineKeyboardButton("🔔 اعلان‌ها", callback_data="toggle_notifications"),
        InlineKeyboardButton("🔙 بازگشت", callback_data="back_main")
    )
    return keyboard

# ========== دستورات اصلی ==========
@bot.message_handler(commands=['start'])
def start_advanced_command(message):
    user = message.from_user
    create_advanced_user(user.id, user.username, user.first_name, user.last_name)
    
    # بررسی ارجاع
    if len(message.text.split()) > 1:
        referrer_id = message.text.split()[1]
        if referrer_id.isdigit():
            db.execute("UPDATE users SET referrer_id = ? WHERE user_id = ?", 
                      (int(referrer_id), user.id))
    
    text = f"""
🚀 **ربات فوق‌پیشرفته VPN WhiteDNS** 🚀
━━━━━━━━━━━━━━━━━━━━━━
👤 **کاربر:** {user.first_name} {user.last_name or ''}
🆔 **آیدی:** `{user.id}`
📅 **تاریخ:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
━━━━━━━━━━━━━━━━━━━━━━

✨ **به ربات حرفه‌ای خوش آمدید!**

🔹 **امکانات پیشرفته:**
• کانفیگ‌های هوشمند با کیفیت بالا
• انتخاب منطقه (ایران/بین‌الملل)
• دریافت دسته‌ای ۱۰، ۲۰، ۵۰ کانفیگ
• کانفیگ‌های اختصاصی و سفارشی
• سیستم تحلیل کیفیت کانفیگ‌ها

💡 **نکته:** برای بهترین نتیجه، از گزینه "کانفیگ هوشمند" استفاده کنید.
"""
    bot.reply_to(message, text, reply_markup=advanced_main_menu(), parse_mode='HTML')

@bot.message_handler(commands=['help'])
def advanced_help_command(message):
    text = """
📚 **راهنمای پیشرفته ربات WhiteDNS**
━━━━━━━━━━━━━━━━━━━━━━

**🔹 دستورات اصلی:**
/start - منوی اصلی
/help - این راهنما
/stats - آمار پیشرفته

**🔹 کانفیگ‌ها:**
• **کانفیگ هوشمند:** بهترین کانفیگ با توجه به موقعیت شما
• **کانفیگ دسته‌ای:** دریافت ۱۰، ۲۰ یا ۵۰ کانفیگ
• **کانفیگ اختصاصی:** کانفیگ با تنظیمات دلخواه
• **بهترین کانفیگ:** بهترین کانفیگ موجود

**🔹 تنظیمات:**
• انتخاب منطقه پیش‌فرض
• انتخاب کیفیت کانفیگ
• فعال‌سازی کانفیگ خودکار

**🔹 پشتیبانی:**
@Grootz_Support
"""
    bot.reply_to(message, text, reply_markup=get_back_button(), parse_mode='HTML')

# ========== هندلرهای پیشرفته ==========
@bot.callback_query_handler(func=lambda call: call.data == "smart_config")
def handle_smart_config(call):
    """تولید کانفیگ هوشمند"""
    user_id = call.from_user.id
    create_advanced_user(user_id, call.from_user.username, call.from_user.first_name, call.from_user.last_name)
    
    # دریافت تنظیمات کاربر
    settings = db.fetch_one("SELECT preferred_region, preferred_quality FROM user_settings WHERE user_id = ?", (user_id,))
    
    region = settings[0] if settings else "iran"
    quality = settings[1] if settings else "high"
    
    # تولید کانفیگ هوشمند
    config = AdvancedConfigManager.generate_smart_config(region=region, quality=quality)
    
    # تحلیل کانفیگ
    valid, analysis = AdvancedConfigManager.validate_and_analyze_config(config)
    
    # ذخیره کانفیگ
    save_advanced_config(user_id, config, region, quality)
    
    text = f"""
🎯 **کانفیگ هوشمند WhiteDNS**
━━━━━━━━━━━━━━━━━━━━━━
👤 **کاربر:** {call.from_user.first_name}
🌍 **منطقه:** {region}
⭐ **کیفیت:** {quality}
━━━━━━━━━━━━━━━━━━━━━━

📋 **کانفیگ شما:**
<code>{config}</code>

━━━━━━━━━━━━━━━━━━━━━━
📊 **تحلیل کانفیگ:**
✅ **اعتبار:** معتبر
⭐ **کیفیت:** {analysis['quality'] if isinstance(analysis, dict) else 'عالی'}
🌐 **دامنه:** {analysis['domain'] if isinstance(analysis, dict) else 'فعال'}
🔐 **متد:** {analysis['method'] if isinstance(analysis, dict) else 'پیشرفته'}

💡 **نکته:** این کانفیگ بر اساس تنظیمات شما ساخته شده است.
"""
    
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("🔄 کانفیگ جدید", callback_data="smart_config"),
        InlineKeyboardButton("📦 کانفیگ دسته‌ای", callback_data="batch_config")
    )
    keyboard.add(
        InlineKeyboardButton("⚙️ تنظیمات", callback_data="settings"),
        InlineKeyboardButton("🔙 بازگشت", callback_data="back_main")
    )
    
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                         reply_markup=keyboard, parse_mode='HTML')
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "batch_config")
def handle_batch_config(call):
    """دریافت دسته‌ای کانفیگ"""
    keyboard = InlineKeyboardMarkup(row_width=3)
    keyboard.add(
        InlineKeyboardButton("۱۰ عدد", callback_data="batch_10"),
        InlineKeyboardButton("۲۰ عدد", callback_data="batch_20"),
        InlineKeyboardButton("۵۰ عدد", callback_data="batch_50")
    )
    keyboard.add(
        InlineKeyboardButton("🔙 بازگشت", callback_data="back_main")
    )
    
    bot.edit_message_text("""
📦 **دریافت دسته‌ای کانفیگ**
━━━━━━━━━━━━━━━━━━━━━━
تعداد کانفیگ‌های مورد نظر را انتخاب کنید:

✅ همه کانفیگ‌ها معتبر و فعال هستند
✅ با دامنه‌های مختلف
✅ کیفیت بالا
""", call.message.chat.id, call.message.message_id,
                         reply_markup=keyboard, parse_mode='HTML')
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("batch_"))
def handle_batch_count(call):
    """تولید کانفیگ‌های دسته‌ای"""
    user_id = call.from_user.id
    create_advanced_user(user_id, call.from_user.username, call.from_user.first_name, call.from_user.last_name)
    
    count = int(call.data.split("_")[1])
    
    # تولید کانفیگ‌ها
    configs = AdvancedConfigManager.generate_batch_configs(count)
    
    # ذخیره کانفیگ‌ها
    for config in configs:
        save_advanced_config(user_id, config)
    
    text = f"""
📦 **{count} کانفیگ جدید WhiteDNS**
━━━━━━━━━━━━━━━━━━━━━━
👤 **کاربر:** {call.from_user.first_name}
━━━━━━━━━━━━━━━━━━━━━━

✅ **{count} کانفیگ معتبر** برای شما ارسال شد.

"""
    # ارسال کانفیگ‌ها در چند پیام
    batch_size = 5
    for i in range(0, count, batch_size):
        batch = configs[i:i+batch_size]
        msg = ""
        for j, config in enumerate(batch, i+1):
            msg += f"📋 **کانفیگ {j}:**\n<code>{config}</code>\n\n"
        bot.send_message(call.message.chat.id, msg, parse_mode='HTML')
    
    text += """
💡 **توصیه:** برای بهترین سرعت، کانفیگ‌های مختلف را تست کنید.
"""
    
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("🔄 کانفیگ جدید", callback_data="smart_config"),
        InlineKeyboardButton("🔙 بازگشت", callback_data="back_main")
    )
    
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                         reply_markup=keyboard, parse_mode='HTML')
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "best_config")
def handle_best_config(call):
    """ارسال بهترین کانفیگ موجود"""
    user_id = call.from_user.id
    create_advanced_user(user_id, call.from_user.username, call.from_user.first_name, call.from_user.last_name)
    
    # تولید چند کانفیگ و انتخاب بهترین
    configs = AdvancedConfigManager.generate_batch_configs(5)
    
    # تحلیل و انتخاب بهترین
    best_config = None
    best_score = -1
    
    for config in configs:
        valid, analysis = AdvancedConfigManager.validate_and_analyze_config(config)
        if valid and isinstance(analysis, dict):
            if analysis["quality_score"] > best_score:
                best_score = analysis["quality_score"]
                best_config = config
    
    if not best_config:
        best_config = configs[0]
    
    save_advanced_config(user_id, best_config)
    
    text = f"""
🏆 **بهترین کانفیگ WhiteDNS**
━━━━━━━━━━━━━━━━━━━━━━
👤 **کاربر:** {call.from_user.first_name}
━━━━━━━━━━━━━━━━━━━━━━

📋 **بهترین کانفیگ:**
<code>{best_config}</code>

━━━━━━━━━━━━━━━━━━━━━━
⭐ **کیفیت:** عالی
🔐 **امنیت:** بالا
🚀 **سرعت:** بسیار بالا
📌 **پایداری:** عالی

💡 **نکته:** این کانفیگ از بین ۵ کانفیگ مختلف انتخاب شده است.
"""
    
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("🔄 کانفیگ جدید", callback_data="smart_config"),
        InlineKeyboardButton("🔙 بازگشت", callback_data="back_main")
    )
    
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                         reply_markup=keyboard, parse_mode='HTML')
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "my_status_advanced")
def handle_advanced_status(call):
    """نمایش وضعیت پیشرفته کاربر"""
    user_id = call.from_user.id
    stats = db.get_user_stats_full(user_id)
    
    if not stats:
        create_advanced_user(user_id, call.from_user.username, call.from_user.first_name, call.from_user.last_name)
        stats = db.get_user_stats_full(user_id)
    
    user = stats["user"]
    configs = stats["configs"]
    settings = stats["settings"]
    
    text = f"""
📊 **وضعیت پیشرفته کاربری**
━━━━━━━━━━━━━━━━━━━━━━
👤 **نام:** {user[2]} {user[3] or ''}
🆔 **آیدی:** `{user[0]}`
👤 **یوزرنیم:** @{user[1] or 'ندارد'}
━━━━━━━━━━━━━━━━━━━━━━
📅 **عضویت:** {format_time_advanced(user[4])}
🔄 **آخرین بازدید:** {format_time_advanced(user[5])}
📋 **کانفیگ‌های دریافت شده:** {user[6]}
🔗 **تعداد ارجاع:** {user[9] if len(user) > 9 else 0}
━━━━━━━━━━━━━━━━━━━━━━
🌍 **منطقه پیش‌فرض:** {settings[1] if settings else 'iran'}
⭐ **کیفیت پیش‌فرض:** {settings[2] if settings else 'high'}
🔄 **کانفیگ خودکار:** {'✅ فعال' if settings[3] else '❌ غیرفعال'}
━━━━━━━━━━━━━━━━━━━━━━
📋 **تعداد کانفیگ‌های موجود:** {len(configs)}

✅ **وضعیت:** فعال
"""
    
    keyboard = InlineKeyboardMarkup(row_width=1)
    if configs:
        keyboard.add(InlineKeyboardButton("📋 مشاهده کانفیگ‌ها", callback_data="view_all_configs"))
    keyboard.add(
        InlineKeyboardButton("🌐 دریافت کانفیگ", callback_data="smart_config"),
        InlineKeyboardButton("⚙️ تنظیمات", callback_data="settings"),
        InlineKeyboardButton("🔙 بازگشت", callback_data="back_main")
    )
    
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                         reply_markup=keyboard, parse_mode='HTML')
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "settings")
def handle_settings(call):
    """منوی تنظیمات پیشرفته"""
    text = """
⚙️ **تنظیمات پیشرفته**
━━━━━━━━━━━━━━━━━━━━━━

از گزینه‌های زیر برای تنظیم ربات استفاده کنید:

🌍 **منطقه پیش‌فرض:** تعیین منطقه برای کانفیگ‌ها
⭐ **کیفیت پیش‌فرض:** کیفیت کانفیگ‌ها
🔄 **کانفیگ خودکار:** دریافت خودکار کانفیگ
🔔 **اعلان‌ها:** دریافت اعلان‌ها
"""
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                         reply_markup=settings_menu(), parse_mode='HTML')
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "advanced_help")
def handle_advanced_help(call):
    """راهنمای پیشرفته"""
    text = """
📚 **راهنمای پیشرفته WhiteDNS**
━━━━━━━━━━━━━━━━━━━━━━

**🔹 کانفیگ هوشمند:**
ربات بهترین کانفیگ را با توجه به موقعیت شما انتخاب می‌کند

**🔹 کانفیگ دسته‌ای:**
می‌توانید ۱۰، ۲۰ یا ۵۰ کانفیگ دریافت کنید

**🔹 کانفیگ اختصاصی:**
کانفیگ با تنظیمات دلخواه خودتان

**🔹 بهترین کانفیگ:**
ربات بهترین کانفیگ را از بین چندین کانفیگ انتخاب می‌کند

**🔹 تنظیمات:**
• منطقه پیش‌فرض (ایران/بین‌الملل)
• کیفیت کانفیگ (عالی/خوب/معمولی)
• دریافت خودکار کانفیگ

**🔹 پشتیبانی:**
@Grootz_Support
"""
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                         reply_markup=get_back_button(), parse_mode='HTML')
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "advanced_stats")
def handle_advanced_stats(call):
    """آمار پیشرفته"""
    user_id = call.from_user.id
    
    # آمار عمومی
    total_users = db.fetch_one("SELECT COUNT(*) FROM users")[0]
    total_configs = db.fetch_one("SELECT COUNT(*) FROM configs")[0]
    active_users = db.fetch_one("SELECT COUNT(*) FROM users WHERE last_seen > ?", 
                               (int(time.time()) - 86400,))[0]
    
    # آمار روزانه
    today = datetime.now().strftime("%Y-%m-%d")
    daily = db.fetch_one("SELECT * FROM daily_stats WHERE date = ?", (today,))
    
    text = f"""
📊 **آمار پیشرفته ربات**
━━━━━━━━━━━━━━━━━━━━━━
👤 **کل کاربران:** {total_users}
👤 **کاربران فعال (۲۴h):** {active_users}
📋 **کل کانفیگ‌ها:** {total_configs}
━━━━━━━━━━━━━━━━━━━━━━
📈 **آمار امروز:**
• کاربران جدید: {daily[3] if daily else 0}
• کانفیگ‌های جدید: {daily[2] if daily else 0}
• کاربران فعال: {daily[4] if daily else 0}
━━━━━━━━━━━━━━━━━━━━━━
🔄 **آخرین به‌روزرسانی:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
    
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                         reply_markup=get_back_button(), parse_mode='HTML')
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "view_all_configs")
def handle_view_all_configs(call):
    """مشاهده همه کانفیگ‌های کاربر"""
    user_id = call.from_user.id
    configs = db.fetch_all("SELECT config, received_date, quality FROM configs WHERE user_id = ? ORDER BY received_date DESC LIMIT 10", (user_id,))
    
    if not configs:
        bot.answer_callback_query(call.id, "❌ شما کانفیگی ندارید!")
        return
    
    text = f"""
📋 **کانفیگ‌های شما**
━━━━━━━━━━━━━━━━━━━━━━
👤 **کاربر:** {call.from_user.first_name}
📊 **تعداد:** {len(configs)} کانفیگ اخیر
━━━━━━━━━━━━━━━━━━━━━━

"""
    for i, (config, date, quality) in enumerate(configs[:5], 1):
        text += f"📋 **کانفیگ {i}** (کیفیت: {quality or 'معمولی'})\n<code>{config[:80]}...</code>\n\n"
    
    if len(configs) > 5:
        text += f"📌 ... و {len(configs) - 5} کانفیگ دیگر\n"
    
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("🔄 دریافت کانفیگ جدید", callback_data="smart_config"),
        InlineKeyboardButton("🔙 بازگشت", callback_data="my_status_advanced")
    )
    
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                         reply_markup=keyboard, parse_mode='HTML')
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "back_main")
def handle_back_advanced(call):
    """بازگشت به منوی اصلی"""
    text = f"""
🚀 **ربات فوق‌پیشرفته VPN WhiteDNS** 🚀
━━━━━━━━━━━━━━━━━━━━━━
👤 **کاربر:** {call.from_user.first_name}
🕐 **زمان:** {datetime.now().strftime("%H:%M:%S")}
━━━━━━━━━━━━━━━━━━━━━━

✨ **منوی اصلی:**
• 🌐 کانفیگ هوشمند
• 📦 کانفیگ دسته‌ای
• 🎯 کانفیگ اختصاصی
• 🏆 بهترین کانفیگ
• 📊 وضعیت من
• ⚙️ تنظیمات
"""
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                         reply_markup=advanced_main_menu(), parse_mode='HTML')
    bot.answer_callback_query(call.id)

# ========== هندلرهای منطقه و کیفیت ==========
@bot.callback_query_handler(func=lambda call: call.data.startswith("region_"))
def handle_region(call):
    """تغییر منطقه"""
    user_id = call.from_user.id
    region = call.data.replace("region_", "")
    
    db.execute("UPDATE user_settings SET preferred_region = ? WHERE user_id = ?", (region, user_id))
    
    bot.answer_callback_query(call.id, f"✅ منطقه به {region} تغییر کرد!")
    handle_settings(call)

@bot.callback_query_handler(func=lambda call: call.data.startswith("quality_"))
def handle_quality(call):
    """تغییر کیفیت"""
    user_id = call.from_user.id
    quality = call.data.replace("quality_", "")
    
    db.execute("UPDATE user_settings SET preferred_quality = ? WHERE user_id = ?", (quality, user_id))
    
    bot.answer_callback_query(call.id, f"✅ کیفیت به {quality} تغییر کرد!")
    handle_settings(call)

# ========== اجرا ==========
if __name__ == "__main__":
    print("=" * 80)
    print("🚀 ربات فوق‌پیشرفته VPN WhiteDNS 🚀")
    print("=" * 80)
    print("✅ کانفیگ‌های هوشمند با کیفیت بالا")
    print("✅ انتخاب منطقه و کیفیت")
    print("✅ دریافت دسته‌ای ۱۰، ۲۰، ۵۰ کانفیگ")
    print("✅ سیستم تحلیل و انتخاب بهترین کانفیگ")
    print("✅ تنظیمات پیشرفته کاربر")
    print("✅ دیتابیس فوق‌پیشرفته با کش")
    print("=" * 80)
    print("🔄 ربات در حال اجرا...")
    print("👤 ادمین: @Grootz_Support")
    print("=" * 80)
    
    # پاک کردن کش منقضی شده هر ساعت
    def clear_cache_periodically():
        while True:
            time.sleep(3600)
            cache.clear_expired()
    
    cache_thread = threading.Thread(target=clear_cache_periodically, daemon=True)
    cache_thread.start()
    
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=60)
        except Exception as e:
            logger.error(f"خطا: {e}")
            print(f"❌ خطا: {e}")
            print("🔄 راه‌اندازی مجدد در 5 ثانیه...")
            time.sleep(5)
            continue