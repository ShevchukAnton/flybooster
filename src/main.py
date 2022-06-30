import logging
import os

import emoji
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message
from aiogram import Bot, Dispatcher
from aiogram.utils import executor
from dotenv import load_dotenv

from src import searcher, message_helper

load_dotenv()
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

token = os.getenv('TOKEN')

# Initialize bot and dispatcher
bot = Bot(token=token)
dp = Dispatcher(bot)

all_books = []


@dp.message_handler(commands=['start'])
async def start_handler(message: Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    user = message.from_user.username
    if user is None:
        user = message.from_user.full_name
    await message.reply(f"Ку-ку {user}!\nЯ поисковый бот для книг!\nЧто изволите искать?")


@dp.message_handler(regexp='^\w+|^\d+')
async def echo(message: Message):
    logging.info(f'User {message.from_user.username} - {message.from_user.full_name} requested for {message.text}')

    starting_search_msg = f"Приступаем к скурпулёзному поиску {emoji.emojize(':flashlight:')}"
    await message.answer(starting_search_msg, parse_mode='Markdown')

    search_results = await searcher.find(message.text)
    if len(search_results['books']) == 0:
        ans = f"{emoji.emojize(':disappointed_face:')} Мы не смогли ничего найти по запросу: \"***{message.text}***\""
    else:
        ans = await create_a_message(search_results['books'])

    if len(all_books) > 0:
        txt = 'Показать ещё 5' if len(all_books) > 5 else f'Показать {len(all_books)}'

        inline_button = InlineKeyboardButton(txt, callback_data='show_more')
        inline_markup = InlineKeyboardMarkup().add(inline_button)

        await message.answer(ans.replace('_', ' '), parse_mode='Markdown', reply_markup=inline_markup)
    else:
        await message.answer(ans.replace('_', ' '), parse_mode='Markdown')


@dp.callback_query_handler(lambda cb: cb.data == 'show_more')
async def show_more_books(callback_query: CallbackQuery):
    global all_books
    await bot.answer_callback_query(callback_query.id)
    loading_more_books_msg = f'Перерываем архив поиска {emoji.emojize(":zzz:")}'

    await bot.send_message(callback_query.from_user.id, loading_more_books_msg, parse_mode='Markdown')

    msg = await create_a_message(all_books)

    if len(all_books) > 0:
        txt = 'Показать ещё 5' if len(all_books) > 5 else f'Показать {len(all_books)}'

        inline_button = InlineKeyboardButton(txt, callback_data='show_more')
        inline_markup = InlineKeyboardMarkup().add(inline_button)

        await bot.send_message(callback_query.from_user.id, msg.replace('_', ' '), parse_mode='Markdown', reply_markup=inline_markup)
    else:
        await bot.send_message(callback_query.from_user.id, msg.replace('_', ' '), parse_mode='Markdown')


async def create_a_message(content, limit=5):
    global all_books
    books_amount = len(content)
    ans = f'Книг найдено: ***{books_amount}***\n'

    books = await searcher.find_downloadable_formats(content[:limit])

    if limit is not None and books_amount > limit:
        all_books = content
        ans = f'Книг найдено: ***{books_amount}*** (первые {limit} будут показаны):\n'

    ans += await message_helper.compile_message(books)

    all_books = [book for book in all_books if book not in books]

    return ans


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
