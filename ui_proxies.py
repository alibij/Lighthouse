# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'proxies.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QListView, QPushButton,
    QSizePolicy, QWidget)

class Ui_ProxiesWindow(object):
    def setupUi(self, ProxiesWindow):
        if not ProxiesWindow.objectName():
            ProxiesWindow.setObjectName(u"ProxiesWindow")
        ProxiesWindow.resize(384, 484)
        self.gridLayout = QGridLayout(ProxiesWindow)
        self.gridLayout.setObjectName(u"gridLayout")
        self.pingtestButton = QPushButton(ProxiesWindow)
        self.pingtestButton.setObjectName(u"pingtestButton")

        self.gridLayout.addWidget(self.pingtestButton, 1, 1, 1, 1)

        self.updateButton = QPushButton(ProxiesWindow)
        self.updateButton.setObjectName(u"updateButton")

        self.gridLayout.addWidget(self.updateButton, 1, 0, 1, 1)

        self.proxiesView = QListView(ProxiesWindow)
        self.proxiesView.setObjectName(u"proxiesView")

        self.gridLayout.addWidget(self.proxiesView, 0, 0, 1, 2)


        self.retranslateUi(ProxiesWindow)

        QMetaObject.connectSlotsByName(ProxiesWindow)
    # setupUi

    def retranslateUi(self, ProxiesWindow):
        ProxiesWindow.setWindowTitle(QCoreApplication.translate("ProxiesWindow", u"Proxies", None))
        self.pingtestButton.setText(QCoreApplication.translate("ProxiesWindow", u"Ping Test", None))
        self.updateButton.setText(QCoreApplication.translate("ProxiesWindow", u"Update", None))
    # retranslateUi

