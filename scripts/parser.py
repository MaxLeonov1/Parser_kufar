from http.client import responses

import requests
from aiogram.types import WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardBuilder
from bs4 import BeautifulSoup
from pydantic.v1.datetime_parse import parse_date

from loader import cursor, Bot
import json
from aiogram import types

def parse_website(url, class_names, inner_class_name):
    response = requests.get(url)
    if response.status_code != 200:
        print(f'Ошибка запроса: {response.status_code}')
        return None
    soup = BeautifulSoup(response.text,'html.parser')
    parsed_date = []
    elements = soup.find_all(class_=class_names)

    for element in elements:
        text = element.get_text(strip=True)

        img_tag = element.find('img')
        img_url = img_tag['src'] if img_tag and 'src' in img_tag.attrs else None

        inner_element = element.find(class_=inner_class_name)
        inner_text = inner_element.get_text(strip=True) if inner_element else None

        link_url = element.get('href') if element.has_attr('href') else None
        link_url = link_url.split('?')[0]

        parsed_date.append([text, img_url, inner_text, link_url])

    return parsed_date




async def parser_update(user_id, bot: Bot):
    cursor.execute("SELECT * FROM users WHERE id=(?)", (user_id,))
    data_user = cursor.fetchall()
    url = data_user[0][1]
    id_task = data_user[0][2]

    class_name = "styles_wrapper__5FoK7"
    inner_class_name = "styles_secondary__MzdEb"
    result = parse_website(url, class_name, inner_class_name)[:5]
    print(result)

    with open(f'data/{user_id}.json','r',encoding='utf-8') as file:
        old_results= json.loads(file.read())

    new_results = []

    for result_new in result:
        index = old_results.index(result_new)
        if len(index) == 0:
            new_results.append(result_new)

    if len(new_results) != 0:
        with open(f'data/{user_id}.json', 'w', encoding='utf-8') as results:
            results.write(json.dumps(result))

        for mess in new_results:
            builder = InlineKeyboardBuilder()
            builder.add(types.InlineKeyboardButton(text='открыть объявление',
                                                   web_app=WebAppInfo(url=mess[3])))
            await bot.send_photo(caption=f'{mess[0]}\n{mess[2]}',
                                 chat_id=user_id,
                                 photo=mess[1],
                                 reply_markup=builder.as_markup(resize_keyboard=True))

