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
    cancel,
    finally_registration,
    info,
    all_users,
    send_url,
    send_message_all_users,
    cancel_lesson
)

def main(dispatcher):

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('all_users', all_users))
    dispatcher.add_handler(CallbackQueryHandler(noneusername, pattern='noneusername'))
    dispatcher.add_handler(MessageHandler(Filters.text("👤 Info"), info))
    dispatcher.add_handler(ConversationHandler(
        entry_points=[MessageHandler(Filters.text("Ro'yxatdan o'tish!"), registration)],
        states={
            0: [MessageHandler(Filters.text, add_first_name)],
            1: [MessageHandler(Filters.text, add_last_name)],
            2: [MessageHandler(Filters.text, add_phone_number)],
            3: [MessageHandler(Filters.text, add_region)],
            4: [MessageHandler(Filters.text, add_school)],
            5: [MessageHandler(Filters.text, finally_registration)]
            },

        fallbacks=[CommandHandler("cancel", cancel)]
    ))
    dispatcher.add_handler(ConversationHandler(
        entry_points=[CommandHandler("send_url", send_url)],
        states={
            0: [MessageHandler(Filters.text, send_message_all_users)]
            },

        fallbacks=[CommandHandler("cancel_lesson", cancel)]
    ))
    return dispatcher