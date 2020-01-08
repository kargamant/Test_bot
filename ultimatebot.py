import requests
import telebot
from telebot.types import Message
from datetime import datetime
import pytz
from random import randint

TOKEN = '934221825:AAFgsBoxVRarQqO8H6JL_5ku7vdNYwLAP0M'

BASE_URL = 'https://api.telegram.org/bot{}/'.format(TOKEN)

bot = telebot.TeleBot(TOKEN)

chat_ids = [
     558801744,
    -365197085,
     491835686
]

@bot.message_handler(commands=['randomemoji'])
def send_randomemoji(message:Message):
    emojis = [
              '😀 ','😬' ,'😁',' 😂',' 😃',' 😄',' 🤣' ,'😅',' 😆',' 😇',
              ' 😉',' 😊',' 🙂',' 🙃',' ☺' ,'😋',' 😌',' 😍',' 😘',' 😗',
              ' 😙' ,'😚',' 🤪',' 😜' ,'😝',' 😛',' 🤑',' 😎',' 🤓',' 🧐',
              ' 🤠',' 🤗',' 🤡',' 😏',' 😶',' 😐',' 😑 ','😒' ,'🙄 '
              ]
    i = randint(0, len(emojis))
    bot.send_message(message.chat.id, emojis[i])

@bot.message_handler(commands=['hello'])
def say_hello(message:Message):
    bot.send_message(message.chat.id, 'hello, human!')

@bot.message_handler(commands=['sendlocation'])
def send_location(message:Message):
    bot.send_location(message.chat.id, 55.695703, 37.926654)

@bot.message_handler(commands=['help'])
def send_help(message:Message):
    commands = [
                'sendlocation - send his location',
                'whattimeisit - send you the time in your city',
                'howistheweather - send you the weather in your city',
                'randomemoji - send you random emoji',
                'hello - hello',
                'help - send you the list of commands'
                ]
    total = ''
    for i in commands:
        total += i + '\n'
    bot.send_message(message.chat.id, total)

@bot.message_handler(commands=['whattimeisit'])
def send_time(message:Message):
    bot.send_message(message.chat.id, 'Ok. Send your timezone in format (part of the world/city)?')
    @bot.message_handler(func=lambda message: True)
    def get_usercity(message: Message):
        try:
            location = message.text
            timezone = pytz.timezone(location)
            time = datetime.now(timezone)
            bot.send_message(message.chat.id, 'it is {} in your city'.format(time))
        except:
            pytz.exceptions.UnknownTimeZoneError
            bot.send_message(message.chat.id, 'Sorry! Misunderstanded you')

def get_response(func):
    return requests.get(BASE_URL + func).json()


print(get_response('getupdates'))
bot.polling()

