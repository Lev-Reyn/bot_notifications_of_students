from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from config import token
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

bot = Bot(token=token)
dp = Dispatcher(bot, storage=storage)
