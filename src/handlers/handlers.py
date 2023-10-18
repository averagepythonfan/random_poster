import logging
from aiogram import F, Router
from aiogram.types import Message
from src.config import ADMIN
from aiogram.filters import Command
from .misc import post, post_stats


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


admin = Router()


@admin.message(F.photo)
async def take_pic(message: Message):
    if message.from_user.id == int(ADMIN):
        photo_id = str(message.photo[-1].file_id)
        res = await post(ptype="pic", link=photo_id)
        logger.info("photo added to database")
        await message.reply(f'Post_id {res}')


@admin.message(F.video)
async def take_vid(message: Message):
    if message.from_user.id == int(ADMIN):
        vid_id = str(message.video.file_id)
        res = await post(ptype="vid", link=vid_id)
        logger.info("video added to database")
        await message.reply(f'Post_id {res}')


@admin.message(F.animation)
async def take_gif(message: Message):
    if message.from_user.id == int(ADMIN):
        gif_id = message.animation.file_id
        res = await post(ptype='gif', link=gif_id)
        await message.reply(f'Post_id {res}')


@admin.message(Command(commands=['stats']))
async def stats_command(message: Message):
    if message.from_user.id == ADMIN:
        res = await post_stats()
        await message.reply(f"Stats: Post Count: {res}")
