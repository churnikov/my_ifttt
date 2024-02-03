import asyncio
from hydrogram import Client

from my_ifttt.settings import settings


async def main():
    async with Client("tg2readwise", settings.telegram_api_id, settings.telegram_api_hash) as app:
        await app.send_message("me", "Greetings from **Hydrogram**!")


asyncio.run(main())
