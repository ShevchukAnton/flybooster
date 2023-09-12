import emoji


async def compile_message(books_list: list):
    msg = ''

    # For now send back only first five findings
    for book in books_list:
        links = ''
        for fmt, link in book.get('fmts').items():
            links += f"{emoji.emojize(':link:')} : [{fmt}]({link})\n            "

        msg += f"""
            {emoji.emojize(':books:')} : {book.get('book_name', 'Книга без назви')}
            {emoji.emojize(':memo:')} : {book.get('author', 'Автор не виявлен')}
            {links}
            -------------------------------------------------------
            """
    return msg
