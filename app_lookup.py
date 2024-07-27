
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

    def run(self):
        asyncio.run(self.async_run())

    async def async_run(self):
        self._config = config.read()
        __is_connect = True if self._config.last_xray_pid > 0 and \
            chek_task(self._config.last_xray_pid) else False
        __ip_data = await get_ip_data(
            proxy=f'http://localhost:{self._config.xray_config.http_port}' if __is_connect else None)

        while True:
            self._config = config.read()
            if self._config.last_xray_pid > 0 and \
                    chek_task(self._config.last_xray_pid):
                self.connect_btn_signal.emit('Disconnect')

                if __ip_data:
                    self.update_lable_signal.emit(
                        f'\nConnected to {__ip_data["country"]}\n\nNow your IP is :\n\t {__ip_data["ip"]}\n')
            else:
                self.connect_btn_signal.emit('Connect')
            await asyncio.sleep(1)

    def disconnect_vpn(self):
        config.write(ConfigData(last_xray_pid=0))
        stop_task(self._config.last_xray_pid)

    def stop_worker(self):
        self._stop_event.set()
