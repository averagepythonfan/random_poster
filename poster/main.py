import datetime
import os
import requests
import time
import logging
from sqlalchemy.engine import create_engine
from sqlalchemy import text, URL
from sqlalchemy.exc import SQLAlchemyError


# init logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# init environment
ADMIN = os.getenv("ADMIN")
CHAT_ID: int = -(int(os.getenv("CHAT_ID")))
TG_CHANNEL_LINK: str = os.getenv("TG_CHANNEL_LINK")
TOKEN: str = os.getenv("TOKEN")


class TelegramBotAPIError(BaseException):
    """Exception for failed TelegramBotAPI request"""
    ...


# init db's URL and sync engine
db_url = URL.create(
    drivername="postgresql",
    username=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    database=os.getenv("POSTGRES_DB")
)
engine = create_engine(db_url)


# functions
def select_random_post() -> tuple:
    """Pulls a randon post from Postgres DB.
    If there is no any posts raise Assertion Error.
    
    Returns a Tuple with post data."""

    stmt = text("""
        SELECT
            post_id,
            post_type,
            link
        FROM post 
        WHERE status = 'wait' 
        ORDER BY random()
        limit 1
    """)

    with engine.connect() as con:
        res = con.execute(stmt)
        post = res.fetchone()
        
    assert len(post) == 3
    return post


def transorm_post_to_data(post: tuple) -> dict:
    """Transorm post data tuple to dict
    with TG Bot API data"""

    POST_ID, POST_TYPE, LINK = post

    post_data = {
        "link": LINK,
        "post_id": POST_ID
    }

    if POST_TYPE == "pic":
        post_data["method"] = "sendPhoto"
        post_data["cont_type"] = "photo"
    elif POST_TYPE == "vid":
        post_data["method"] = "sendVideo"
        post_data["cont_type"] = "video"
    elif POST_TYPE == "gif":
        post_data["method"] = "sendAnimation"
        post_data["cont_type"] = "animation"

    return post_data


def post_to_channel(link: str,
                    cont_type: str, 
                    post_id: int,
                    method: str) -> bool:
    """Make a post with TG Bot API
    
    Return True, otherwise raise an Exception"""

    params = {
        "chat_id": CHAT_ID,
        f"{cont_type}": link,
        "caption": f'<b>POST ID</b>: <i>{post_id}</i>\n\n<b><a href="{TG_CHANNEL_LINK}">Пекара Жеки. Подписаться.</a></b>',
        "parse_mode": "HTML"
    }

    resp = requests.post(f"https://api.telegram.org/bot{TOKEN}/{method}", json=params)
    if resp.status_code == 200:
        return True
    else:
        raise TelegramBotAPIError(f"failed post requests: {resp.json()}")


def update_db(post_id: int) -> bool:
    """Update successfull post in data base"""

    with engine.connect() as con:
        con.execute(text(f"""
            UPDATE post
            SET status = 'post'
            WHERE post_id = {post_id}
        """))
        con.commit()
        return True


def notificate_admin(text: str) -> None:
    """Notificate an Admin with special information
    through TG Bot API, returns None"""

    params = {
        "chat_id": ADMIN,
        "text": text,
    }

    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json=params
    )


def make_post() -> None:
    try:
        post = select_random_post()
    except AssertionError:
        notificate_admin("There is no any posts")
    data = transorm_post_to_data(post)
    try:
        if post_to_channel(**data):
            pid = data["post_id"]
            if update_db(pid):
                notificate_admin(f"Successfull post, id {pid}")
    except TelegramBotAPIError as e:
        notificate_admin(text=str(e))
    except SQLAlchemyError as sql_e:
        notificate_admin(text=str(sql_e))


# main endless loop
while True:
    now = datetime.datetime.now()
    if 6 <= now.hour <= 20:
        logger.info("Posting time!")
        if (now.minute % 30 == 0 ):
            logger.info("Time to make a post and wait for 30 min!")
            make_post()
            time.sleep(1800)
        else:
            logger.info("Wait a minute!")
            time.sleep(60)
    else:
        logger.info("Wait a minute!")
        time.sleep(60)
