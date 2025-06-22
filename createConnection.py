import createServerFile
import argparse
import os
from speedtest import speedTest
import base64
import asyncio
from common import *
from createConfig import fetch_and_decode_data, create_config, main_config, read_local_file
from managertask import start_core, stop_task, find_xray_pid
from getData import testPing
from url2json import generateConfig


async def connect_to_fastest(url, config):

    if pid := find_xray_pid():
        stop_task(pid)

    if main_config(url, http_port=config['http_port'],
                   socks5_port=config['socks_port'],
                   socks=config['socks']):
        start_core(config_file_path='./config.json')

        # ip_data = await get_ip_data(proxy=f'http://localhost:{config["http_port"]}')
        ip_data = local_ip_data(
            proxy=f'http://localhost:{config["http_port"]}')

        clear()

        print(
            f'\nConnected to {ip_data["country"]} Server \nNow your IP is : {ip_data["ip"]}\n')


async def main(xray_config: dict, test_limit=-1,
               create_file=False, fecth_proxy: str = None,
               local_file: str = None, speed_test: bool = True,
               connect_to_fast: bool = True):
    clear()
    print('Getting the latest servers')
    print(connect_to_fast)
    server_list_url = "https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/Eternity"
    fetch_list = read_local_file(
        local_file) if local_file else fetch_and_decode_data(server_list_url, proxy=fecth_proxy)
    if not fetch_list:
        clear()
        print("LightHouse can't find server")
        return

    file = create_config(fetch_list)

    task = start_core(config_file_path='./testconfig.json')

    print('Getting the best server suitable for your internet')

    servers = await testPing(proxies=[f'http://localhost:{i}' for i in range(file['startPort'], file['lastPort']+1)])
    proxies = {}
    for i, ping in enumerate(servers):
        port = i+file['startPort']
        proxies[port] = {'port': port, 'proxyUrl': f'http://localhost:{port}',
                         'connectionUrl': await removeRemark(file['serverList'][i], i),
                         'ping': ping, 'downloadSpeed': 0}

    activeServer = []
    for i in proxies:
        if proxies[i]['ping'] > 0:
            activeServer.append(proxies[i])
    if not len(activeServer) > 0:
        clear()
        print("All servers is not available")
        return
    activeServer = sorted(activeServer, key=lambda x: x['ping'])
    highestserver = {}
    speed = 0.00
    if speed_test:
        for i, server in enumerate(activeServer):

            if i > test_limit and test_limit > 0:
                break

            activeServer[i]['downloadSpeed'] = await speedTest(proxy=server['proxyUrl'])
            speed = activeServer[i]['downloadSpeed']

            if 'downloadSpeed' not in highestserver:
                highestserver = server
            else:
                highestserver = server if server['downloadSpeed'] > highestserver['downloadSpeed'] else highestserver

            clear()
            # print(f'Current Speed is : {netspeed} MB/s')
            print(
                f'highest server speed is {highestserver["downloadSpeed"]} MB/s')
            print(f'current server speed is {speed} MB/s')

            serverlen = test_limit if (test_limit > 0 and test_limit <= len(
                activeServer)) else len(activeServer)

            print_loading_bar(i+1, 0, serverlen)

    stop_task(task['pid'])
    if connect_to_fast:
        await connect_to_fastest(highestserver['connectionUrl'], xray_config)

    if create_file:
        s = generateConfig(highestserver['connectionUrl'])
        with open("./fast.json", 'w') as f:
            json.dump(s, f, indent=4)
        createServerFile.server_list_file(activeServer)

    clear()
    print("Task completed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')

    parser.add_argument('--limit', '-l', type=int, default=10,
                        help='Limit server for testing default no limit')

    parser.add_argument('--makefile', '-o', action='store_true', default=False,
                        help='Create a file from the list of active servers default=False')

    parser.add_argument('--httpport', type=int, default=1081,
                        help='http port default=1081 if create connection')

    parser.add_argument('--socksport', type=int, default=1080,
                        help='http port default=1080 if create connection')

    parser.add_argument('--fetchproxy', '-p', type=str, default=None,
                        help='set "http" proxy for fetch server data')

    parser.add_argument('--connect', action='store_true',
                        help='Create a connection to fast server')

    parser.add_argument('--localfile', '-f', type=str, default=None,
                        help='Use local server file')

    parser.add_argument('--speed_test', '-T', type=str, default="RDST",
                        help='set test metod | "RDST" > mix mode for ping, real delay and speed test'
                        '| "PD" > ping and real delay test '
                        )

    args = parser.parse_args()
    xray_setting = {
        # 'http': not args.disablehttp,
        #     'socks': not args.disablesocks,
        #     'http_port': args.httpport,
        #     'socks_port': args.socksport
    }

    if args.localfile and not os.path.exists(args.localfile):
        print("File address not valid")
        exit()
    asyncio.run(main(test_limit=args.limit,
                     create_file=args.makefile, xray_config=xray_setting,
                     fecth_proxy=args.fetchproxy, local_file=args.localfile,
                     speed_test=True if args.speed_test == "RDST" else False,
                     connect_to_fast=args.connect))
