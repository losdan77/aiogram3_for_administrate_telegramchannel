from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, BotCommand, BotCommandScopeDefault
from aiogram.types import FSInputFile

from apscheduler.schedulers.asyncio import AsyncIOScheduler

import asyncio
import os
from dotenv import load_dotenv

from core.handlers.reddit_memes_eng import published_post_reddit_memes_eng
from core.handlers.info_about_channel import check_info_about_channel

import datetime as dt

load_dotenv()
TOKEN = os.getenv('TOKEN_TEST')
ADMIN_ID = os.getenv('ADMIN_ID')
CHANNEL_REDDITMEMESENG = os.getenv('CHANNEL_REDDITMEMESENG')


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command='start',
                   description='Начало работы'),
        BotCommand(command='nsd_info',
                   description='Информация о НСД'),
        BotCommand(command='channel_info',
                   description='Информация о каналах'),
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(ADMIN_ID, 'Бот запущен!')


async def stop_bot(bot: Bot):
    await bot.send_message(ADMIN_ID, 'Бот остановлен!')


async def get_start(message: Message, bot: Bot):
    if int(message.from_user.id) == int(ADMIN_ID):
        await message.answer('Привет, Бос')
    else:
        await bot.send_message(ADMIN_ID,
                               f'Бос, кто-то лезет к нам id:{message.from_user.id}')
        await message.answer('Друг, я тебя не знаю')

        with open('NSD.txt', 'a', encoding='utf-8') as file:
            file.write(f'{dt.datetime.now()} - {str(message.from_user.id)} - @{message.from_user.username}\n')


async def send_nsd_info(message: Message, bot: Bot):
    if int(message.from_user.id) == int(ADMIN_ID):
        nsd_info = FSInputFile(path=r'./NSD.txt')
        await bot.send_document(ADMIN_ID, document=nsd_info)


async def error_message(message: Message, bot: Bot):
    if int(message.from_user.id) == int(ADMIN_ID):
        await message.answer('Неизвестная команда')


async def start():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(published_post_reddit_memes_eng,
                      trigger='interval',
                      seconds=3600,
                      kwargs={'bot': bot})
    scheduler.start()

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.message.register(get_start,
                        F.text == '/start')
    dp.message.register(send_nsd_info,
                        F.text == '/nsd_info')
    dp.message.register(check_info_about_channel,
                        F.text == '/channel_info')
    dp.message.register(error_message)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(start())
