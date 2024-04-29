from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, BotCommand, BotCommandScopeDefault
from aiogram.types import FSInputFile

from apscheduler.schedulers.asyncio import AsyncIOScheduler

import asyncio
import os
from dotenv import load_dotenv

import requests
from bs4 import BeautifulSoup
import random

import datetime as dt

load_dotenv()
TOKEN = os.getenv('TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')
CHANNEL_REDDITMEMESENG = os.getenv('CHANNEL_REDDITMEMESENG')

mass_user_agent = ['Mozilla/5.0 (compatible; U; ABrowse 0.6; Syllable) AppleWebKit/420+ (KHTML, like Gecko)',
                    'Mozilla/5.0 (compatible; ABrowse 0.4; Syllable)',
                    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; GTB5; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; Maxthon; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)',
                    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser; GTB6; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)',
                    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser; GTB5; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)',
                    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB6; Acoo Browser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
                    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Trident/4.0; Acoo Browser; GTB5; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)',
                    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)',
                    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; GTB5; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)',
                    'Mozilla/5.0 (X11; Linux i686; rv:7.0a1) Gecko/20110603 SeaMonkey/2.2a1pre',
                    'Mozilla/5.0 (X11; Linux i686; rv:7.0a1) Gecko/20110530 SeaMonkey/2.2a1pre',
                    'Mozilla/5.0 (X11; Linux i686; rv:7.0a1) Gecko/20110526 SeaMonkey/2.2a1pre'
                   ]

proxies = {'https': 'http://V84kEe:XhAdiJu5Ej@45.15.72.224:5500'}

url = 'https://www.reddit.com/r/memes/'
block_div_class = 'block relative cursor-pointer group bg-neutral-background focus-within:bg-neutral-background-hover hover:bg-neutral-background-hover xs:rounded-[16px] px-md py-2xs my-2xs nd:visible'
text_title_class = 'block font-semibold text-neutral-content-strong m-0 visited:text-neutral-content-weak text-16 xs:text-18  mb-2xs xs:mb-xs '


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command='start',
                   description='Начало работы'),
        BotCommand(command='nsd_info',
                   description='Информация о НСД')
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


async def published_post(bot: Bot):
    try:
        headers = {
            'User-Agent': random.choice(mass_user_agent)
        }

        response = requests.get(url, headers=headers, proxies=proxies)
        soup = BeautifulSoup(response.text, "lxml")

        photo_url = soup.find(class_=block_div_class).find('img')['src']
        title_text = soup.find(class_=block_div_class).find('a')
        title_text = str(title_text.text)

        with open('photo_url.txt', 'r') as file:
            last_photo_url = file.readline()

        if photo_url != last_photo_url:
            with open('photo_url.txt', 'w') as file:
                file.write(photo_url)

            photo = requests.get(photo_url, headers=headers, proxies=proxies)

            with open('photo.png', 'wb') as file:
                file.write(photo.content)

            result_photo = FSInputFile(r'./photo.png')
            await bot.send_photo(CHANNEL_REDDITMEMESENG,
                                photo=result_photo,
                                caption=title_text)
    except:
        print('error')
    # title_text = 'hihihihih'
    # result_photo = FSInputFile(r'./photo.png')
    # await bot.send_photo(CHANNEL_REDDITMEMESENG,
    #                     photo=result_photo,
    #                     caption=title_text)

async def error_message(message: Message, bot: Bot):
    if int(message.from_user.id) == int(ADMIN_ID):
        await message.answer('Неизвестная команда')


async def start():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(published_post,
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
    dp.message.register(error_message)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(start())
