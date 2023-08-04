import os
import datetime
import requests
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from keepalive import keep_alive
import json

bot = Bot(token=os.getenv('tg_key'))
open_weather_token = os.getenv('weather_key')
dp = Dispatcher(bot)

keep_alive()


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
  await message.reply('Привет! Напиши мне название города и я пришлю сводку погоды!')
