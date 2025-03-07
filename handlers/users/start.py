from aiogram.filters import Command
from aiogram.types import Message
from loader import router, cursor, con
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from keys.key import kb_start

@router.message(Command('start'))
async def start(message: Message):
    info_source = message.text.split(' ')
    user_id = message.from_user.id
    cursor.execute("SELECT id FROM users")
    users_id = cursor.fetchall()[0]
    print(users_id,user_id)
    if len(info_source) >1:
        tok = info_source[1]
    cursor.execute("SELECT * FROM stats WHERE token=(?)",(tok,))
    st_data = cursor.fetchall()
    if st_data and (user_id in users_id):
        cursor.execute("UPDATE stats SET counter = counter + 1 WHERE token=(?)",(tok,))
        con.commit()
    builder = ReplyKeyboardBuilder()
    for button in kb_start:
        builder.add(button)
    builder.adjust(1)
    await message.answer(text='Добро пожаловать',reply_markup=builder.as_markup(resize_keyboard = True))