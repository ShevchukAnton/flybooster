import sys
sys.path.append('.')

from src import searcher, message_helper
from dotenv import load_dotenv
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from aiogram import Bot, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message
import emoji
import logging
import os


load_dotenv()
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

token = os.getenv('TOKEN')

# Initialize bot and dispatcher
storage = MemoryStorage()
bot = Bot(token=token)
dp = Dispatcher(bot, storage=storage)


class Name_request(StatesGroup):
    query = State()

class Author_request(StatesGroup):
    query = State()


all_books = []
starting_search_msg = f"Починаємо ретельний пошук {emoji.emojize(':flashlight:')}"


@dp.message_handler(commands=['start'])
async def start_handler(message: Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    global all_books
    all_books.clear()
    user = message.from_user.username
    if user is None:
        user = message.from_user.full_name
    await message.reply(f"Вітаю {user}!\nЯ пошуковий бот для книг!\n/name - пошук аз назвою \n/author - пошук за автором \n/genre - пошук за жанром \n/series - пошук за серією")


@dp.message_handler(commands=['name'])
async def echo(message: Message):
    global all_books
    all_books.clear()
    search_question = 'Введіть назву книги або частину назви'
    await Name_request.query.set()
    await message.answer(search_question)


@dp.message_handler(commands=['author'])
async def search_by_author(message: Message):
    global all_books
    all_books.clear()
    search_question = 'Введіть П.І.Б автора або якусь частину з них'
    await Author_request.query.set()
    await message.answer(search_question)


@dp.message_handler(commands=['genre'])
async def echo(message: Message):
    global all_books
    all_books.clear()
    search_question = 'Введіть бажаний жанр'
    await Name_request.query.set()
    await message.answer(search_question)


@dp.message_handler(commands=['series'])
async def echo(message: Message):
    global all_books
    all_books.clear()
    search_question = 'Введіть назву серії або частину назви'
    await Name_request.query.set()
    await message.answer(search_question)


@dp.message_handler(state=Name_request.query)
async def query_handler(message: Message, state: FSMContext):
    await state.finish()

    logging.info(
        f'User {message.from_user.username} - {message.from_user.full_name} requested for {message.text}')

    await message.answer(starting_search_msg, parse_mode='Markdown')

    search_results = await searcher.search_by_name(message.text)
    if len(search_results['books']) == 0:
        ans = f"{emoji.emojize(':man_shrugging:')} Вибачайте, ми не знайшли нічого за запитом: \"***{message.text}***\""
    else:
        ans = await create_a_message(search_results['books'])

    if len(all_books) > 0:
        txt = 'Показати ще 5' if len(all_books) > 5 else f'Показати {len(all_books)}'

        inline_button = InlineKeyboardButton(txt, callback_data='show_more')
        inline_markup = InlineKeyboardMarkup().add(inline_button)

        await message.answer(ans.replace('_', ' '), parse_mode='Markdown', reply_markup=inline_markup)
    else:
        await message.answer(ans.replace('_', ' '), parse_mode='Markdown')


@dp.message_handler(state=Author_request.query)
async def query_handler(message: Message, state: FSMContext):
    await state.finish()

    logging.info(f'User {message.from_user.username} - {message.from_user.full_name} requested for {message.text}')

    await message.answer(starting_search_msg, parse_mode='Markdown')

    search_results = await searcher.search_by_author(message.text)
    if len(search_results['authors']) == 0:
        ans = f"{emoji.emojize(':man_shrugging:')} Вибачайте, ми не знайшли нічого за запитом: \"***{message.text}***\""
    else:
        ans = await create_a_message(search_results['authors'])

    if len(all_books) > 0:
        txt = 'Показати ще 5' if len(all_books) > 5 else f'Показати {len(all_books)}'

        inline_button = InlineKeyboardButton(txt, callback_data='show_more')
        inline_markup = InlineKeyboardMarkup().add(inline_button)

        await message.answer(ans.replace('_', ' '), parse_mode='Markdown', reply_markup=inline_markup)
    else:
        await message.answer(ans.replace('_', ' '), parse_mode='Markdown')


@dp.callback_query_handler(lambda cb: cb.data == 'show_more')
async def show_more_books(callback_query: CallbackQuery):
    global all_books
    await bot.answer_callback_query(callback_query.id)
    loading_more_books_msg = f'Шукаємо в архіві {emoji.emojize(":zzz:")}'

    await bot.send_message(callback_query.from_user.id, loading_more_books_msg, parse_mode='Markdown')

    msg = await create_a_message(all_books)

    if len(all_books) > 0:
        txt = 'Показати ще 5' if len(all_books) > 5 else f'Показати {len(all_books)}'

        inline_button = InlineKeyboardButton(txt, callback_data='show_more')
        inline_markup = InlineKeyboardMarkup().add(inline_button)

        await bot.send_message(callback_query.from_user.id, msg.replace('_', ' '), parse_mode='Markdown', reply_markup=inline_markup)
    else:
        await bot.send_message(callback_query.from_user.id, msg.replace('_', ' '), parse_mode='Markdown')


async def create_a_message(content, limit=5):
    global all_books
    books_amount = len(content)
    ans = f'Книг знайдено: ***{books_amount}***\n'

    books = await searcher.find_downloadable_formats(content[:limit])

    if limit is not None and books_amount > limit:
        all_books = content
        ans = f'Книг знайдено: ***{books_amount}*** (перші {limit} відображені):\n'

    ans += await message_helper.compile_message(books)

    all_books = [book for book in all_books if book not in books]

    return ans


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
