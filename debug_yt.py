import asyncio
import os
import aiohttp

async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://www.googleapis.com/youtube/v3/search",
            params={
                "part": "snippet",
                "channelId": os.environ["YT_CHANNEL_ID"],
                "type": "video",
                "eventType": "live",
                "key": os.environ["YT_API_KEY"],
            },
        ) as resp:
            import json
            print(json.dumps(await resp.json(), indent=2))

asyncio.run(main())
