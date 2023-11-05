from aiogram import F, Router
from aiogram.types import Message
from src.config import admins
from aiogram.filters import Command
from .misc import post, post_stats, post_on_channel


admin = Router()


@admin.message(F.photo)
async def take_pic(message: Message):
    if message.from_user.id in admins:
        photo_id = str(message.photo[-1].file_id)
        res = post(ptype="pic", link=photo_id)
        await message.reply(f'Post_id {res}')


@admin.message(F.video)
async def take_vid(message: Message):
    if message.from_user.id in admin:
        vid_id = str(message.video.file_id)
        res = post(ptype="vid", link=vid_id)
        await message.reply(f'Post_id {res}')


@admin.message(F.animation)
async def take_gif(message: Message):
    if message.from_user.id in admins:
        gif_id = message.animation.file_id
        res = post(ptype='gif', link=gif_id)
        await message.reply(f'Post_id {res}')


@admin.message(Command(commands=['stats']))
async def stats_command(message: Message):
    if message.from_user.id in admins:
        res = await post_stats()
        await message.reply(f"Stats: Post Count: {res}")


@admin.message(Command(commands=['random']))
async def stats_command(message: Message):
    if message.from_user.id in admins:
        res = await post_on_channel()
        if res:
            await message.reply(f"Successfull post")

@admin.message(Command(commands=['status']))
async def stats_command(message: Message):
    if message.from_user.id in admins:
        res = f"<b>ID:</b> {message.from_user.id},\n<b>STATUS</b>: ADMIN"
        await message.reply(res, parse_mode='HTML')
    else:
        res = f"<b>ID:</b> {message.from_user.id},\n<b>STATUS</b>: GUEST"
        await message.reply(res, parse_mode='HTML')