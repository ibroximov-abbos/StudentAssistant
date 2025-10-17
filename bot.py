import asyncio
import logging
import sys
import django
from aiogram import Bot, Dispatcher, html, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from asgiref.sync import sync_to_async
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import CallbackQuery
from aiogram.types import FSInputFile

from removeFile import removeFile
from  file_generator.gemini_api import ai_request

from dotenv import load_dotenv
import os
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from assistant.models import Student

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

TOKEN = BOT_TOKEN

storage = MemoryStorage()
dp = Dispatcher(storage=storage) 
class Registration(StatesGroup):
    full_name = State()

class ToOrder(StatesGroup):
    subject = State()
    theme = State()
    doc_type = State()
    size = State()
class Result(StatesGroup):
    result = State()
    
def get_options_keyboard():
    buttons = [
        [InlineKeyboardButton(text="Word", callback_data="word"),
        InlineKeyboardButton(text="PowerPoint", callback_data="powerpoint")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    try:
        student = await sync_to_async(Student.objects.get)(
            username=message.from_user.username
        )
        await message.answer(f"Assalomu alaykum, {html.bold(student.full_name)}!")
        await state.update_data(full_name=student.full_name)
        await message.answer('Qaysi fandan referat yoki prezentatsiya xoxlaysiz?')
        await state.set_state(ToOrder.subject)
        
    except Student.DoesNotExist:
        await message.answer(
            "Assalomu alaykum!\n"
            "Iltimos familiya va ismingizni kiriting.\n"
            "Masalan: Aliyev Vali"
        )
        await state.set_state(Registration.full_name)

@dp.message(Registration.full_name)
async def process_name(message: Message, state: FSMContext):
    full_name = message.text.strip()    
    try:
        await sync_to_async(Student.objects.create)(
            username=message.from_user.username,
            full_name=full_name
        )
        
        await state.clear()
        logger.info(f"User {message.from_user.id} registered: {full_name}")
        await message.answer('Qaysi fandan referat yoki prezentatsiya xoxlaysiz?')
        await state.set_state(ToOrder.subject)
        
    except Exception as e:
        logger.error(f"Error: {e}")
        await message.answer("Xatolik yuz berdi!")
        await state.clear()


@dp.message(ToOrder.subject)
async def get_subject(message: Message, state: FSMContext):
    subject = message.text.strip()
    await state.update_data(subject=subject)
    await message.answer("Qaysi mavzu bo'yicha?")
    await state.set_state(ToOrder.theme)

@dp.message(ToOrder.theme)
async def get_subject(message: Message, state: FSMContext):
    theme = message.text.strip()
    await state.update_data(theme=theme)
    await message.answer("Hujjat qaysi formatda bo'lsin? Quyidagilardan birini tanlang:", reply_markup=get_options_keyboard())
    await state.set_state(ToOrder.doc_type)

@dp.callback_query(F.data, ToOrder.doc_type)
async def option_handler(callback: CallbackQuery, state: FSMContext):
    doc_type = callback.data
    await state.update_data(doc_type=doc_type)
    await callback.message.edit_reply_markup()
    await callback.message.answer(doc_type)
    await callback.message.answer("Hajmini 5-20 diapazonda kiriting(masalan: 10).")
    await state.set_state(ToOrder.size)

@dp.message(ToOrder.size)
async def get_subject(message: Message, state: FSMContext):
    size = message.text
    username = message.from_user.username
    if size.isdigit(): 
        size = int(size)
        if 5 <= size <= 20:
            await state.update_data(size=size)
            state_data = await state.get_data()
            data = {
                'full_name': state_data.get('full_name'),
                'username': username,
                'subject': state_data.get('subject'),
                'theme': state_data.get('theme'),
                'doc_type': state_data.get('doc_type'),
                'size': state_data.get('size')
            }
            await message.answer('File tayyorlanmoqda...')
            result = ai_request(data)
            if result == 'ok' and data['doc_type'] == 'word':
                file_path = f"{data['username']}.docx"
                document = FSInputFile(file_path)
                await message.answer_document(document, caption="Refaratingiz tayyor!")
                removeFile(file_path)

            elif result == 'ok' and data['doc_type'] == 'powerpoint':
                file_path = f"{data['username']}.pptx"
                document = FSInputFile(file_path)
                await message.answer_document(document, caption="Taqdimotingiz tayyor!")
                removeFile(file_path)
        else:
            await message.answer("Hujjat hajmi quyidagi diapazonda bo'lishi kerak: 5-20.")
            await state.set_state(ToOrder.size)
    else:
        await message.answer("Hujjat hajmi raqamlar bilan ko'rsatilishi kerak.")
        await state.set_state(ToOrder.size)


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    logger.info("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())