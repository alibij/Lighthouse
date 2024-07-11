import asyncio
from typing import List, Optional
from aiohttp import ClientSession, ClientTimeout
import time


# async def __download_speed_test(url, proxy, download_timeout):
#     speed = -1
#     try:
#         timeout = ClientTimeout(total=download_timeout)

#         async with ClientSession(timeout=timeout) as session:
#             async with session.get(url, proxy=proxy) as response:
#                 if response.status == 200:

#                     startTime = time.time()
#                     data = 0
#                     bufferSize = 1024 * 1024

#                     while True:
#                         d = await response.content.read(bufferSize)
#                         if not d:
#                             break
#                         data += len(d)

#                     endTime = time.time()
#                     download_time = endTime - startTime
#                     speed = (data / download_time) / (1024 * 1024)
#                     print("url:",url,"speed:","{:.2f}".format(speed))
#                 else:
#                     print(
#                         f"Failed to download from {url}. Status code: {response.status}")
#     except Exception as e:
#         # print(f"Exception occurred for {url} with proxy {proxy}: {e}")
#         pass
#     return speed           


# async def __test_urls_with_proxies(urls: List[str], proxies: List[Optional[str]], download_timeout):
#     speedTest = []

#     for url in urls:
#         for proxy in proxies:
#             speedTest.append(await __download_speed_test(url, proxy, download_timeout))

#     return speedTest


async def speedTest(testUrl='https://speed.cloudflare.com/__down?bytes=1000000', proxy=None, timeout=30):

    # speedTest = []

    # for url in testUrl:
    #     for proxy in proxies:
    #         speedTest.append(await __download_speed_test(url, proxy, timeout))

    speed = -1
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
                    print(
                        f"Failed to download from {proxy}. Status code: {response.status}")
    except Exception as e:
        # print(f"Exception occurred for {url} with proxy {proxy}: {e}")
        pass
    return "{:.2f}".format(speed)

    return speedTest

