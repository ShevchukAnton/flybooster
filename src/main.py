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
    await message.reply(f"Hi {user}!\nI'm SearchBot!\nWhat do you want to search?")


@dp.message_handler(regexp='^\w+|^\d+')
async def echo(message: types.Message):
    search_results = await searcher.find(message.text)
    ans = 'Results:\n'
    # For now send back only first five findings
    for result in search_results['books'][:5]:
        ans += f"""
        {emoji.emojize(':books:')} : {result['book_name']}
        {emoji.emojize(':man:')} : {result['author']}
        {emoji.emojize(':link:')} : {result['book_link']}
        ------------------------------------------------------------
        """
    await message.answer(ans)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
