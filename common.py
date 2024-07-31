from aiohttp import ClientSession, ClientTimeout
import asyncio
import time
import sys
import os
import base64
import json


async def removeRemark(url, num):

    mode = url.split('://')
    mode[0] = mode[0].lower()

    if mode[0] in ['ss', 'trojan']:
        return (f'{url.split("#")[0]}#Lighthouse.{num}')

    elif mode[0] in ['vmess', 'vless']:

        decoded_data = base64.b64decode(mode[1])
        u = json.loads(decoded_data.decode('utf-8'))
        u['ps'] = f'Lighthouse.{num}'
        u = json.dumps(u, ensure_ascii=False)
        eb = base64.b64encode(u.encode('utf-8'))
        es = eb.decode('utf-8')
        return (f'{mode[0]}://{es}')


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def make_file(data: any, file_name: str, mode='w', encoding='utf-8'):
    with open(file_name, mode, encoding=encoding) as f:
        f.write(data)


def print_loading_bar(current, min_val, max_val, length=80):
    progress = (current - min_val) / (max_val - min_val)
    percent = int(progress * 100)
    bar_length = int(length * progress)
    bar = '[' + '|' * bar_length + ' ' * \
        (length - bar_length) + '] ' + f'{percent} %'
    sys.stdout.write('\r' + bar)
    sys.stdout.flush()


async def get_ip(proxy=None, time_out=10):
    try:
        timeout = ClientTimeout(total=time_out)
        testUrl = 'http://icanhazip.com/'
        async with ClientSession(timeout=timeout) as session:
            async with session.get(testUrl, proxy=proxy) as response:
                if response.status == 200:
                    return await response.text()
    except Exception as e:
        pass


async def get_ip_data(proxy=None, time_out=10):

    timeout = ClientTimeout(total=time_out)

    ip = await get_ip(proxy)

    testUrl = f'http://ip-api.com/json/{ip}'
    try:
        async with ClientSession(timeout=timeout) as session:
            async with session.get(testUrl) as response:
                if response.status == 200:
                    data = (await response.json())
                    data['ip'] = ip
                    return data
                else:
                    return None
    except Exception as e:
        pass

    testUrl = f'https://ipinfo.io/{ip}/json'
    try:
        async with ClientSession(timeout=timeout) as session:
            async with session.get(testUrl) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return None
    except Exception as e:
        pass

    testUrl = 'https://ifconfig.co/json'
    try:

        async with ClientSession(timeout=timeout) as session:
            async with session.get(testUrl, proxy=proxy) as response:
                if response.status == 200:
                    return await response.json()
    except Exception as e:
        pass

if __name__ == "__main__":
    asyncio.run(get_ip_data())
