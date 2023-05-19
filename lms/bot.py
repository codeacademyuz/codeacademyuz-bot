from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import Update

welcome_text = """
Assalomu alaykum, {first_name}\!

*CODEACADEMY* dasturchilar maktabi botiga xush kelibsiz\!

Kelejak kasbini o'rganmoqchi bo'lsangiz bizga qo'shiling\!

*📱 Telegram:* @codeacademyai
*📞 Telefon:* \+998 95 012 77 33
"""

def start(update: Update, context: CallbackContext):
    update.message.reply_markdown_v2(welcome_text.format(first_name=update.effective_user.first_name))
