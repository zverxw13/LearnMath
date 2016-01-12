# -*- coding: utf-8 -*-

import sys
import sched
import time
import functools
import os
import glob

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QWidget, QApplication, QDialog, QTreeWidgetItem, QMainWindow, QLabel, QMessageBox, \
    QTextEdit
from PyQt5 import QtMultimedia

from ui_files.settings_dialog_ui import Ui_Dialog
from Game import *
from LearnMathGui import *


class DefaultConfigurationDialog(QDialog):
    cb_hints_values = ["Bez podpowiedzi", "Zawsze dostępne", "Max liczba podpowiedzi",
                       "Max liczba popdpowiedzi = % równań"]

    def __init__(self, parent=None, game_configuration=None):
        super(DefaultConfigurationDialog, self).__init__(parent)
        # QDialog.__init__(self, parent)

        # self.logger = LearnMathGui.logger
        self.game_configuration = game_configuration

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # set data for self.ui.comboBox_hints
        self.ui.comboBox_hints.addItems(self.cb_hints_values)
        self.ui.comboBox_hints.currentIndexChanged['QString'].connect(self.handleCbHintsChanged)

        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)

        self.setWindowTitle("Konfiguracja gier")

        if game_configuration is not None:
            self.setConfigurationData(game_configuration)

    def setConfigurationData(self, game_configuration=None):
        self.game_configuration = game_configuration
        if game_configuration is not None:
            s_c_question = str(game_configuration.default_equations)
            hints_mode = game_configuration.game_hints_mode
            print("in set game_configuration.game_hints_mode = ", game_configuration.game_hints_mode)
            hints_c = str(game_configuration.game_hints_value)
            print("...in setConfigurationData: starting, hints_c = ", hints_c)
            p_name = game_configuration.player_name

            snd = game_configuration.default_sound_on
            self.ui.checkBox_sounds.setChecked(snd)

            self.ui.plainTextEdit_questions.setPlainText(s_c_question)
            self.ui.plainTextEdit.setPlainText(p_name)
            self.ui.plainTextEdit_hints.setEnabled(True)
            self.ui.comboBox_hints.setCurrentText(game_configuration.HINTS_MODE_2_PL[hints_mode])
            if hints_mode == game_configuration.GAME_HINTS_MODE_UNLIMITED:
                # self.ui.plainTextEdit_hints.setPlainText("")
                self.ui.plainTextEdit_hints.setEnabled(False)
                # self.ui.comboBox_hints.setCurrentText("Zawsze dostępne")
            elif hints_mode == game_configuration.GAME_HINTS_MODE_NO_HINTS:
                self.ui.plainTextEdit_hints.setEnabled(False)
            elif hints_mode == game_configuration.GAME_HINTS_MODE_MAX_NUMBER:
                self.ui.plainTextEdit_hints.setPlainText(hints_c)
                print("...in setConfigurationData: end, hints_c = ", hints_c)
            elif hints_mode == game_configuration.GAME_HINTS_MODE_MAX_AS_PERCENT:
                self.ui.plainTextEdit_hints.setPlainText(hints_c)
                print("...in setConfigurationData: end, hints_c = ", hints_c)
                # self.ui.comboBox_hints.setCurrentText("Max liczba podpowiedzi")
            # elif hints_mode == game_configuration.GAME_HINTS_MAX_AS_PERCENT_OF_ALL_EQUATIONS:
            #     self.ui.plainTextEdit_hints.setPlainText(hints_c)
                # self.ui.comboBox_hints.setCurrentText("Max liczba popdpowiedzi = % równań")

    def handleCbHintsChanged(self):
        hints_mode_str = self.ui.comboBox_hints.currentText()
        print("current hints mode = ", hints_mode_str)
        enb = True
        if hints_mode_str == "Zawsze dostępne" or hints_mode_str == "Bez podpowiedzi":
            enb = False
        self.ui.plainTextEdit_hints.setEnabled(enb)
        # if hints_mode_str == "Max liczba podpowiedzi" or hints_mode_str == "Max liczba popdpowiedzi = % równań":
        #     self.ui.plainTextEdit_hints.setPlainText(hints_c)

    def accept(self):
        try:
            print("in accept - begin")
            self.game_configuration.player_name = self.ui.plainTextEdit.toPlainText()
            self.game_configuration.default_equations = int(self.ui.plainTextEdit_questions.toPlainText())
            self.game_configuration.game_hints_value = self.ui.plainTextEdit_hints.toPlainText()
            self.game_configuration.game_hints_mode = self.game_configuration.HINTS_PL_2_MODE[self.ui.comboBox_hints.currentText()]
            self.game_configuration.default_sound_on = self.ui.checkBox_sounds.isChecked()
            print("in accept: ", self.game_configuration.__str__())
            print("self.game_configuration.game_hints_mode = ", self.game_configuration.game_hints_mode)
            QDialog.accept(self) # ??czy to jest potrzebne?
        except Exception as exc:
            print(exc)

    def getConfiguration(self):
        """
        Returns configuration as LearnMathGui.GameConfiguration
        :return: game configuration
        """
        return self.game_configuration


    def reject(self):
        print("in reject: ", self.game_configuration)
        QDialog.reject(self)


