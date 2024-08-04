import sys
import asyncio
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QProgressBar, QWidget
from PyQt5.QtGui import QFontMetrics


# Placeholder imports
from config import ConfigManager, ConfigData
from managertask import stop_task, chek_task
from common import *
from xray_tester import XrayTesterWorker
from app_lookup import AppLookUpWorker

config = ConfigManager(filename='./config', encode=False)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.xray_tester_worker = XrayTesterWorker()
        self.app_look_up_worker = AppLookUpWorker()
        self._config = config.read()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('LightHouse VPN')
        self.setFixedSize(300, 400)

        self.label = QLabel("Waiting")
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignCenter)

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
            self.app_look_up_worker.update_lable_signal.connect(
                self.update_label)
            self.app_look_up_worker.start()

    def handle_connect(self):
        if check_internet():
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
            self.xray_tester_worker.signals.update_ip_signal.connect(
                self.app_look_up_worker.update_ip)
            self.xray_tester_worker.signals.test_is_runing.connect(
                self.app_look_up_worker.runing_test)
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
