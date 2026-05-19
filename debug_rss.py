import asyncio
import os
import aiohttp

async def main():
    async with aiohttp.ClientSession() as session:
        url = f"https://www.youtube.com/feeds/videos.xml?channel_id={os.environ['YT_CHANNEL_ID']}"
        async with session.get(url) as resp:
            print(await resp.text())

asyncio.run(main())
