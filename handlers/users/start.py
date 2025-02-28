from aiogram.filters import Command
from aiogram.types import Message
from loader import router, cursor, con
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from keys.key import kb_start

@router.message(Command('start'))
async def start(message: Message):
    builder = ReplyKeyboardBuilder()
    for button in kb_start:
        builder.add(button)
    builder.adjust(1)
    await message.answer(text='Добро пожаловать',reply_markup=builder.as_markup(resize_keyboard = True))