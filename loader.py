from aiogram import Bot, Dispatcher, Router
from aiohttp.web_routedef import route
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config.token import TOKEN
import sqlite3

con = sqlite3.connect("data/data.db")
cursor = con.cursor()

router = Router()
dp = Dispatcher()
dp.include_router(router)
bot = Bot(TOKEN)

scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
