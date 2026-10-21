import asyncio
import logging
import os
import sqlite3
from aiohttp import web
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton
)

ADMIN_ID = 8544987474

# ----------------- DB SETUP -----------------
def init_db():
    conn = sqlite3.connect("bot_database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS api_settings (
            service_type TEXT PRIMARY KEY,
            api_url TEXT,
            api_key TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            name TEXT,
            price REAL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ----------------- FSM STATES -----------------
class AddApiState(StatesGroup):
    waiting_for_url = State()
    waiting_for_key = State()

class AddServiceState(StatesGroup):
    waiting_for_category = State()
    waiting_for_name = State()
    waiting_for_price = State()

# ----------------- DUMMY SERVER -----------------
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

# ----------------- KEYBOARDS (PASTDAGI TUGMALAR) -----------------
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

# Admin bosganda pastda chiqadigan asosiy boshqaruv menyusi (siz xohlagandek)
admin_control_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔑 Nakrutka API"), KeyboardButton(text="📱 Raqam API")],
        [KeyboardButton(text="➕ Yangi Xizmat Qo'shish"), KeyboardButton(text="📋 Xizmatlar Ro'yxati")],
        [KeyboardButton(text="👥 Foydalanuvchilar"), KeyboardButton(text="📊 Statistika")],
        [KeyboardButton(text="🔙 Asosiy Menyu")]
    ],
    resize_keyboard=True
)

TOKEN = os.environ.get("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# ----------------- HANDLERS -----------------
@dp.message(CommandStart())
async def start_cmd(message: Message, state: FSMContext):
    await state.clear()
    if message.from_user.id == ADMIN_ID:
        await message.answer("Assalomu alaykum Boss! Boshqaruv paneliga xush kelibsiz.", reply_markup=admin_main_menu)
    else:
        await message.answer("Assalomu alaykum! Botimizga xush kelibsiz.", reply_markup=user_main_menu)

@dp.message(F.text == "🗄 Boshqaruv")
async def control_panel(message: Message, state: FSMContext):
    await state.clear()
    if message.from_user.id == ADMIN_ID:
        await message.answer("🎛 **Admin Boshqaruv Paneli**\n\nKerakli bo'limni pastdagi tugmalardan tanlang:", reply_markup=admin_control_menu, parse_mode="Markdown")
    else:
        await message.answer("Sizga bu bo'limga ruxsat yo'q.")

@dp.message(F.text == "🔙 Asosiy Menyu")
async def back_to_main(message: Message, state: FSMContext):
    await state.clear()
    if message.from_user.id == ADMIN_ID:
        await message.answer("Asosiy menyuga qaytdingiz.", reply_markup=admin_main_menu)
    else:
        await message.answer("Asosiy menyuga qaytdingiz.", reply_markup=user_main_menu)

@dp.message(F.text.in_({"🔑 Nakrutka API", "📱 Raqam API"}))
async def api_menu_click(message: Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        return
    service_type = message.text
    await state.update_data(current_api_type=service_type)
    await state.set_state(AddApiState.waiting_for_url)
    await message.answer(f"🌐 **{service_type}** uchun API URL (sayt manzili)ni kiriting:\n(Masalan: `https://provider.com/api/v2`)", parse_mode="Markdown")

@dp.message(F.text == "➕ Yangi Xizmat Qo'shish")
async def add_service_click(message: Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        return
    await state.set_state(AddServiceState.waiting_for_category)
    await message.answer("📁 Xizmat kategoriyasini kiriting:\n(Masalan: Telegram, Instagram, Virtual Raqam)")

@dp.message(F.text == "📋 Xizmatlar Ro'yxati")
async def list_services_click(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    conn = sqlite3.connect("bot_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, category, name, price FROM services")
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        await message.answer("📋 Hozircha hech qanday xizmat qo'shilmagan.")
    else:
        msg = "📋 **Mavjud Xizmatlar va Raqamlar:**\n\n"
        for row in rows:
            msg += f"🔹 **ID:** {row[0]} | **Kategoriya:** {row[1]}\n   **Nomi:** {row[2]} - {row[3]} so'm\n\n"
        await message.answer(msg, parse_mode="Markdown")

# ----- API QO'SHISH FSM -----
@dp.message(AddApiState.waiting_for_url)
async def process_api_url(message: Message, state: FSMContext):
    await state.update_data(api_url=message.text)
    await state.set_state(AddApiState.waiting_for_key)
    await message.answer("🔑 Endi API KEY (Kalit)ni kiriting:")

@dp.message(AddApiState.waiting_for_key)
async def process_api_key(message: Message, state: FSMContext):
    data = await state.get_data()
    api_type = data.get("current_api_type")
    api_url = data.get("api_url")
    api_key = message.text
    
    conn = sqlite3.connect("bot_database.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO api_settings (service_type, api_url, api_key)
        VALUES (?, ?, ?)
    """, (api_type, api_url, api_key))
    conn.commit()
    conn.close()
    
    await state.clear()
    await message.answer(f"✅ **{api_type}** muvaffaqiyatli saqlandi!\n\n🌐 **URL:** {api_url}\n🔑 **KEY:** {api_key}", parse_mode="admin_control_menu", reply_markup=admin_control_menu)

# ----- XIZMAT QO'SHISH FSM -----
@dp.message(AddServiceState.waiting_for_category)
async def process_service_category(message: Message, state: FSMContext):
    await state.update_data(category=message.text)
    await state.set_state(AddServiceState.waiting_for_name)
    await message.answer("📝 Xizmat yoki Raqam nomini kiriting:\n(Masalan: `Telegram Premium 1 Oylik` yoki `Uzbekistan (+998) Virtual Raqam`)", parse_mode="Markdown")

@dp.message(AddServiceState.waiting_for_name)
async def process_service_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddServiceState.waiting_for_price)
    await message.answer("💰 Xizmat narxini kiriting (faqat raqamda, masalan: `15000`):", parse_mode="Markdown")

@dp.message(AddServiceState.waiting_for_price)
async def process_service_price(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("⚠️ Iltimos, narxni faqat raqamda kiriting!")
        return
    
    data = await state.get_data()
    category = data.get("category")
    name = data.get("name")
    price = float(message.text)
    
    conn = sqlite3.connect("bot_database.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO services (category, name, price)
        VALUES (?, ?, ?)
    """, (category, name, price))
    conn.commit()
    conn.close()
    
    await state.clear()
    await message.answer(f"✅ **Xizmat qo'shildi!**\n\n📁 **Kategoriya:** {category}\n📝 **Nomi:** {name}\n💰 **Narxi:** {price} so'm", reply_markup=admin_control_menu, parse_mode="Markdown")

async def main():
    logging.basicConfig(level=logging.INFO)
    await start_dummy_server()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

