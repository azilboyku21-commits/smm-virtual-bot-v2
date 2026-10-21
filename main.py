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

# 2. Asosiy Asosiy Menyu (Pastki tugmalar)
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📁 Xizmatlar"), KeyboardButton(text="📞 Nomer Olish")],
        [KeyboardButton(text="🛒 Buyurtmalarim"), KeyboardButton(text="🫂 Pul ishlash")],
        [KeyboardButton(text="💰 Mening hisobim"), KeyboardButton(text="💵 Hisob to'ldirish")],
        [KeyboardButton(text="📩 Yordam"), KeyboardButton(text="☎️ Qo'llab-quvvatlash")],
        [KeyboardButton(text="💠 Hamkorlik")]
    ],
    resize_keyboard=True
)

# 3. Inline Menyu ("📁 Xizmatlar" bosilganda chiqadi)
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

# 4. Bot va Dispatcher
TOKEN = os.environ.get("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

# /start bosilganda
@dp.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer(
        "Assalomu alaykum! Botimizga xush kelibsiz.",
        reply_markup=main_menu
    )

# "📁 Xizmatlar" bosilganda
@dp.message(F.text == "📁 Xizmatlar")
async def show_services(message: Message):
    await message.answer(
        "✅ Xizmatlarimizni tanlaganingizdan xursandmiz!\n👇 Ijtimoiy tarmoqlardan birini tanlang.",
        reply_markup=services_inline_menu
    )

# "📞 Nomer Olish" va boshqa menyu tugmalari uchun umumiy handler
@dp.message(F.text.in_({
    "📞 Nomer Olish", "🛒 Buyurtmalarim", "🫂 Pul ishlash", 
    "💰 Mening hisobim", "💵 Hisob to'ldirish", "📩 Yordam", 
    "☎️ Qo'llab-quvvatlash", "💠 Hamkorlik"
}))
async def handle_main_buttons(message: Message):
    await message.answer(f"Siz **{message.text}** bo'limini tanladingiz.\n\n⚙️ Bu bo'lim tez orada to'liq sozlanadi!")

# Inline tugmalar (Telegram, Instagram va h.k.) bosilganda
@dp.callback_query(F.data.startswith("serv_"))
async def handle_services_callback(call: CallbackQuery):
    await call.answer()
    await call.message.answer(f"Siz xizmat turini tanladingiz!\n\n⚙️ Tez orada bu yerga o'zingiz xizmatlar va narxlarni qo'shishingiz mumkin.")

async def main():
    logging.basicConfig(level=logging.INFO)
    await start_dummy_server()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

