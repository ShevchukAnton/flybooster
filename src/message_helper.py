import emoji
from aiogram import types


async def compile_message(book):
    buttons = []
    for fmt, link in book.get('fmts').items():
        buttons.append(types.InlineKeyboardButton(text=fmt.upper(), callback_data=f'download**{link}'))

    msg = f"""
        {emoji.emojize(':books:')} : {book.get('book_name', 'Книга без назви')}
        {emoji.emojize(':memo:')} : {book.get('author', 'Автор не виявлен')}
        """.replace('_', ' ')

    return msg, buttons
