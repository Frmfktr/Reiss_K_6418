from PyQt5 import QtGui, QtWidgets, uic
from protocol import K6418
from serial.tools.list_ports import comports
import sys

class GUI(QtWidgets.QMainWindow):

    def __init__(self):
        super(GUI, self).__init__()
        uic.loadUi('GUI.ui', self)
        self.init_widgets()
        self.find_ports()
        self.show()

    def init_widgets(self):
        self.port_list = self.findChild(QtWidgets.QComboBox, 'port_list')
        self.refresh_btn = self.findChild(QtWidgets.QPushButton, 'refresh_btn')
        self.refresh_btn.clicked.connect(self.refresh_ports)

        self.file_bnt = self.findChild(QtWidgets.QPushButton, 'file_btn')
        self.file_edit = self.findChild(QtWidgets.QLineEdit, 'file_edit')
        self.file_btn.clicked.connect(self.select_file)

        self.start_btn = self.findChild(QtWidgets.QPushButton, 'start_btn')
        self.start_btn.clicked.connect(self.start)

    def start(self):
        port = self.port_list.currentText()
        f = self.file_edit.text()
        if not port == "" and not f == "":
            print(port)
        else:
            if port == "":
                print("kein port vorhanden!")
            if f == "":
                print("keine Datei ausgewählt!")

    def select_file(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '',"HPGL Files (*.hpgl)")
        if not fname == None:
            self.file_edit.setText(fname[0])

    def find_ports(self):
        ports = list(comports())
        for port in ports:
            self.port_list.addItem(port.device)

    def refresh_ports(self):
        self.port_list.clear()
        self.find_ports()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    gui = GUI()
    sys.exit(app.exec_())
