import asyncio
import logging
import os

import aiohttp
from custom_components.generac.api import GeneracApiClient

logging.basicConfig(level=logging.DEBUG)

jar = aiohttp.CookieJar(unsafe=True)


async def main():
    async with aiohttp.ClientSession(cookie_jar=jar) as session:
        api = GeneracApiClient(os.environ["GENERAC_USER"], os.environ["GENERAC_PASS"], session)
        await api.login()
        print(await api.get_generator_data())

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
