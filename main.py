import argparse
import os
from speedtest import speedTest
import base64
import asyncio
from common import *
from createConfig import fetch_and_decode_data, create_config, main_config
from managertask import start_core, stop_task, find_xray_pid
from getPing import testPing


def connect_to_fastest(url):
    if pid := find_xray_pid():
        print(pid)
        stop_task(pid)
    if main_config(url):
        start_core(config_file_path='./config.json')


async def main(test_limit, speedtelorance):
    clear()
    print('Getting the latest servers')
    file = create_config(fetch_and_decode_data())

    task = start_core()

    servers = await testPing(proxies=[f'http://localhost:{i}' for i in range(file['startPort'], file['lastPort']+1)])

    proxies = {}
    for i, ping in enumerate(servers):
        port = i+file['startPort']
        proxies[port] = {'port': port, 'proxyUrl': f'http://localhost:{port}', 'connectionUrl': await removeRemark(file['serverList'][i], i), 'ping': ping, 'downloadSpeed': 0}

    clashFile = ''
    serverfile = ''
    activeServer = []
    for i in proxies:
        if proxies[i]['ping'] > 0:
            activeServer.append(proxies[i])
    activeServer = sorted(activeServer, key=lambda x: x['ping'])
    highestspeed = 0.00
    speed = 0.00
    for i, server in enumerate(activeServer):
        highestspeed = float(speed) if float(
            speed) > highestspeed else highestspeed

        speed = await speedTest(proxy=server['proxyUrl'])
        activeServer[i]['downloadSpeed'] = speed
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f'current server speed is {speed} MB/s')
        print(f'highest server speed is {highestspeed} MB/s')
        serverlen = len(activeServer) if test_limit < 0 else test_limit
        print(f'\n   {i}/{serverlen} tested')
        if i == test_limit:
            break
    stop_task(task['pid'])
    activeServer = sorted(activeServer, key=lambda x: float(
        x['downloadSpeed']), reverse=True)
    for i in activeServer:
        clashFile += f'{i["connectionUrl"]}\n'
        serverfile += f'{i}\n'

    encoded_bytes = base64.b64encode(clashFile.encode('utf-8'))
    encoded_string = encoded_bytes.decode('utf-8')
    with open("./serverlist.txt", 'w', encoding='utf-8') as f:
        f.write(serverfile)

    with open("./clashfile.txt", 'w', encoding='utf-8') as f:
        f.write(encoded_string)




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--limit','-L', type=int, default=10,
                        help='Limit value for processing')

    args = parser.parse_args()

    asyncio.run(main(args.limit))
