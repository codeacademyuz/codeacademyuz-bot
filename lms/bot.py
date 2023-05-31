from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler, ConversationHandler
from telegram import Update, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, Video
from .constants import messages
from .db import Database
import re
users_db = Database()
import requests

def start(update: Update, context: CallbackContext):
    first_name = update.effective_user.first_name
    chat_id = update.effective_chat.id
    welcome_text = messages.get('welcome_text').format(first_name=first_name)
    button = KeyboardButton(text="Ro'yxatdan o'tish!")
    keyboard = ReplyKeyboardMarkup([[button]], resize_keyboard=True)
    update.message.reply_html(text=welcome_text, reply_markup=keyboard)

    check_user = users_db.check_user(update.effective_chat.id)
    if check_user:
        start_msg = messages['registrated']
        button = KeyboardButton(text="👤 Info")
        keyboard = ReplyKeyboardMarkup([[button]], resize_keyboard=True)
        update.message.reply_markdown_v2(start_msg, reply_markup=keyboard)
    else:
        data = {
                "chat_id": chat_id,
                "status": "username"
            }
        users_db.add_temp_user_data(data, chat_id)
        start_msg = messages.get('username_exists')

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
    if chat_id == 1046157991 or chat_id == 715393503 or update.message.chat.username == 'jumanovdiyorbek':
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
    
    if query.data.split(':')[1] == 'andriod':
        with open('codeacademyuz-bot/android_signup.mp4', 'rb') as f:
            andriod = f
            query.bot.send_video(chat_id=update.effective_user.id, video=andriod, caption=messages['caption'])
    elif query.data.split(':')[1] == 'ios':
        with open('codeacademyuz-bot/ios_signup.mp4', 'rb') as f:
            ios = f
            query.bot.send_video(update.effective_user.id, video=ios, caption=messages['caption'])
    

def add_first_name(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    text = update.message.text
    data = users_db.temp_user_data_get(chat_id)
    data['first_name'] = text
    data['status'] = 'last_name'
    users_db.temp_user_data_update(data, chat_id)
    update.message.reply_markdown_v2(messages['add_last_name'])

def add_last_name(update: Update, context: CallbackContext):
    text = update.message.text
    chat_id = update.effective_chat.id
    data = users_db.temp_user_data_get(chat_id)
    data['last_name'] = text
    data['username'] = update.effective_user.username
    data['chat_id'] = chat_id
    data['status'] = 'phone_number'
    users_db.temp_user_data_update(data, chat_id)

    update.message.reply_markdown_v2(messages['add_phone_number'])


def add_phone_number(update: Update, context: CallbackContext):
    text = update.message.text
    chat_id = update.effective_chat.id
    data = users_db.temp_user_data_get(chat_id)

    if re.match(r"^998\d{9}$", text) == None:
        update.message.reply_markdown_v2(messages['add_phone_number_error']) 
        data = {
                "status": "phone_number"
            }
        users_db.temp_user_data_update(data, chat_id)
    else:
        data['phone_number'] = text
        data['status'] = 'region'
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
    data['status'] = 'school'
    users_db.temp_user_data_update(data, chat_id)

    update.message.reply_markdown_v2(messages['add_school'], reply_markup=ReplyKeyboardRemove())

def add_school(update: Update, context: CallbackContext):
    text = update.message.text
    chat_id = update.effective_chat.id
    data = users_db.temp_user_data_get(chat_id)
    data['school'] = text
    data['status'] = 'tasdiqlash'
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
    chat_id = update.effective_chat.id
    if text == "✅ Tasdiqlash":
        
        data = users_db.temp_user_data_get(chat_id)

        users_db.add_user(data, chat_id)
        users_db.temp_user_data_remove(chat_id)

        user_data = {
            "first_name": data["first_name"],
            "last_name": data["last_name"],
            "tg_username": data["username"],
            "tg_chat_id": data["chat_id"],
            "phone": data["phone_number"],
            "school": data["school"],
            "region": data["region"],
        }
        response = requests.post("https://calms.pythonanywhere.com/students/", json=user_data)
        
        update.message.reply_markdown_v2("Siz muvaffaqiyatli ro'yxatdan o'tdingiz\!", reply_markup=ReplyKeyboardRemove())
    else:
        data = {'status': 'first_name'}
        users_db.temp_user_data_update(data, chat_id)
        return registration(update, context)

def registration(update: Update, context: CallbackContext):

    if users_db.status_send_url != "sending_url":
        chat_id = update.effective_chat.id

        # check is user in database
        if not users_db.check_user(chat_id):
            temp_data = users_db.temp_user_data_get(chat_id)
            text = update.message.text

            if not users_db.check_user(chat_id):
                status = temp_data['status']

                if text == "Ro'yxatdan o'tish!" and status != 'first_name':
                    username = update.effective_user.username
                    if username == None:
                        start_msg = messages.get('username_none')
                        # create inline keyboard
                        button_andriod = InlineKeyboardButton("Andriod uchun", callback_data="noneusername:andriod")
                        button_ios = InlineKeyboardButton("IOS uchun", callback_data="noneusername:ios")
                        keyboard = InlineKeyboardMarkup([[button_andriod, button_ios]])
                        update.message.reply_markdown_v2(start_msg, reply_markup=keyboard)
                    
                    else:
                        data = {
                            "chat_id": chat_id,
                            "status": "first_name"
                        }
                        users_db.temp_user_data_update(data, chat_id)
                        update.message.reply_markdown_v2(messages['add_first_name'], reply_markup=ReplyKeyboardRemove())
                        # users_db.status = "first_name"

                elif status == "first_name":
                    add_first_name(update, context)

                elif status == "last_name":
                    add_last_name(update, context)

                elif status == "phone_number":
                    add_phone_number(update, context)

                elif status == "region":
                    add_region(update, context)

                elif status == "school":   
                    add_school(update, context)

                elif status == "tasdiqlash":  
                    if text == "✅ Tasdiqlash":
                        finally_registration(update, context)
                    else:
                        update.message.reply_markdown_v2(messages['add_first_name'], reply_markup=ReplyKeyboardRemove())
                        data = {'status': 'first_name'}
                        users_db.temp_user_data_update(data, chat_id)
        else:
            start(update, context)

    elif users_db.status_send_url == "sending_url":
        users_db.status_send_url = "other"
        send_message_all_users(update, context)