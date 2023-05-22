from telegram.ext import Updater
import os
from lms.handler import main
from settings import TOKEN

if __name__ == '__main__':

    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher

    dispatcher = main(dispatcher)

    updater.start_polling()
    updater.idle()