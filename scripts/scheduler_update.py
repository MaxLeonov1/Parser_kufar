from loader import router, cursor, con, scheduler, bot
from scripts.parser import parser_update

def update_scheduler():
    cursor.execute('SELECT * FROM users')
    data = cursor.fetchall()
    for user in data:
        user_id = user[0]
        task = scheduler.add_job(parser_update,
                                 trigger='interval',
                                 seconds=60,
                                 kwargs={'user_id': user_id, 'bot': bot})
        cursor.execute('UPDATE users SET id_task=(?) WHERE id=(?)', (str(task.id),user_id))
        con.commit()