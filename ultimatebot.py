import requests
import telebot
from telebot.types import Message
from datetime import datetime
import pytz
from random import randint
from bs4 import BeautifulSoup as BS

TOKEN = '934221825:AAFgsBoxVRarQqO8H6JL_5ku7vdNYwLAP0M'

BASE_URL = 'https://api.telegram.org/bot{}/'.format(TOKEN)

bot = telebot.TeleBot(TOKEN)

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

@bot.message_handler(commands=['randfilm'])
def rand_film_generate(message:Message):
    url = 'https://www.kinopoisk.ru/top/'

    response = requests.get(url)

    html = response.text

    soup = BS(html, "html.parser")

    tds = soup.find_all('td', {'style': "height: 27px; vertical-align: middle; padding: 6px 30px 6px 0"})

    names = []

    e = 0
    for item in tds:
        e += 1
        film = str(e) + '.' + item.find('a', {'class': 'all'}).text
        names.append(film)
    e = randint(0, len(names))
    print(names[e])
    bot.send_message(message.chat.id, names[e])


@bot.message_handler(commands=['help'])
def send_help(message:Message):
    commands = [
                'sendlocation - send his location',
                'whattimeisit - send you the time in your city(format of command - whattimeisit your timezone)',
                'howistheweather - send you the weather in your city(format of command - howistheweather your city',
                'randomemoji - send you random emoji',
                'hello - hello',
                'help - send you the list of commands'
                ]
    total = ''
    for i in commands:
        total += i + '\n'
    bot.send_message(message.chat.id, total)

#{'ok': True, 'result': [{'update_id': 780289943, 'message': {'message_id': 506, 'from': {'id': 558801744, 'is_bot': False, 'first_name': 'Егор', 'last_name': 'Летов,а может и нет', 'language_code': 'ru'}, 'chat': {'id': 558801744, 'first_name': 'Егор', 'last_name': 'Летов,а может и нет', 'type': 'private'}, 'date': 1578682638, 'text': 'gggg'}}]}

@bot.message_handler(commands='howistheweather')
def send_weather(message:Message):
    try:
        mes = message.text.replace('/howistheweather ', '')
        weather_url = 'https://yandex.ru/pogoda/' + mes.lower()
        response = requests.get(weather_url)
        html = BS(response.text, 'html.parser')
        t = html.find('span', {'class': 'temp__value'}).text
        wind_speed = html.find('span', {'class': 'wind-speed'}).text
        humidity = html.find('div', {'class': 'term term_orient_v fact__humidity'}).text
        pressure = html.find('div', {'class': 'term term_orient_v fact__pressure'}).text
        bot.send_message(message.chat.id,'The tempreture in your city is {}, wind speed is {}, humidity is {}, the pressure is {}'.format(t, wind_speed, humidity, pressure))
    except:
        AttributeError
        bot.send_message(message.chat.id, 'wrong city')

@bot.message_handler(commands=['whattimeisit'])
def send_time(message:Message):
    try:
        location = message.text.replace('/whattimeisit ', '')
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




