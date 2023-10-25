import aiohttp
import logging
from sqlalchemy import insert, select, update
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import count, random
from src.db import async_session_maker, Posts, engine_sync
from src.config import CHAT_ID, TG_CHANNEL_LINK, TOKEN


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def post(ptype: str, link: str):
    with Session(engine_sync) as session:
        stmt = select(Posts.post_id).order_by(Posts.post_id.desc()).limit(1)
        res = session.execute(stmt)
        post_id = res.scalar()

        post_data = {
            "post_id": post_id + 1,
            "post_type": ptype,
            "link": link
        }

        stmt = insert(Posts).values(**post_data).returning(Posts.post_id)
        res = session.execute(stmt)
        session.commit()
        return res.scalar()


async def post_stats():
    async with async_session_maker() as session:
        stmt = select(count(Posts.status)).where(Posts.status == "post")
        res = await session.execute(stmt)
        return res.scalar()


async def update_post(post_id: str):
    async with async_session_maker() as session:
        stmt_ = update(Posts).where(Posts.post_id == post_id).values({"status": "post"})
        await session.execute(stmt_)
        await session.commit()
        logger.info(f"Successfull update for {post_id}")


async def make_post(cont_type: str,
                    method: str,
                    link: str,
                    post_id: int,
                    chat_id: int = CHAT_ID):
    params = {
            "chat_id": chat_id,
            f"{cont_type}": link,
            "caption": f'<b>POST ID</b>: <i>{post_id}</i>\n\n<b><a href="{TG_CHANNEL_LINK}">Пекара Жеки. Подписаться.</a></b>',
            "parse_mode": "HTML"
        }
    
    logger.info(f"post data is {params}")

    async with aiohttp.ClientSession() as session:
        async with session.post(
            url=f"https://api.telegram.org/bot{TOKEN}/{method}", data=params) as resp:
            if resp.status == 200:
                await update_post(post_id=post_id)
                return True
            else:
                logger.error(f"Failed request to Telegram Bot API, {await resp.json()}")


async def post_on_channel():
    async with async_session_maker() as session:
        stmt = select(Posts).where(Posts.status == "wait").order_by(random()).limit(1)
        res = await session.execute(stmt)
        content = res.scalar()
    
    logger.info(f"Earn post with {content.post_id} ID")

    post_data = {
        "link": content.link,
        "post_id": content.post_id
    }

    if content.post_type == "pic":
        post_data["method"] = "sendPhoto"
        post_data["cont_type"] = "photo"
    elif content.post_type == "vid":
        post_data["method"] = "sendVideo"
        post_data["cont_type"] = "video"
    elif content.post_type == "gif":
        post_data["method"] = "sendAnimation"
        post_data["cont_type"] = "animation"

    return await make_post(**post_data)
