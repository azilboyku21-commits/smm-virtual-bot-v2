import asyncio
import logging
import os
from aiohttp import web
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

# Sizning Admin ID raqamingiz
ADMIN_ID = 8544987474

# 1. Render uchun soxta veb-server (Port xatosini oldini oladi)
async def handle(request):
    return web.Response(text="Bot is running!")

async def start_dummy_server():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

# 2. Oddiy foydalanuvchilar uchun Asosiy Menyu
user_main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📁 Buyurtma berish")],
        [KeyboardButton(text="📊 Buyurtmalar"), KeyboardButton(text="💰 Mening hisobim")],
        [KeyboardButton(text="🗣 Referal tizimi"), KeyboardButton(text="💵 Hisob to'ldirish")],
        [KeyboardButton(text="☎️ Murojaat"), KeyboardButton(text="📖 Qo'llanma")],
        [KeyboardButton(text="🤝 Hamkorlik tizimi")]
    ],
    resize_keyboard=True
)

# 3. Admin uchun Asosiy Menyu ("🗄 Boshqaruv" tugmasi bilan)
admin_main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📁 Buyurtma berish")],
        [KeyboardButton(text="📊 Buyurtmalar"), KeyboardButton(text="💰 Mening hisobim")],
        [KeyboardButton(text="🗣 Referal tizimi"), KeyboardButton(text="💵 Hisob to'ldirish")],
        [KeyboardButton(text="☎️ Murojaat"), KeyboardButton(text="📖 Qo'llanma")],
        [KeyboardButton(text="🤝 Hamkorlik tizimi")],
        [KeyboardButton(text="🗄 Boshqaruv")]
    ],
    resize_keyboard=True
)

# 4. Boshqaruv (Admin Panel) menyusi
admin_control_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🔑 Nakrutka API", callback_data="ctrl_nakrutka"),
            InlineKeyboardButton(text="⭐ Stars va Premium", callback_data="ctrl_stars")
        ],
        [
            InlineKeyboardButton(text="📱 Raqam API", callback_data="ctrl_raqam"),
            InlineKeyboardButton(text="🎁 Gift", callback_data="ctrl_gift")
        ],
        [
            InlineKeyboardButton(text="🛒 Buyurtmalar", callback_data="ctrl_orders"),
            InlineKeyboardButton(text="👥 Foydalanuvchilar", callback_data="ctrl_users")
        ],
        [
            InlineKeyboardButton(text="💳 To'lov tizimlar", callback_data="ctrl_payments"),
            InlineKeyboardButton(text="🎟 Promokod", callback_data="ctrl_promo")
        ],
        [
            InlineKeyboardButton(text="📩 Xabar yuborish", callback_data="ctrl_send"),
            InlineKeyboardButton(text="📢 Majburiy obuna", callback_data="ctrl_sub")
        ],
        [
            InlineKeyboardButton(text="🔔 Bildirishnomalar", callback_data="ctrl_notif"),
            InlineKeyboardButton(text="📊 Statistika", callback_data="ctrl_stats")
        ],
        [
            InlineKeyboardButton(text="⚙️ Sozlamalar", callback_data="ctrl_settings"),
            InlineKeyboardButton(text="🎨 Dizayn", callback_data="ctrl_design")
        ],
        [
            InlineKeyboardButton(text="📖 Qo'llanma", callback_data="ctrl_guide"),
            InlineKeyboardButton(text="👮‍♂️ Adminlar", callback_data="ctrl_admins")
        ],
        [
            InlineKeyboardButton(text="🌐 Web Panel", callback_data="ctrl_web")
        ],
        [
            InlineKeyboardButton(text="⏪ Orqaga", callback_data="ctrl_back")
        ]
    ]
)

TOKEN = os.environ.get("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_cmd(message: Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer(
            "Assalomu alaykum Boss! Boshqaruv paneliga xush kelibsiz.",
            reply_markup=admin_main_menu
        )
    else:
        await message.answer(
            "Assalomu alaykum! Botimizga xush kelibsiz

