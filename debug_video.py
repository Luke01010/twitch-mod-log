"""
debug_video.py — Dynamically looks up the channel's RSS feed, finds all video IDs,
then calls videos.list to see which one (if any) has an activeLiveChatId.
Run this after quota resets to verify the full RSS -> videos.list chain works.
"""
import asyncio
import json
import os
import re

import aiohttp


async def main():
    channel_id = os.environ["YT_CHANNEL_ID"]
    api_key = os.environ["YT_API_KEY"]

    async with aiohttp.ClientSession() as session:
        # Step 1: fetch RSS feed and extract all video IDs
        url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
        print(f"Fetching RSS: {url}")
        async with session.get(url) as resp:
            text = await resp.text()
        video_ids = re.findall(r"<yt:videoId>([^<]+)</yt:videoId>", text)
        print(f"Found {len(video_ids)} video IDs in RSS: {video_ids}")

        if not video_ids:
            print("No video IDs found in RSS feed -- is the channel ID correct?")
            return

        # Step 2: call videos.list with all IDs batched (1 quota unit)
        print(f"\nCalling videos.list for {len(video_ids)} IDs...")
        async with session.get(
            "https://www.googleapis.com/youtube/v3/videos",
            params={
                "part": "liveStreamingDetails,snippet",
                "id": ",".join(video_ids),
                "key": api_key,
            },
        ) as resp:
            data = await resp.json()

        if "error" in data:
            print(f"\nAPI ERROR:\n{json.dumps(data['error'], indent=2)}")
            return

        items = data.get("items", [])
        print(f"Got {len(items)} items back from API\n")
        for item in items:
            vid = item.get("id")
            title = item.get("snippet", {}).get("title", "(no title)")
            live = item.get("liveStreamingDetails", {})
            chat_id = live.get("activeLiveChatId")
            status = "LIVE" if chat_id else "not live"
            print(f"  [{status}]  {vid}  |  {title}")
            if chat_id:
                print(f"         activeLiveChatId: {chat_id}")
        print()

        if not items:
            print("No items returned. The video IDs may not belong to this API key's quota project.")


asyncio.run(main())
