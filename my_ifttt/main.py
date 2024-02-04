import asyncio
from hydrogram import Client
from redis import Redis
from datetime import datetime
from loguru import logger
from aiohttp import ClientSession
from pydantic import BaseModel

from my_ifttt.settings import settings
from my_ifttt.readwise import ReadWise

if settings.debug:
    from fakeredis import FakeStrictRedis as Redis


class Channel(BaseModel):
    username: str
    tags: list[str]
    display_name: str


TG_CHANNELS = [
            Channel(username="@meduzalive", tags=["news", "russian"], display_name="Meduza"),
            Channel(username="@russiagainstwar", tags=["news", "russian"], display_name="Russians Against War (Sweden)"),
            Channel(username="@CarnegieRussiaEurasia", tags=["news", "russian"], display_name="Carnegie Russia (Berlin)"),
            Channel(username="@partially_unsupervised", tags=["tech", "russian"], display_name="Partially Unsupervised"),
            Channel(username="@addmeto", tags=["tech", "russian"], display_name="Addmeto"),
            Channel(username="@usachevruslan", tags=["tech", "travel", "russian"], display_name="Ruslan Usachev"),
            Channel(username="@testytestchannel", tags=["tech", "russian"], display_name="Testy Test Channel"),
            Channel(username="@EtoBorisAkunin", tags=["books", "russian"], display_name="Boris Akunin"),
            Channel(username="@Duntsova", tags=["news", "politics", "russian"], display_name="Duntsova"),
            Channel(username="@schonberlin", tags=["news", "russian", "german"], display_name="Schon Berlin"),
            Channel(username="@eschulmann", tags=["news", "russian"], display_name="Ekaterina Schulmann"),
            Channel(username="@tldr_tany", tags=["news", "tech", "russian"], display_name="Tatiana Saveleva"),
            Channel(username="@renat_alimbekov", tags=["news", "russian", "tech", "data-science"], display_name="Пристанище Дата Сайентиста"),
            Channel(username="@dlinnlp", tags=["news", "russian", "tech", "nlp"], display_name="DL in NLP"),
            Channel(username="@CVML_team", tags=["news", "russian", "tech", "cv"], display_name="Заметки Computer Vision инженера"),
            Channel(username="@cryptovalerii", tags=["news", "russian", "tech", "crypto"], display_name="Crypto Valerii"),
            Channel(username="@swedenofficial", tags=["news", "swedish"], display_name="Sweden Official"),
            Channel(username="@rybolos_channel", tags=["news", "russian", "tech", "nlp"], display_name="Kali Novskaya"),
            Channel(username="@fe_city_boy", tags=["comedy", "russian"], display_name="Денис Чужой про комедию"),
            Channel(username="@pezduzalive", tags=["news", "comedy", "russian"], display_name="Пездуза"),
            Channel(username="@seeallochnaya", tags=["news", "tech", "russian", "nlp"], display_name="Сиолошная"),
            Channel(username="@dksefun", tags=["russian", "swedish", "education"], display_name="Скандинавские откровения"),
            Channel(username="@astapov_pavel", tags=["russian", "education"], display_name="Павел Астапов"),
            Channel(username="@cumonmychannel", tags=["russian", "pron", "comedy"], display_name="Тот парень с порнозависимостью"),
        ]


def is_main_news_meduza(message):
    return message.text and "Главные новости" in message.text


async def main():
    redis = Redis(host="redis", port=6379, db=0)

    async with Client("tg2readwise", settings.telegram_api_id, settings.telegram_api_hash) as app, ClientSession() as session:
        readwise = ReadWise(settings.readwise_api_token, session)
        await readwise.check_token()

        while True:
            for channel in TG_CHANNELS:
                logger.info(f"Processing channel {channel.username}")

                message_id = redis.get(f"ifttt:readwise:{channel.username}")
                logger.info(f"Last message id {message_id}")
                kwargs = {}
                if not message_id:
                    kwargs["limit"] = 1
                else:
                    message_id = int(message_id)
                    kwargs["limit"] = 30

                logger.info(f"Getting messages from {channel.username} with kwargs {kwargs}")

                messages = []
                async for message in app.get_chat_history(channel.username, **kwargs):
                    if message_id and message.id == message_id:
                        break

                    # I want only main news from Meduza
                    if channel.username == "@meduzalive" and not is_main_news_meduza(message):
                        continue

                    logger.info(f"Processing message {message.link}")
                    if message.text:
                        messages.append(message)

                if not messages:
                    logger.info(f"No messages found")
                    continue

                redis.set(f"ifttt:readwise:{channel.username}", int(messages[0].id))
                for message in messages:
                    telegram_link = message.link

                    await readwise.save(
                            title=str(message.chat.username) + " " + str(datetime.now().isoformat()),
                            url=telegram_link,
                            summary=message.text[:128],
                            html=message.text.html,
                            tags=channel.tags,
                            category="article",
                            author=channel.display_name,
                        )
                    logger.info(f"Saved message {telegram_link} to Readwise")


            # sleep for 60 minutes
            await asyncio.sleep(60 * 60)


asyncio.run(main())
