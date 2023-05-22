from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler, ConversationHandler
from telegram import Update, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, Video
from .constants import messages
from .db import Database
import re
users_db = Database()

def start(update: Update, context: CallbackContext):
    username = update.effective_user.username
    first_name = update.effective_user.first_name
    if username == None:
        hi = messages.get('hi').format(first_name=first_name)
        msg = messages.get('username_none')
        start_msg = f"{hi}\n\n{msg}"
        # create inline keyboard
        button = InlineKeyboardButton("Qo'llanma orqali username o'rnatish", callback_data="noneusername")
        keyboard = InlineKeyboardMarkup([[button]])
        update.message.reply_markdown_v2(start_msg, reply_markup=keyboard)
    
    else:
        hi = messages.get('hi')
        check_user = users_db.check_user(update.effective_chat.id)

        if check_user:
            start_msg = hi.format(first_name=first_name) + messages['registrated']
            button = KeyboardButton(text="👤 Info")
            keyboard = ReplyKeyboardMarkup([[button]], resize_keyboard=True)
            update.message.reply_markdown_v2(start_msg, reply_markup=keyboard)
        else:
            msg = messages.get('username_exists')
            start_msg = f"{hi}\n\n{msg}".format(first_name=update.effective_user.first_name)

            button = KeyboardButton(text="Ro'yxatdan o'tish!")
            keyboard = ReplyKeyboardMarkup([[button]], resize_keyboard=True)
            update.message.reply_markdown_v2(start_msg, reply_markup=keyboard)

def all_users(update: Update, context: CallbackContext):
    users_count = users_db.get_users()
    update.message.reply_html(f"Botdan ro'yxatdan o'tgan foydalanuvchilar soni: <b>{len(users_count)}</b>")

def send_message_all_users(update: Update, context: CallbackContext):
    users = users_db.get_users()
    text = update.message.text
    chat_id = update.effective_chat.id
    if chat_id == 1046157991 or chat_id == 715393503:
        for user in users:
            try:
                # create inline keyboard for sending url
                button = InlineKeyboardButton("Darsga o'tish", url=text)
                keyboard = InlineKeyboardMarkup([[button]])
                context.bot.send_message(chat_id=user['chat_id'], text="Darsga o'tish uchun quyidagi tugmani bosing:", reply_markup=keyboard)
            except:
                error_message = f"Xatolik yuz berdi: \n\Ismi: {user['first_name']}\nFamilyasi: {user['last_name']}\nUsername: {user['username']}\nMaktabi: {user['school']}\nViloyati: {user['region']}"
                context.bot.send_message(chat_id=chat_id, text=error_message)
        
        chat_id = update.effective_chat.id
        context.bot.send_message(chat_id=chat_id, text="Xabar yuborildi!")
    else:
        context.bot.send_message(chat_id=chat_id, text="Siz bu buyruqni bajarib bo'lmaysiz!")
    
def send_url(update: Update, context: CallbackContext):
    text = "Yuborish uchun URL manzilini kiriting:"
    update.message.reply_text(text)
    users_db.status_send_url = "sending_url"

def info(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user = users_db.get_user(chat_id)
    info_msg = messages['about'].format(
        first_name=user['first_name'],
        last_name=user['last_name'],
        username=user['username'],
        phone_number=user['phone_number'],
        region=user['region'],
        school=user['school']
    )
    update.message.reply_html(info_msg)

def noneusername(update: Update, context: CallbackContext):
    query = update.callback_query
    # send video through file id
    query.answer("Video yuklanmoqda...")
    query.edit_message_text(text="send cheat sheet video")

def add_first_name(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    text = update.message.text
    data = users_db.temp_user_data_get(chat_id)
    data['first_name'] = text
    users_db.temp_user_data_update(data, chat_id)
    update.message.reply_markdown_v2(messages['add_last_name'])

def add_last_name(update: Update, context: CallbackContext):
    text = update.message.text
    chat_id = update.effective_chat.id
    data = users_db.temp_user_data_get(chat_id)
    data['last_name'] = text
    data['username'] = update.effective_user.username
    data['chat_id'] = chat_id
    users_db.temp_user_data_update(data, chat_id)

    update.message.reply_markdown_v2(messages['add_phone_number'])


def add_phone_number(update: Update, context: CallbackContext):
    text = update.message.text
    chat_id = update.effective_chat.id
    data = users_db.temp_user_data_get(chat_id)

    if re.match(r"^998\d{9}$", text) == None:
        update.message.reply_markdown_v2(messages['add_phone_number_error']) 
        return False
    else:
        data['phone_number'] = text
        users_db.temp_user_data_update(data, chat_id)
    
    
        button1 = KeyboardButton(text = "Samarqand shahar")
        button2 = KeyboardButton(text = "Samarqand tumani")
        button3 = KeyboardButton(text = "Bulung'ur tumani")
        button4 = KeyboardButton(text = "Jomboy tumani")
        button5 = KeyboardButton(text = "Ishtixon tumani")
        button6 = KeyboardButton(text = "Kattaqo'rg'on tumani")
        button7 = KeyboardButton(text = "Kattaqo'rg'on shahar")
        button8 = KeyboardButton(text = "Toyloq tumani")
        button9 = KeyboardButton(text = "Qo'shrabot tumani")

        keyboard = ReplyKeyboardMarkup([[button1, button2], [button3, button4], [button5, button6], [button7, button8], [button9]], resize_keyboard=True)
        update.message.reply_markdown_v2(messages['add_region'], reply_markup=keyboard)
        return True

def add_region(update: Update, context: CallbackContext):
    text = update.message.text
    chat_id = update.effective_chat.id
    data = users_db.temp_user_data_get(chat_id)
    data['region'] = text
    users_db.temp_user_data_update(data, chat_id)

    update.message.reply_markdown_v2(messages['add_school'], reply_markup=ReplyKeyboardRemove())

def add_school(update: Update, context: CallbackContext):
    text = update.message.text
    chat_id = update.effective_chat.id
    data = users_db.temp_user_data_get(chat_id)
    data['school'] = text
    users_db.temp_user_data_update(data, chat_id)

    button = KeyboardButton(text = "✅ Tasdiqlash")
    button1 = KeyboardButton(text = "🔄 Qaytadan o'tish")
    keyboard = ReplyKeyboardMarkup([[button],[button1]], resize_keyboard=True)

    first_name = data['first_name']
    last_name = data['last_name']
    phone_number = f"{data['phone_number']}"
    region = data['region']
    school = data['school']

    msg = messages['tasdiqlash_html'].format(first_name=first_name, last_name=last_name, phone_number=phone_number, region=region, school=school)
    # reply html format
    update.message.reply_html(msg, reply_markup=keyboard)

def finally_registration(update: Update, context: CallbackContext):
    text = update.message.text
    if text == "✅ Tasdiqlash":
        chat_id = update.effective_chat.id
        data = users_db.temp_user_data_get(chat_id)

        users_db.add_user(data, chat_id)
        users_db.temp_user_data_remove(chat_id)
        update.message.reply_markdown_v2("Siz muvaffaqiyatli ro'yxatdan o'tdingiz\!", reply_markup=ReplyKeyboardRemove())
    else:
        return registration(update, context)

def registration(update: Update, context: CallbackContext):
    # remove reply keyboard
    chat_id = update.effective_chat.id
    temp_data = users_db.temp_user_data_get(chat_id)
    text = update.message.text
    # if text == "":
    #     status = users_db.status
    #     status = "registration"
    status = users_db.status

    if text == "Ro'yxatdan o'tish!" or status == "registration":
        data = {
            "chat_id": chat_id,
        }
        users_db.add_temp_user_data(data, chat_id)
        update.message.reply_markdown_v2(messages['add_first_name'], reply_markup=ReplyKeyboardRemove())
        users_db.status = "first_name"

    elif status == "first_name":
        add_first_name(update, context)
        users_db.status = "last_name"

    elif status == "last_name":
        add_last_name(update, context)
        users_db.status = "phone_number"

    elif status == "phone_number":
        is_valid = add_phone_number(update, context)
        if is_valid:
            users_db.status = "region"
        else:
            users_db.status = "phone_number"

    elif status == "region":
        add_region(update, context)
        users_db.status = "school"

    elif status == "school":   
        add_school(update, context)
        users_db.status = "tasdiqlash"

    elif status == "tasdiqlash":  
        if text == "✅ Tasdiqlash":
            finally_registration(update, context)
            users_db.status = "other"
        else:
            update.message.reply_markdown_v2(messages['add_first_name'], reply_markup=ReplyKeyboardRemove())
            users_db.status = "registration"

    elif users_db.status_send_url == "sending_url":
        users_db.status_send_url = "other"
        send_message_all_users(update, context)