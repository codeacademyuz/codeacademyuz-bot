from flask import Flask
import os
from .bot import (
    start,
)


BOT_TOKEN = os.environ.get('BOT_TOKEN')

app = Flask(__name__)


from .routes import *
