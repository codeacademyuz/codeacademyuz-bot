from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import Update
from .constants import messages

def start(update: Update, context: CallbackContext):
    username = update.effective_user.username
    if username == None:
        hi = messages.get('hi')
        msg = messages.get('username_none')
        start_msg = f"{hi}\n\n{msg}".format(first_name=update.effective_user.first_name)
        update.message.reply_markdown_v2(start_msg)
    
    else:
        hi = messages.get('hi')
        msg = messages.get('username_exists')
        start_msg = f"{hi}\n\n{msg}".format(first_name=update.effective_user.first_name)
        
        update.message.reply_markdown_v2(start_msg)
