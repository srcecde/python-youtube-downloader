import unittest
import sys
import os
from PyQt5 import QtCore, QtGui as qt, QtWidgets as qw

try:
    sys.path.insert(0, os.path.abspath('..'))
    from yt_downloader import MainUi, check_avail, download, InfoMessage
except Exception as e:
    sys.path.insert(0, os.path.abspath('.'))
    from yt_downloader import MainUi, check_avail, download, InfoMessage


class test_yt(unittest.TestCase):

    def test_yt_dwn(self):
        app = qw.QApplication(sys.argv)
        y = MainUi()

        @unittest.skip("Popup message skipping")
        def ski(self):
            print("Called")

            InfoMessage(y)

        check_avail(y)

        ski()
        download(y)


if __name__ == '__main__':
    unittest.main()
