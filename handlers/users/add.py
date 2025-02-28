from aiogram.types import Message
from aiogram import types
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from loader import router, cursor, con, scheduler, bot
from aiogram import F
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from keys.key import kb_start
from scripts.parser import parser_update, parse_website
import json

class FormUrl(StatesGroup):
    url = State()

@router.message(F.text == 'Добавить ссылку')
async def input_url(message: Message, state: FSMContext):
    user_id = message.from_user.id
    cursor.execute("SELECT * FROM users WHERE id=(?)",(user_id,))
    if len(cursor.fetchall())>0:
        await message.answer(text='Ссылка уже добавлена')
        return
    await state.set_state((FormUrl.url))
    await message.answer('Введите URL',reply_markup=types.ReplyKeyboardRemove())

@router.message(FormUrl.url)
async def get_url(message: Message, state: FSMContext):
    await state.update_data(url=message.text)
    data = await state.get_data()
    url = data['url']
    user_id = str(message.chat.id)
    await state.clear()
    task = scheduler.add_job(parser_update,
                             trigger='interval',
                             seconds=60,
                             kwargs={'user_id': user_id, 'bot': bot})
    cursor.execute("INSERT INTO users (id,url,id_task) VALUES (?,?,?)",(user_id,url,str(task.id)))
    con.commit()

    class_name = "styles_wrapper__5FoK7"
    inner_class_name = "styles_secondary__MzdEb"
    result = parse_website(data['url'], class_name, inner_class_name)[:5]
    with open(f'data/{user_id}.json','w',encoding='utf-8') as file:
        file.write(json.dumps(result))

    builder = ReplyKeyboardBuilder()
    for button in kb_start:
        builder.add(button)
    builder.adjust(1)
    await message.answer(text='URL добавлен', reply_markup=builder.as_markup(resize_keyboard=True))