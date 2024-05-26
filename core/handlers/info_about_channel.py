from aiogram import Bot
from aiogram.types import Message

import os
from dotenv import load_dotenv


load_dotenv()
CHANNEL_REDDITMEMESENG = os.getenv('CHANNEL_REDDITMEMESENG')
ADMIN_ID = os.getenv('ADMIN_ID')


async def check_info_about_channel(message: Message, bot: Bot):
    if int(message.from_user.id) == int(ADMIN_ID):
        member_count = await bot.get_chat_member_count(CHANNEL_REDDITMEMESENG)
        info = await bot.get_chat(CHANNEL_REDDITMEMESENG)
        text = f'''
                    Канал: {info.title}
                    Подписчиков: {member_count}
                '''
        await bot.send_message(ADMIN_ID, text)