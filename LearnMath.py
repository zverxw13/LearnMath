# -*- coding: utf-8 -*-

import sys
import ctypes
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QWidget, QApplication
import LM_Utils

from LearnMathGui import LearnMathGui

logger = LM_Utils.createLoggerForScreenAndFile("learn_math_log.txt")

if __name__ == "__main__":

    try:
        app = QApplication(sys.argv)
        myapp = LearnMathGui()

        myappid = 'mj.learn_math.lm.1' # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        app.setQuitOnLastWindowClosed(False)

        myapp.show()
        sys.exit(app.exec_())
    except Exception as ex:
        print(ex)
