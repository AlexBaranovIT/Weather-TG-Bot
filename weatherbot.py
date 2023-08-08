import os
import datetime
import requests
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from keepalive import keep_alive
import json

#Instead of tg_key insert your API token from BotFather
bot = Bot(token=os.getenv('tg_key'))
#Instead of weather_key insert your API token from OpenWeather
open_weather_token = os.getenv('weather_key')

dp = Dispatcher(bot)

keep_alive()


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
  await message.reply('HI! Send me a city name and I will send weather info about this city')


@dp.message_handler()
async def get_weather(message: types.Message):
  code_to_smile = {
        "Clear": "Clear \U00002600",
        "Clouds": "Cloudy \U00002601",
        "Rain": "Rain \U00002614",
        "Drizzle": "Little rain \U00002614",
        "Thunderstorm": "Storm \U000026A1",
        "Snow": "Snow \U0001F328",
        "Mist": "Fog \U0001F32B"
    }
  try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно, не пойму что там за погода!"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
              f"Погода в городе: {city}\nТемпература: {cur_weather}C° {wd}\n"
              f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
              f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
              f"***Хорошего дня!***"
              )

  except:
        await message.reply("\U00002620 Проверьте название города \U00002620")


executor.start_polling(dp)
