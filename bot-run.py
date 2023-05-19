from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Update
import os
from lms.bot import (
    start,
)


BOT_TOKEN = os.environ.get('BOT_TOKEN')


def main():
    updater = Updater(token=BOT_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))

    
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
