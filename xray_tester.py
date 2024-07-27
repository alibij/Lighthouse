import sys
import asyncio
from PyQt5.QtCore import QThread, pyqtSignal, QObject, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QProgressBar, QWidget

# Placeholder imports
from config import ConfigManager, ConfigData
from managertask import start_core, stop_task, chek_task
from createConfig import fetch_and_decode_data, create_config, main_config
from speedtest import speedTest
from getPing import testPing
import createServerFile
from common import *


config = ConfigManager(filename='./config', encode=False)


class Signals(QObject):
    label_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)


class XrayTesterWorker(QThread):
    def __init__(self):
        super().__init__()
        self.signals = Signals()
        self._stop_event = asyncio.Event()

    async def connect_to_fastest(self, url, config):
        if main_config(url, http_port=config['http_port'], socks5_port=config['socks_port'], socks=config['socks']):
            self._task = start_core(config_file_path='./config.json')
            ip_data = await get_ip_data(proxy=f'http://localhost:{config["http_port"]}')
            if ip_data:
                self.signals.label_signal.emit(
                    f'\nConnected to {ip_data["country"]}\n\nNow your IP is :\n  {ip_data["ip"]}\n')
            else:
                self.signals.label_signal.emit(
                    "Connected\nCan't get ip"
                )
            return self._task

    async def async_run(self, xray_config, test_limit, speed_tolerance, create_file):
        self.signals.label_signal.emit('Getting the latest servers')

        file = create_config(fetch_and_decode_data(
            'https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/sub/sub_merge.txt',
            False
        ))
        self._task = start_core(config_file_path='./testconfig.json')

        self.signals.label_signal.emit(
            'Getting the best server suitable for your internet')

        servers = await testPing(
            proxies=[f'http://localhost:{i}' for i in range(
                file['startPort'],
                file['lastPort'] + 1)]
        )
        proxies = {
            i + file['startPort']: {
                'port': i + file['startPort'],
                'proxyUrl': f'http://localhost:{i + file["startPort"]}',
                'connectionUrl': await removeRemark(file['serverList'][i], i),
                'ping': ping,
                'downloadSpeed': 0
            }
            for i, ping in enumerate(servers)
        }

        activeServer = [proxies[i] for i in proxies if proxies[i]['ping'] > 0]
        activeServer.sort(key=lambda x: x['ping'])
        print(len(servers), len(activeServer))
        highest_server = {}
        speed = 0.00
        net_speed = await speedTest()

        for i, server in enumerate(activeServer):
            if self._stop_event.is_set():
                self.signals.label_signal.emit('Waiting for ...')
                self.signals.progress_signal.emit(0)
                stop_task(self._task['pid'])
                return

            if i == test_limit or speed >= (net_speed * speed_tolerance):
                break

            activeServer[i]['downloadSpeed'] = await speedTest(proxy=server['proxyUrl'])
            speed = activeServer[i]['downloadSpeed']

            highest_server = server if 'downloadSpeed' not in highest_server or server[
                'downloadSpeed'] > highest_server['downloadSpeed'] else highest_server

            t = f'Current Speed is : {net_speed} MB/s'
            t += f'\nhighest server speed is {highest_server["downloadSpeed"]} MB/s'
            t += f'\ncurrent server speed is {speed} MB/s'

            self.signals.label_signal.emit(t)

            server_len = min(test_limit, len(activeServer)
                             ) if test_limit > 0 else len(activeServer)
            self.signals.progress_signal.emit(
                int((100 * (i + 1)) / server_len))

        stop_task(self._task['pid'])
        self.signals.progress_signal.emit(100)

        t = await self.connect_to_fastest(highest_server['connectionUrl'], xray_config)
        config.write(ConfigData(last_xray_pid=t['pid']))
        if create_file:
            createServerFile.server_list_file(activeServer)

    def run(self):
        asyncio.run(self.async_run(
            xray_config=config.read().xray_config.dict(),
            test_limit=config.read().test_limit,
            speed_tolerance=config.read().speed_tolerance,
            create_file=config.read().create_file))

    def stop_worker(self):
        self._stop_event.set()
