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

    task = start_core(config_file_path='./testconfig.json')

    print('Getting the best server suitable for your internet')

    servers = await testPing(proxies=[f'http://localhost:{i}' for i in range(file['startPort'], file['lastPort']+1)])

    proxies = {}
    for i, ping in enumerate(servers):
        port = i+file['startPort']
        proxies[port] = {'port': port, 'proxyUrl': f'http://localhost:{port}',
                         'connectionUrl': await removeRemark(file['serverList'][i], i),
                         'ping': ping, 'downloadSpeed': 0}

    clashFile = ''
    serverfile = ''
    activeServer = []
    for i in proxies:
        if proxies[i]['ping'] > 0:
            activeServer.append(proxies[i])

    activeServer = sorted(activeServer, key=lambda x: x['ping'])
    highestserver = {}
    speed = 0.00
    netspeed = await speedTest()

    for i, server in enumerate(activeServer):

        if i == test_limit or speed >= (netspeed*speedtelorance):

            connect_to_fastest(highestserver['connectionUrl'])
            break

        activeServer[i]['downloadSpeed'] = await speedTest(proxy=server['proxyUrl'])
        speed = activeServer[i]['downloadSpeed']

        if 'downloadSpeed' not in highestserver:
            highestserver = server
        else:
            highestserver = server if server['downloadSpeed'] > highestserver['downloadSpeed'] else highestserver

        clear()
        print(f'Current Speed is : {netspeed} MB/s')
        print(f'highest server speed is {highestserver["downloadSpeed"]} MB/s')
        print(f'current server speed is {speed} MB/s')

        serverlen = test_limit if (test_limit > 0 and test_limit <= len(
            activeServer)) else len(activeServer)

        print_loading_bar(i+1, 0,serverlen)

    stop_task(task['pid'])
    activeServer = sorted(
        activeServer, key=lambda x: x['downloadSpeed'], reverse=True)
    for i in activeServer:
        clashFile += f'{i["connectionUrl"]}\n'
        serverfile += f'{i}\n'

    encoded_bytes = base64.b64encode(clashFile.encode('utf-8'))
    encoded_string = encoded_bytes.decode('utf-8')

    make_file(serverfile, "./serverlist.txt")
    make_file(encoded_string, "./clashfile.txt")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--limit','-L', type=int, default=10,
                        help='Limit value for processing')

    args = parser.parse_args()

    asyncio.run(main(args.limit))
