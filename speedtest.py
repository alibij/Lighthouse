import asyncio
from typing import List, Optional
from aiohttp import ClientSession, ClientTimeout
import time


async def speedTest(testUrl='https://speed.cloudflare.com/__down?bytes=1000000', proxy=None, timeout=30):

    speed = 0
    try:
        timeout = ClientTimeout(total=timeout)

        async with ClientSession(timeout=timeout) as session:
            async with session.get(testUrl, proxy=proxy) as response:
                if response.status == 200:

                    startTime = time.time()
                    data = 0
                    bufferSize = 1024 * 1024

                    while True:
                        d = await response.content.read(bufferSize)
                        if not d:
                            break
                        data += len(d)

                    endTime = time.time()
                    download_time = endTime - startTime
                    speed = (data / download_time) / (1024 * 1024)
                else:
                    # print(f"Failed to download from {proxy}. Status code: {response.status}")
                    pass
    except Exception as e:
        # print(f"Exception occurred for {url} with proxy {proxy}: {e}")
        pass
    return float("{:.2f}".format(speed))

async def main():
    speed = await speedTest()
    print(f'Current Speed is : {speed} MB/s')

if __name__ == "__main__":
    asyncio.run(main())
    