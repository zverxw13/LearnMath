# -*- coding: utf-8 -*-

"""Main module for LearnMath applications."""

import ctypes
import sys

import PyQt5.QtWidgets

import LM_Utils
from LearnMathGui import LearnMathGui

logger = LM_Utils.create_logger_for_screen_and_file("learn_math_log.txt")


if __name__ == "__main__":

    try:
        app = PyQt5.QtWidgets.QApplication(sys.argv)
        myapp = LearnMathGui()

        my_app_id = "mj.learn_math.lm.1"  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)
        app.setQuitOnLastWindowClosed(False)

        myapp.show()
        sys.exit(app.exec_())
    except Exception as ex:
        print(ex)
        raise
