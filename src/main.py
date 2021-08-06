import logging
import os

import emoji
from aiogram import types, Bot, Dispatcher
from aiogram.utils import executor
from dotenv import load_dotenv

from src import searcher

load_dotenv()
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

token = os.getenv('TOKEN')

# Initialize bot and dispatcher
bot = Bot(token=token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    user = message.from_user.username
    if user is None:
        user = message.from_user.full_name
    await message.reply(f"Ку-ку {user}!\nЯ поисковый бот для книг!\nЧто изволите искать?")


@dp.message_handler(regexp='^\w+|^\d+')
async def echo(message: types.Message):
    logging.info(f'User {message.from_user.username} - {message.from_user.full_name} requested for {message.text}')
    search_results = await searcher.find(message.text)
    if len(search_results['books']) == 0:
        ans = f"{emoji.emojize(':disappointed_face:')} Мы не смогли нечго найти по запросу: \"***{message.text}***\""
    else:
        ans = await create_a_message(search_results)

    await message.answer(ans.replace('_', ' '), parse_mode='Markdown')


async def create_a_message(content):
    ans = f'Книг найдено: ***{len(content["books"])}*** (первые 5 будут показаны):\n'
    # For now send back only first five findings
    for result in content['books'][:5]:
        links = ''
        for link in result.get('fmts'):
            links += f'[{link.key}]({link.value})\t'

        ans += f"""
            {emoji.emojize(':books:')} : {result.get('book_name', 'Безымянная книга')}
            {emoji.emojize(':memo:')} : {result.get('author', 'Автор не установлен')}
            {emoji.emojize(':link:')} : {links}) 
            -------------------------------------------------------
            """
    return ans


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
