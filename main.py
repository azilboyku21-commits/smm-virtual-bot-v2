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

# Sizning Telegram ID raqamingiz
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
        [KeyboardButton(text="📁 Xizmatlar"), KeyboardButton(text="📞 Nomer Olish")],
        [KeyboardButton(text="🛒 Buyurtmalarim"), KeyboardButton(text="🫂 Pul ishlash")],
        [KeyboardButton(text="💰 Mening hisobim"), KeyboardButton(text="💵 Hisob to'ldirish")],
        [KeyboardButton(text="📩 Yordam"), KeyboardButton(text="☎️ Qo'llab-quvvatlash")],
        [KeyboardButton(text="💠 Hamkorlik")]
    ],
    resize_keyboard=True
)

# 3. Faqat SIZ (Admin) uchun Asosiy Menyu (Sozlamalar bilan)
admin_main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📁 Xizmatlar"), KeyboardButton(text="📞 Nomer Olish")],
        [KeyboardButton(text="🛒 Buyurtmalarim"), KeyboardButton(text="🫂 Pul ishlash")],
        [KeyboardButton(text="💰 Mening hisobim"), KeyboardButton(text="💵 Hisob to'ldirish")],
        [KeyboardButton(text="📩 Yordam"), KeyboardButton(text="☎️ Qo'llab-quvvatlash")],
        [KeyboardButton(text="💠 Hamkorlik"), KeyboardButton(text="⚙️ Sozlamalar (Admin)")]
    ],
    resize_keyboard=True
)

# 4. Admin Sozlamalar Menyusi (Inline)
admin_settings_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="➕ Xizmat qo'shish", callback_data="add_service"),
            InlineKeyboardButton(text="➕ Nomer qo'shish", callback_data="add_number")
        ],
        [
            InlineKeyboardButton(text="📊 Statistika", callback_data="admin_stats"),
            InlineKeyboardButton(text="📢 Xabar yuborish", callback_data="admin_broadcast")
        ]
    ]
)

# 5. Xizmatlar Menyusi
services_inline_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🔵 Telegram", callback_data="serv_telegram"),
            InlineKeyboardButton(text="🟣 Instagram", callback_data="serv_instagram")
        ],
        [
            InlineKeyboardButton(text="🖤 TikTok", callback_data="serv_tiktok"),
            InlineKeyboardButton(text="🔴 YouTube", callback_data="serv_youtube")
        ],
        [
            InlineKeyboardButton(text="⭐ Telegram [Stars-Premium-Gift]", callback_data="serv_stars")
        ],
        [
            InlineKeyboardButton(text="🔍 Qidirish", callback_data="serv_search"),
            InlineKeyboardButton(text="🛒 Barcha xizmatlar ↗️", callback_data="serv_all")
        ]
    ]
)

TOKEN = os.environ.get("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

# /start bosilganda
@dp.message(CommandStart())
async def start_cmd(message: Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer(
            "Assalomu alaykum Admin! Xush kelibsiz.",
            reply_markup=admin_main_menu
        )
    else:
        await message.answer(
            "Assalomu alaykum! Botimizga xush kelibsiz.",
            reply_markup=user_main_menu
        )

# "⚙️ Sozlamalar (Admin)" bosilganda
@dp.message(F.text == "⚙️ Sozlamalar (Admin)")
async def admin_panel(message: Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer(
            "🛠 **Admin boshqaruv paneli:**\n\nQuyidagi tugmalar orqali xizmatlar va nomerlar qo'shishni boshlashingiz mumkin:",
            reply_markup=admin_settings_menu,
            parse_mode="Markdown"
        )

# "📁 Xizmatlar" bosilganda
@dp.message(F.text == "📁 Xizmatlar")
async def show_services(message: Message):
    await message.answer(
        "✅ Xizmatlarimizni tanlaganingizdan xursandmiz!\n👇 Ijtimoiy tarmoqlardan birini tanlang.",
        reply_markup=services_inline_menu
    )

# Sozlamalar menyusidagi tugmalar ishlashi uchun
@dp.callback_query(F.data.in_({"add_service", "add_number", "admin_stats", "admin_broadcast"}))
async def admin_actions(call: CallbackQuery):
    if call.from_user.id == ADMIN_ID:
        await call.answer()
        if call.data == "add_service":
            await call.message.answer("➕ Yangi xizmat qo'shish uchun ma'lumotlarni yuboring (Masalan: Telegram ko'rishlar - 1000 ta = 5000 so'm)")
        elif call.data == "add_number":
            await call.message.answer("➕ Yangi davlat va nomer qo'shish uchun narxini kiriting...")
        elif call.data == "admin_stats":
            await call.message.answer("📊 Hozircha botda 1 ta foydalanuvchi bor.")
        elif call.data == "admin_broadcast":
            await call.message.answer("📢 Barcha foydalanuvchilarga yuboriladigan matnni kiriting...")

async def main():
    logging.basicConfig(level=logging.INFO)
    await start_dummy_server()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

