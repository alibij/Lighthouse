
import asyncio
from PyQt5.QtCore import QThread, pyqtSignal

from config import ConfigManager, ConfigData
from managertask import stop_task, chek_task
from common import *


config = ConfigManager(filename='./config', encode=False)


class AppLookUpWorker(QThread):
    connect_btn_signal = pyqtSignal(str)
    update_lable_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._stop_event = asyncio.Event()
        self.update_ip_flag = True
        self.test_is_run = False

    def run(self):
        asyncio.run(self.async_run())

    async def async_run(self):

        while True:
            self._config = config.read()
            if self.update_ip_flag:
                self.update_ip_flag = False
                __is_connect = True if self._config.last_xray_pid > 0 and \
                    chek_task(self._config.last_xray_pid) else False
                __ip_data = await get_ip_data(
                    proxy=f'http://localhost:{self._config.xray_config.http_port}' if __is_connect else None)

            if self._config.last_xray_pid > 0 and \
                    chek_task(self._config.last_xray_pid) or self.test_is_run:
                self.connect_btn_signal.emit('Disconnect')

                if __ip_data and not self.test_is_run:
                    country = __ip_data["country"] if "country" in __ip_data else "Country Not Find"

                    self.update_lable_signal.emit(
                        f'\nConnected\n{country}\n\nYour IP\n{__ip_data["ip"]}\n')

            else:
                self.connect_btn_signal.emit('Connect')
                self.update_lable_signal.emit('LightHouse is ready to use')
            await asyncio.sleep(1)

    def disconnect_vpn(self):
        config.write(ConfigData(last_xray_pid=0))
        stop_task(self._config.last_xray_pid)

    def stop_worker(self):
        self._stop_event.set()

    def update_ip(self):
        self.update_ip_flag = True

    def runing_test(self, status: bool):
        self.test_is_run = status
