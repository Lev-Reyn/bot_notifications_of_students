from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from config import token
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import types

storage = MemoryStorage()

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
