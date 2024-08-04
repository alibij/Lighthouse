# This Python file uses the following encoding: utf-8
import sys
import base64

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtCore import QAbstractListModel, Qt, QUrl, Slot, QThread, Signal
from PySide6.QtGui import QImage
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
# from ui_form import Ui_MainWindow
from ui_main import Ui_MainWindow
from ui_proxies import Ui_ProxiesWindow
from ui_settings import Ui_SettingsWindow

from config import ConfigManager
# from xray import create_config
from url2json import *
# from getPing import *


tick = QImage("tick.png")


class ProxyModel(QAbstractListModel):
    def __init__(self, proxies=None):
        super().__init__()
        self.proxies = proxies or []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            remark, _ = self.proxies[index.row()]
            return remark

        # if role == Qt.DecorationRole:
        #     status, _ = self.todos[index.row()]
        #     if status:
        #         return tick

    def rowCount(self, index):
        return len(self.proxies)


# class PingTestThread(QThread):
#     result_ready = Signal()

#     def run(self):
#         self.config = ConfigManager.get_instance()

#         file = create_config([c for (_, c) in self.config.get('proxies')])

#         self._task = start_core(config_file_path='./testconfig.json')

#         servers = await testPing(
#             proxies=[f'http://localhost:{i}' for i in range(
#                 file['startPort'],
#                 file['lastPort'] + 1)]
#         )
#         print(servers)

#         self.result_ready.emit()

class SettingsWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """

    def __init__(self):
        super().__init__()
        self.config = ConfigManager.get_instance()

        self.ui = Ui_SettingsWindow()
        self.ui.setupUi(self)



class ProxiesWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """

    def __init__(self, model):
        super().__init__()
        self.config = ConfigManager.get_instance()

        self.ui = Ui_ProxiesWindow()
        self.ui.setupUi(self)

        self.model = model
        self.ui.proxiesView.setModel(self.model)
        self.update_proxies_view()

        self.network_manager = QNetworkAccessManager(self)
        self.ui.updateButton.clicked.connect(self.update_button_click)

        self.ui.pingtestButton.clicked.connect(self.pingtest_button_click)

    @Slot()
    def update_proxies_view(self):
        if p := self.config.get('proxies'):
            self.model.proxies = p
        self.model.layoutChanged.emit()

    @Slot()
    def pingtest_button_click(self):
        # self.ping_test_thread = PingTestThread()
        # self.ping_test_thread.result_ready.connect(self.update_proxies_view)
        # self.ping_test_thread.start()
        pass

    @Slot()
    def update_button_click(self):
        # Replace with your URL
        url = QUrl(
            "https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/Eternity")
        request = QNetworkRequest(url)

        # Send the request asynchronously
        self.network_reply = self.network_manager.get(request)

        # Connect the finished signal to a slot
        self.network_reply.finished.connect(self.handle_network_reply)

    @Slot()
    def handle_network_reply(self):
        proxies = []
        if self.network_reply.error() == QNetworkReply.NoError:
            response_data = self.network_reply.readAll().data().decode()
            decoded_data = base64.b64decode(
                response_data).decode(
                encoding="utf-8", errors="ignore")
            for p in decoded_data.strip().split('\n'):
                if c := generateConfig(p):
                    proxies.append((c['_comment']['remark'], c))

            self.config.set('proxies', proxies)
            self.update_proxies_view()

        else:
            print("Network request failed:", self.network_reply.errorString())

        # Clean up
        self.network_reply.deleteLater()


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = ConfigManager.get_instance()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.windows = {}
        self.ui.update_sub_btn.clicked.connect(self.proxyWS)
        self.ui.settings_btn.clicked.connect(self.settingsWS)

    def proxyWS(self):
        self.model = ProxyModel()
        if 'proxy' not in self.windows:
            self.windows['proxy'] = ProxiesWindow(model=self.model)
        self.windows['proxy'].show()


    def settingsWS(self):
        if 'settings' not in self.windows:
            self.windows['settings'] = SettingsWindow()
        self.windows['settings'].show()


    def closeEvent(self, event):
        # Perform the save operation before closing
        for win in self.windows.values():
            win.close()
        self.config.save_config()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
