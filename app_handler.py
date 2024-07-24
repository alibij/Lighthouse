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
from xray_tester import XrayTesterWorker, Signals

config = ConfigManager(filename='./config', encode=False)


class AppLookUpWorker(QThread):
    connect_btn_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._stop_event = asyncio.Event()

    def run(self):
        asyncio.run(self.async_run())

    async def async_run(self):
        while True:
            self._config = config.read()
            if self._config.last_xray_pid > 0 and \
                    chek_task(self._config.last_xray_pid):
                self.connect_btn_signal.emit('Disconnect')
            else:
                self.connect_btn_signal.emit('Connect')
            await asyncio.sleep(1)

    def disconnect_vpn(self):
        config.write(ConfigData(last_xray_pid=0))
        stop_task(self._config.last_xray_pid)

    def stop_worker(self):
        self._stop_event.set()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.xray_tester_worker = XrayTesterWorker()
        self.app_look_up_worker = AppLookUpWorker()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('LightHouse VPN')
        self.setFixedSize(300, 400)

        self.label = QLabel("Waiting for ...")

        self.progress_bar = QProgressBar()

        self.connect_btn = QPushButton()
        self.connect_btn.clicked.connect(self.handle_connect)

        self.exit_btn = QPushButton('Exit')
        self.exit_btn.clicked.connect(self.close)

        self.app_lookup_connect()

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.connect_btn)
        layout.addWidget(self.exit_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    @pyqtSlot(str)
    def update_label(self, message):
        self.label.setText(message)

    @pyqtSlot(int)
    def update_progress(self, value):
        self.progress_bar.setValue(value)

    @pyqtSlot(str)
    def update_connect_btn(self, value):
        self.connect_btn.setText(value)

    def app_lookup_connect(self):
        if not self.app_look_up_worker.isRunning():
            self.app_look_up_worker.connect_btn_signal.connect(
                self.update_connect_btn)
            self.app_look_up_worker.start()

    def handle_connect(self):
        if self.connect_btn.text() == 'Connect':
            self.connect_btn.setText('Disconnect')
            self.xray_tester_connect()
        else:
            self.connect_btn.setText('Connect')
            self.disconnect_vpn()

    def xray_tester_connect(self):
        if not self. xray_tester_worker.isRunning():
            self.xray_tester_worker.signals.label_signal.connect(
                self.update_label)
            self.xray_tester_worker.signals.progress_signal.connect(
                self.update_progress)
            self.xray_tester_worker.start()

    def disconnect_vpn(self):
        if self.xray_tester_worker.isRunning():
            self.xray_tester_worker.stop_worker()
            self.xray_tester_worker.wait()

        if self.app_look_up_worker.isRunning():
            self.app_look_up_worker.disconnect_vpn()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
