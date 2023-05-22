import telegram
from flask import request
from telegram.ext import Dispatcher

import settings
# import os

# TOKEN = os.environ.get('TOKEN')

bot = telegram.Bot(settings.TOKEN)

from lms import app

@app.route('/getInfo')
def getInfo():

    info = bot.get_webhook_info()
    return info.to_json()

@app.route('/set')
def setWebhook():
    
    HOOK_URL = 'https://codeacademyrobot.pythonanywhere.com/'
    hook_bool = bot.setWebhook(url=HOOK_URL)
    return str(hook_bool)



@app.route('/', methods=['POST'])
def main():
    from lms.handler import main

    dp = Dispatcher(bot, None, workers=1)

    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)

        dp = main(dp)

        dp.process_update(update)


    return 'ok'