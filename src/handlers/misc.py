import aiohttp
from sqlalchemy import insert, select, update
from sqlalchemy.sql.functions import count, random
from src.db import async_session_maker, Posts
from src.config import CHAT_ID, TG_CHANNEL_LINK, TOKEN


async def post(ptype: str, link: str):
    async with async_session_maker() as session:
        post_data = {
            "post_type": ptype,
            "link": link
        }
        stmt = insert(Posts).values(**post_data).returning(Posts.post_id)
        res = await session.execute(stmt)
        await session.commit()
        return res.scalar()


async def post_stats():
    async with async_session_maker() as session:
        stmt = select(count(Posts.status)).where(Posts.status == "post")
        res = await session.execute(stmt)
        return res.scalar()


async def update_post(link: str):
    async with async_session_maker() as session:
        stmt_ = update(Posts).where(Posts.link == link).values({"status": "post"})
        await session.execute(stmt_)
        await session.commit()



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
    
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url=f"https://api.telegram.org/bot{TOKEN}/{method}", data=params) as resp:
            if resp.status == 200:
                await update_post(link=link)


async def post_on_channel():
    async with async_session_maker() as session:
        stmt = select(Posts).where(Posts.status == "wait").order_by(random()).limit(1)
        res = await session.execute(stmt)
        content = res.scalar()
    
    post_data = {
        "cont_type": content.post_type,
        "link": content.link,
        "post_id": content.post_id
    }

    if content.post_type == "pic":
        post_data["method"] = "sendPhoto"
    elif content.post_type == "vid":
        post_data["method"] = "sendVideo"
    elif content.post_type == "gif":
        post_data["method"] = "sendAnimation"

    await make_post(**post_data)
