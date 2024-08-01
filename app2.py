
import asyncio
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QTextEdit, QProgressBar, QVBoxLayout
from PyQt5.QtGui import QIcon
from config import ConfigManager, ConfigData
from managertask import start_core, stop_task, find_xray_pid, chek_task
from createConfig import fetch_and_decode_data, create_config, main_config
from speedtest import speedTest
from getPing import testPing
import createServerFile
from common import *


config = ConfigManager(filename='./config', encode=True)


def connection_status():
    a = config.read()
    return True if a.last_xray_pid > 0 and chek_task(a.last_xray_pid) else False


def connection_button():

    if connection_status():
        on_disconnect()
        connect_button.setText('Connect')

    else:
        on_connect()
        connect_button.setText('Disconnect')


def on_connect():

    conf = config.read()
    asyncio.run(make_connection(test_limit=conf.test_limit, speed_tolerance=conf.speed_tolerance,
                create_file=conf.create_file, xray_config=conf.xray_config.dict()))


def on_disconnect():
    pid = config.read().last_xray_pid
    stop_task(pid)
    config.write(ConfigData(last_xray_pid=0))
    clear_log()


def clear_log():
    log_area.clear()


def update_progress_bar(value):
    progress_bar.setValue(value)
    progress_bar.setFormat(f'{value}%')
    QApplication.processEvents()


async def connect_to_fastest(url, config):

    if main_config(url, http_port=config['http_port'], socks5_port=config['socks_port'], socks=config['socks']):
        task = start_core(config_file_path='./config.json')
        ip_data = await get_ip_data(proxy=f'http://localhost:{config["http_port"]}')
        clear_log()
        log_area.append(
            f'\nConnected to {ip_data["country"]} Server \nNow your IP is : {ip_data["ip"]}\n')
        return task


async def make_connection(xray_config, test_limit, speed_tolerance, create_file):
    clear_log()
    log_area.append('Getting the latest servers')
    file = create_config(fetch_and_decode_data())
    task = start_core(config_file_path='./testconfig.json')

    log_area.append('Getting the best server suitable for your internet')

    servers = await testPing(proxies=[f'http://localhost:{i}' for i in range(file['startPort'], file['lastPort'] + 1)])
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

    highest_server = {}
    speed = 0.00
    net_speed = await speedTest()

    for i, server in enumerate(activeServer):
        if i == test_limit or speed >= (net_speed * speed_tolerance):
            break

        activeServer[i]['downloadSpeed'] = await speedTest(proxy=server['proxyUrl'])
        speed = activeServer[i]['downloadSpeed']

        highest_server = server if 'downloadSpeed' not in highest_server or server[
            'downloadSpeed'] > highest_server['downloadSpeed'] else highest_server

        clear_log()
        log_area.append(f'Current Speed is : {net_speed} MB/s')
        log_area.append(
            f'highest server speed is {highest_server["downloadSpeed"]} MB/s')
        log_area.append(f'current server speed is {speed} MB/s')

        server_len = min(test_limit, len(activeServer)
                         ) if test_limit > 0 else len(activeServer)
        update_progress_bar(int((100 * (i + 1)) / server_len))
        await asyncio.sleep(.1)

    stop_task(task['pid'])
    update_progress_bar(100)

    t = await connect_to_fastest(highest_server['connectionUrl'], xray_config)
    config.write(ConfigData(last_xray_pid=t['pid']))
    if create_file:
        createServerFile.server_list_file(activeServer)


def main():
    global log_area, progress_bar, connect_button
    app = QApplication(sys.argv)
    w, h = 200, 300

    window = QWidget()
    window.setWindowTitle('LightHouse VPN')
    window.setFixedSize(w, h)
    window.setWindowIcon(QIcon('./image.png'))

    layout = QVBoxLayout(window)

    log_area = QTextEdit(window)
    log_area.setReadOnly(True)
    progress_bar = QProgressBar(window)
    progress_bar.setTextVisible(True)

    # test_button = QPushButton('Test', window)
    connect_button = QPushButton(
        'disconnect'if connection_status() else 'Connect', window)
    exit_button = QPushButton('Exit', window)
    connect_button.clicked.connect(connection_button)
    # test_button.clicked.connect(clear_log)

    exit_button.clicked.connect(app.quit)

    layout.addWidget(log_area)
    layout.addWidget(progress_bar)
    # layout.addWidget(test_button)
    layout.addWidget(connect_button)
    layout.addWidget(exit_button)

    window.setLayout(layout)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
