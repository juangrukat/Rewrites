# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
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
from PySide6.QtWidgets import (QApplication, QComboBox, QLabel, QMainWindow,
    QMenuBar, QPlainTextEdit, QPushButton, QSizePolicy,
    QStatusBar, QTabWidget, QTextEdit, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1024, 768)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.Tabs = QTabWidget(self.centralwidget)
        self.Tabs.setObjectName(u"Tabs")
        self.Tabs.setGeometry(QRect(20, 40, 1021, 721))
        self.WorkArea = QWidget()
        self.WorkArea.setObjectName(u"WorkArea")
        self.Excerpts = QTextEdit(self.WorkArea)
        self.Excerpts.setObjectName(u"Excerpts")
        self.Excerpts.setGeometry(QRect(10, 80, 591, 141))
        self.Rewrites = QTextEdit(self.WorkArea)
        self.Rewrites.setObjectName(u"Rewrites")
        self.Rewrites.setGeometry(QRect(10, 260, 591, 141))
        self.analysis = QTextEdit(self.WorkArea)
        self.analysis.setObjectName(u"analysis")
        self.analysis.setGeometry(QRect(650, 80, 331, 321))
        self.sendopenai = QPushButton(self.WorkArea)
        self.sendopenai.setObjectName(u"sendopenai")
        self.sendopenai.setGeometry(QRect(10, 410, 100, 32))
        self.airesponse = QTextEdit(self.WorkArea)
        self.airesponse.setObjectName(u"airesponse")
        self.airesponse.setGeometry(QRect(10, 470, 971, 171))
        self.label_excerpt = QLabel(self.WorkArea)
        self.label_excerpt.setObjectName(u"label_excerpt")
        self.label_excerpt.setGeometry(QRect(280, 60, 101, 16))
        self.label_rewrite = QLabel(self.WorkArea)
        self.label_rewrite.setObjectName(u"label_rewrite")
        self.label_rewrite.setGeometry(QRect(300, 240, 58, 16))
        self.label_analysis = QLabel(self.WorkArea)
        self.label_analysis.setObjectName(u"label_analysis")
        self.label_analysis.setGeometry(QRect(780, 50, 58, 16))
        self.label_airesponse = QLabel(self.WorkArea)
        self.label_airesponse.setObjectName(u"label_airesponse")
        self.label_airesponse.setGeometry(QRect(460, 450, 81, 16))
        self.pushButton_random = QPushButton(self.WorkArea)
        self.pushButton_random.setObjectName(u"pushButton_random")
        self.pushButton_random.setGeometry(QRect(10, 40, 100, 32))
        self.Tabs.addTab(self.WorkArea, "")
        self.Settings = QWidget()
        self.Settings.setObjectName(u"Settings")
        from PySide6.QtWidgets import QLineEdit
        self.apifield = QLineEdit(self.Settings)
        self.apifield.setObjectName(u"apifield")
        self.apifield.setGeometry(QRect(30, 50, 421, 31))
        self.apifield.setEchoMode(QLineEdit.Password)
        self.apisave = QPushButton(self.Settings)
        self.apisave.setObjectName(u"apisave")
        self.apisave.setGeometry(QRect(30, 100, 100, 32))
        self.comboBox_prompt = QComboBox(self.Settings)
        self.comboBox_prompt.setObjectName(u"comboBox_prompt")
        self.comboBox_prompt.setGeometry(QRect(40, 220, 103, 32))
        self.Tabs.addTab(self.Settings, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1024, 24))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.Tabs.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.sendopenai.setText(QCoreApplication.translate("MainWindow", u"Send to AI", None))
        self.label_excerpt.setText(QCoreApplication.translate("MainWindow", u"Original Excerpt", None))
        self.label_rewrite.setText(QCoreApplication.translate("MainWindow", u"Rewrite", None))
        self.label_analysis.setText(QCoreApplication.translate("MainWindow", u"Analysis", None))
        self.label_airesponse.setText(QCoreApplication.translate("MainWindow", u"AI Response", None))
        self.pushButton_random.setText(QCoreApplication.translate("MainWindow", u"Get Random", None))
        self.Tabs.setTabText(self.Tabs.indexOf(self.WorkArea), QCoreApplication.translate("MainWindow", u"Work Area", None))
        self.apisave.setText(QCoreApplication.translate("MainWindow", u"Save API", None))
        self.Tabs.setTabText(self.Tabs.indexOf(self.Settings), QCoreApplication.translate("MainWindow", u"Settings", None))
    # retranslateUi

