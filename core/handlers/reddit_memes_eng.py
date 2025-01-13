from aiogram import Bot
from aiogram.types import FSInputFile

import requests
from bs4 import BeautifulSoup
import random

import datetime as dt

from core.utils.for_parser import mass_user_agent

import os
from dotenv import load_dotenv


load_dotenv()
CHANNEL_REDDITMEMESENG = os.getenv('CHANNEL_REDDITMEMESENG')
ADMIN_ID = os.getenv('ADMIN_ID') #

url = 'https://www.reddit.com/r/memes/'
text_div_class = 'block relative cursor-pointer group bg-neutral-background focus-within:bg-neutral-background-hover hover:bg-neutral-background-hover xs:rounded-[16px] px-md py-2xs my-2xs nd:visible'
photo_div_class = 'media-lightbox-img max-h-[100vw] h-full w-full object-contain overflow-hidden relative bg-black'


async def published_post_reddit_memes_eng(bot: Bot):
    try:
        headers = {
            'User-Agent': random.choice(mass_user_agent)
        }
        proxies = {
            'http': 'http://V84kEe:XhAdiJu5Ej@45.15.72.224:5500',
            'https': 'http://V84kEe:XhAdiJu5Ej@45.15.72.224:5500'
        }   
        
        response = requests.get(url, headers=headers, proxies=proxies)
        soup = BeautifulSoup(response.text, "lxml")

        photo_url = soup.find(class_=photo_div_class).find('img')['src']
        title_text = soup.find(class_=text_div_class).find('a')
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
            
    except Exception as e:
        await bot.send_message(ADMIN_ID, f'ошибка {e}')
