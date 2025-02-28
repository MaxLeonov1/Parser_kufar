from aiogram.types import Message
from loader import router,cursor,con, scheduler
from aiogram import F

@router.message(F.text == 'Удалить ссылку')
async def input_url(message: Message):
    user_id = message.from_user.id
    cursor.execute("SELECT * FROM users WHERE id=(?)",(user_id,))
    data_user = cursor.fetchall()
    if len(data_user)==0:
        await message.answer(text='У вас нет добавленной ссылки')
        return

    scheduler.remove_job(data_user[0][2])
    cursor.execute("DELETE FROM users WHERE id=(?)",(user_id,))
    con.commit()
    await message.answer('URL удален')