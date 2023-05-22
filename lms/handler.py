from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
from telegram import Update
import os
from .bot import (
    start,
    noneusername,
    registration,
    add_first_name,
    add_last_name,
    add_phone_number,
    add_region,
    add_school,
    finally_registration,
    info,
    all_users,
    send_url,
    send_message_all_users,
)

def main(dispatcher):

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('all_users', all_users))
    dispatcher.add_handler(CommandHandler("send_url", send_url))
    dispatcher.add_handler(CallbackQueryHandler(noneusername, pattern='noneusername'))
    dispatcher.add_handler(MessageHandler(Filters.text("👤 Info"), info))
    dispatcher.add_handler(MessageHandler(Filters.text, registration))

    return dispatcher