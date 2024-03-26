import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QMessageBox, QMainWindow, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap
from PyQt5.Qt import Qt, QSize
import shutil
import os
class InstallProgram(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Установка компонентов")
        self.setWindowIcon(QIcon('/opt/AppInstaller/icon.svg'))
        self.setGeometry(100, 100, 400, 200)
        self.setFixedSize(450, 190)
        
        self.label = QLabel(self)
        pixmap = QPixmap('/opt/AppInstaller/dnd.png')
        self.label.setPixmap(pixmap)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.move(0, 0)

        self.button = QPushButton("Справка", self)
        self.button.setGeometry(195, 165, 60, 15)
        self.button.clicked.connect(self.showMessageBox)

        self.label = QLabel(self)
        self.label.setText("Для установки программы, перетащите сюда .epf файл")
        self.label.move(50, 145)
        
        self.setAcceptDrops(True)
        
    def removetemp(self):
        os.remove("/tmp/info.txt")
        os.remove("/tmp/" + self.desktop_name)
        os.remove("/tmp/icon.png")
        os.remove("/tmp/necessary.txt")
        shutil.rmtree("/tmp/" + self.folder_name)
# NO!!!!!!!!=====================================================
    def nobtn(self):
        self.removetemp()
        QApplication.quit()
# YES !!!!!!=====================================================
    def yesbtn(self):
        folder_path_opt = "/opt/" + self.folder_name
        file_path_desktop = "/usr/share/applications/" + self.desktop_name
        if os.path.exists(folder_path_opt):
            shutil.rmtree(folder_path_opt)

        if os.path.exists(file_path_desktop):
            os.remove(file_path_desktop)
        shutil.copytree("/tmp/" + self.folder_name, "/opt/" + self.folder_name)
        shutil.copy("/tmp/" + self.desktop_name, "/usr/share/applications/" + self.desktop_name)
        os.system(self.script)
        info_box = QMessageBox(self)
        info_box.setWindowTitle('Установка')
        info_box.setText('Программа успешно установлена!')
        info_box.exec()
        
        self.removetemp()
        QApplication.quit()
        
    def closeEvent(self, event):
        self.removetemp()
        event.accept()
    def showMessageBox(self):
        msg = QMessageBox()
        msg.setWindowTitle("О программе")
        msg.setIcon(QMessageBox.Information)
        msg.setText("<br>Установка компонентов Elyzion <br>Авторы: <br>Игнатьев Илья <br>Crystal Project©</a> 2023-2024г.")
        msg.setStyleSheet("QLabel {color: white; font-size: 15px;}")
        pixmap = QPixmap("images/ES.png")
        msg.setIconPixmap(pixmap)
        msg.exec_()
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.endswith('.epf'):
                self.install_program(file_path)

    def necessary(self):
        try:
            with open('/tmp/necessary.txt', 'r') as file:
                content = file.read()
                QMessageBox.information(None, "Необходимые зависимости", content)
        except FileNotFoundError:
            QMessageBox.critical(None, "Ошибка", "Файл необходимых для программы зависимостей не найден, дальнейшая установка программы не рекомендуется.")

    def install_program(self, file_path):
        shutil.unpack_archive(file_path, "/tmp", format="tar")
        
        with open("/tmp/info.txt", "r", encoding="utf-8") as file:
            info = file.read().splitlines()
            program_name = info[0]
            publisher_name = info[1]
            self.folder_name = info[2]
            self.desktop_name = info[3]
            self.script = info[4]
        
        reply = QMainWindow(self)
        reply.setGeometry(100, 100, 400, 200)
        reply.setFixedSize(450, 190)
        reply.setWindowTitle('Установка компонентов')
        #reply.setIconPixmap(QIcon("/tmp/icon.png").pixmap(50, 50))
        centralwidget = QWidget(reply)
        centralwidget.setObjectName(u"centralwidget")
        verticalLayout = QVBoxLayout(centralwidget)
        verticalLayout.setObjectName(u"verticalLayout")
        label = QLabel(centralwidget)
        label.setText(f'Вы действительно хотите установить данное ПО?\nНазвание: {program_name}\nРазработчик: {publisher_name} ')
        label.setObjectName(u"label")

        verticalLayout.addWidget(label)
        horizontalLayout_2 = QHBoxLayout()
        horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        label_2 = QLabel(centralwidget)
        label_2.setObjectName(u"label_2")
        #label_2.setMaximumSize(QSize(64, 64))
        label_2.setPixmap(QIcon("/tmp/icon.png").pixmap(50, 50))

        horizontalLayout_2.addWidget(label_2)


       
        horizontalLayout_2.addWidget(label)
        verticalLayout.addLayout(horizontalLayout_2)



        horizontalLayout = QHBoxLayout()
        horizontalLayout.setObjectName(u"horizontalLayout")
        pushButton = QPushButton("Да", centralwidget)
        pushButton.clicked.connect(self.yesbtn)


        horizontalLayout.addWidget(pushButton)

        pushButton_2 = QPushButton("Нет", centralwidget)
        pushButton_2.setObjectName(u"pushButton_2")
        pushButton_2.clicked.connect(self.nobtn)

        horizontalLayout.addWidget(pushButton_2)

        pushButton_3 = QPushButton('Необходимые зависимости', centralwidget)
        pushButton_3.setObjectName(u"pushButton_3")
        pushButton_3.clicked.connect(self.necessary)

        horizontalLayout.addWidget(pushButton_3)


        verticalLayout.addLayout(horizontalLayout)

        reply.setCentralWidget(centralwidget)
        reply.closeEvent = self.closeEvent
        reply.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.black)
    palette.setColor(QPalette.Button, QColor(255, 255, 255))
    palette.setColor(QPalette.ButtonText, Qt.black)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(255, 255, 255))
    palette.setColor(QPalette.Highlight, QColor(255, 255 ,255))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)
    app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")
    
    install_program = InstallProgram()
    install_program.show()
    
    sys.exit(app.exec_())
