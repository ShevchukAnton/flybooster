#!/usr/bin/env python

import logging
import os

from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

load_dotenv()
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

token = os.getenv('TOKEN')
updater = Updater(token=token)
dispatcher = updater.dispatcher


def start(update, context):
    """
    /start command handler
    :param update:
    :param context:
    :return:
    """
    context.bot.send_message(chat_id=update.effective_chat.id, text="What do you want to search?")


# TODO add search usage here
def read_input(update, context):
    """
    Reads regular user's input
    :param update: This module contains an object that represents a Telegram Update
    :param context:
    :return: modified message
    """
    answer = f'Agreed that {update.message.text}'
    context.bot.send_message(chat_id=update.effective_chat.id, text=answer)


# Actually handlers
regular_message_handler = MessageHandler(Filters.text & (~Filters.command), read_input)
start_handler = CommandHandler('start', start)

# All registered handlers will be here
dispatcher.add_handler(start_handler)
dispatcher.add_handler(regular_message_handler)

# The BEGINNING
updater.start_polling()
