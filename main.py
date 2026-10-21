import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🚀 SMM Xizmatlar", callback_data="smm")],
            [InlineKeyboardButton(text="📱 Virtual Raqam", callback_data="number")],
            [InlineKeyboardButton(text="⭐ Telegram Stars", callback_data="stars")],
            [InlineKeyboardButton(text="🔑 Shaxsiy API", callback_data="api")]
        ]
    )
    await message.answer("👋 Xush kelibsiz! Bo'limni tanlang:", reply_markup=keyboard)
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

