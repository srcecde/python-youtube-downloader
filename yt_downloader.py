"""
Python YoutTube Video Downloader
========================
Developed by: Chirag Rathod (Srce Cde)
Email: chiragr83@gmail.com
========================
"""
import os
import itertools
import sys
import threading
from pytube import *
from PyQt5 import QtCore, QtGui as qt, QtWidgets as qw
from PyQt5.QtCore import QObject, pyqtSignal

#Setting Path to save the Downloaded Videos
exp_user = os.path.expanduser("~")
op = os.path.join(exp_user, "Downloads", "YouTube Videos")
vid = str()


class MainUi(qw.QMainWindow):
    def __init__(self):
        super(MainUi, self).__init__()
        threading.Thread.__init__(self)
        self.setGeometry(50, 50, 700, 500)
        self.setWindowTitle("YouTube Video Downloader")

        # Setting style of the Qt Window
        qw.QApplication.setStyle(qw.QStyleFactory.create("Plastique"))

        hfont = qt.QFont()
        hfont.setBold(True)
        hfont.setPointSize(18)

        nfont = qt.QFont()
        nfont.setBold(True)

        self.enter_url_label = qw.QLabel("Enter the YouTube video URL to download", self)
        self.enter_url_label.setFont(hfont)
        self.enter_url_label.resize(self.enter_url_label.minimumSizeHint())
        self.enter_url_label.move(20, 20)

        self.enter_url_txt = qw.QLineEdit(self)
        self.enter_url_txt.setFixedWidth(400)
        self.enter_url_txt.move(20, 65)

        self.vid_status_label = qw.QLabel("Available", self)
        self.pixmap = qt.QPixmap("favicon.ico")
        self.vid_status_label.setPixmap(self.pixmap)
        self.vid_status_label.setFont(hfont)
        self.vid_status_label.resize(self.vid_status_label.minimumSizeHint())
        self.vid_status_label.move(430, 65)
        self.vid_status_label.setVisible(True)

        self.chk_availability = qw.QPushButton("Check Availibilty", self)
        self.chk_availability.resize(self.chk_availability.minimumSizeHint())
        self.chk_availability.move(470, 65)
        self.chk_availability.clicked.connect(lambda: check_avail(self))

        self.download_quality = qw.QLabel("Download Quality", self)
        self.download_quality.setFont(nfont)
        self.download_quality.resize(self.download_quality.minimumSizeHint())
        self.download_quality.move(20, 120)

        self.resoution_list = qw.QComboBox(self)
        self.resoution_list.move(170, 113)

        self.download_button = qw.QPushButton("Download", self)
        self.download_button.setStyleSheet('color: blue')
        self.download_button.resize(self.download_button.minimumSizeHint())
        self.download_button.setGeometry(370, 113, 150, 50)
        self.download_button.clicked.connect(lambda: download(self))

        self.progress = qw.QProgressBar(self)
        self.progress.setGeometry(20, 190, 500, 20)

        self.resoution_list.currentIndexChanged.connect(self.selectionchange)

    def handle_trigger(self):
        # This function will be called when download is completed
        InfoMessage(self, "The Video has been downloaded at Downloads/YouTube Videos")

    def selectionchange(self):
        # Setting up resolution and extension
        selected_resolution = []
        selected_resolution.append(self.resoution_list.currentText())
        split_lst = [i.split(' - ') for i in selected_resolution]
        self.split_lst2 = list(itertools.chain.from_iterable(split_lst))


def ErrorMessage(self, text):

    choice = qw.QMessageBox.information(self, "Error!",
                                    text,
                                    qw.QMessageBox.Ok)
    if(choice == qw.QMessageBox.Ok):
        pass
    else:
        pass


def InfoMessage(self, text):

    choice = qw.QMessageBox.information(self, "Information!",
                                    text,
                                    qw.QMessageBox.Ok)
    if(choice == qw.QMessageBox.Ok):
        pass
    else:
        pass


def download(self):
    global vid
    vid_url = s_url(self)
    vid = vid_url.get(self.split_lst2[0], self.split_lst2[1])

    if not os.path.exists(op):
        os.makedirs(op)

    InfoMessage(self, "Downloading Video!!! You will be informed when done")

    # Triggering download process on the sub thread to avoid freezing of UI
    self.threadclass = ThreadDwn()
    # The below will be triggered when ThreadDwn class will emit the signal
    self.threadclass.trig.connect(lambda: MainUi.handle_trigger(self))
    self.threadclass.start()


class ThreadDwn(QtCore.QThread, qw.QMainWindow):
    global vid
    trig = pyqtSignal()

    def __init__(self):
        super(ThreadDwn, self).__init__()

    def run(self):
        # Downloading Video
        vid.download(op)
        # Emit the signal when downloading is finished
        self.trig.emit()


def check_avail(self):
    vid_url = s_url(self)
    files = vid_url.get_videos()
    v_list = []
    for f in files:
        v_extn = f.extension
        v_resol = f.resolution
        v_list.append((v_extn, v_resol))

    for item in v_list:
        self.resoution_list.addItem(item[0] + " - " + item[1])

    return vid_url


def s_url(self):
    # Getting URL from text box
    vid_url = YouTube(self.enter_url_txt.text())
    return vid_url


def main():
    app = qw.QApplication(sys.argv)

    Mobj = MainUi()

    Mobj.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
