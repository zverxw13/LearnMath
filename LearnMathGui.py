# -*- coding: utf-8 -*-

"""
LearnMath application GUI.
"""

import sys
import glob

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QMessageBox, QToolTip, QDesktopWidget, QInputDialog, \
    QLineEdit
from PyQt5 import QtMultimedia

from ui_files.learn_math_ui import Ui_MainWindowMatematykaNa5
from LearnMathDialogs import DefaultConfigurationDialog
from LearnMathConfiguration import *
from Statistic import *
from Rule import RuleParsingSingleLineException
import LM_Utils


class GameConfiguration():
    """Class representing game configuration."""
    GAME_DEFAULT_EQUATIONS = 10
    GAME_TYPE_SINGLE_OPERATIONS = "SINGLE_OPERATIONS"
    GAME_TYPE_MULTIPLE_OPERATIONS = "MULTIPLE_OPERATIONS"
    GAME_MODE_NORMAL = "LEARN_MODE"
    GAME_MODE_REPEAT = "REPEAT_MODE"
    GAME_HINTS_MAX_AS_PERCENT_OF_ALL_EQUATIONS = 10
    GAME_HINTS_DEFAULT = 3
    GAME_HINTS_MODE_NO_HINTS = "HINT_NO_HINTS"
    GAME_HINTS_MODE_UNLIMITED = "HINTS_UNLIMITED"
    GAME_HINTS_MODE_MAX_NUMBER = "HINTS_MAX_NUMBER"
    GAME_HINTS_MODE_MAX_AS_PERCENT = "HINTS_MAX_AS_PERCENT"
    GAME_PLAYER_NAME = "Hubert"

    HINTS_MODE_2_PL = {GAME_HINTS_MODE_NO_HINTS: "Bez podpowiedzi",
                       GAME_HINTS_MODE_UNLIMITED: "Zawsze dostępne",
                       GAME_HINTS_MODE_MAX_NUMBER: "Max liczba podpowiedzi",
                       GAME_HINTS_MODE_MAX_AS_PERCENT: "Max liczba popdpowiedzi = % równań"}

    HINTS_PL_2_MODE = {"Bez podpowiedzi": GAME_HINTS_MODE_NO_HINTS,
                       "Zawsze dostępne": GAME_HINTS_MODE_UNLIMITED,
                       "Max liczba podpowiedzi": GAME_HINTS_MODE_MAX_NUMBER,
                       "Max liczba popdpowiedzi = % równań": GAME_HINTS_MODE_MAX_AS_PERCENT}

    def __init__(self, default_equations=GAME_DEFAULT_EQUATIONS,
                 game_type=GAME_TYPE_SINGLE_OPERATIONS,
                 game_mode=GAME_MODE_NORMAL,
                 game_hints_mode=GAME_HINTS_MODE_UNLIMITED,
                 game_hints_value=None,
                 default_sound_on=False):
        self.default_equations = default_equations
        self.game_equations = default_equations
        self.default_sound_on = default_sound_on
        self.game_type = game_type
        self.game_mode = game_mode
        self.game_hints_mode = game_hints_mode
        self.game_hints_value = game_hints_value
        self.player_name = GameConfiguration.GAME_PLAYER_NAME

    def __str__(self):
        s_val = str(self.game_equations) + \
                " | " + self.game_hints_mode + \
                " | " + str(self.game_hints_value) + \
                " | " + self.player_name
        return s_val


class LearnMathGui(QMainWindow):
    """GUI for Learn Math - main window."""
    WELCOME_IMAGE = "./resources/160_calc.png"

    def __init__(self, parent=None):
        super(LearnMathGui, self).__init__(parent)

        self.logger = logging.getLogger()
        self.ui = Ui_MainWindowMatematykaNa5()
        self.ui.setupUi(self)

        # data initialization
        # set up GameConfiguration
        loaded_configuration = None
        try:
            loaded_configuration = \
                LearnMathConfiguration.loadConfigurationFromFile()
            # print("--> wczytana konfiguracja:\n")
            self.logger.debug("--> wczytana konfiguracja:\n")
            # print(loaded_configuration)
            self.game_configuration = loaded_configuration
        except Exception as exc:
            # print("Nie można wczytać konfiguracji.\n" + exc.__str__())
            # print("Ustawiono domyślną konfigurację.")
            self.logger.debug("Nie można wczytać konfiguracji.\n" + exc.__str__())
            self.logger.debug("Ustawiono domyślną konfigurację.")

            self.game_configuration = GameConfiguration(
                default_equations=10, game_type=None, game_mode=None,
                game_hints_mode=GameConfiguration.GAME_HINTS_MODE_UNLIMITED,
                game_hints_value=7, default_sound_on=True)

        self.statistic = Statistic(self.game_configuration.player_name)
        try:
            self.statistic.load_statistic_from_file()
        except FileNotFoundError as fne:
            self.logger.debug("There is no statistic data file for " +
                              self.game_configuration.player_name +
                              "\nStatistic data file will be created "
                              "during playing game.")

        self.db_s = DB_Statistic()
        self.game_player_id = \
            self.db_s.switch_player(self.game_configuration.player_name)

        self.game_current_equation_counter = 1
        self.game_current_equation = None
        self.game_max_hints = 0

        # set last comment for user's answer as empty string
        self.game_last_comment_for_answer = ""
        #
        self.game_correct_counter = 0
        # delay after displaying comment about user's answer
        self.game_delay = 2500
        # set game sounds to on
        self.game_sound_on = self.game_configuration.default_sound_on
        # set the game_growing_delta.
        # It should be used with current equation counter during the game
        self.game_growing_delta = 0
        #
        self.game_in_progress = False

        self.game_config = []
        # dictionary for equations for which user gave incorrect answer
        self.game_bad_answers = []
        self.game_bad_answers_saved = []

        # a base pixmap - for original growing image
        self.base_pixmap = None

        # the rest of set up
        # self.set_growing_image(LearnMathGui.WELCOME_IMAGE)
        self.set_logo_image(LearnMathGui.LearnMathGui.WELCOME_IMAGE)
        self.hide_all_game_elements()
        self.show_growing_area()  # temporary

        # setting tooltips and statustips
        QToolTip.setFont(QFont('SansSerif', 10))
        self.ui.pushButton_check.setToolTip("Sprawdź swoją odpowiedź")
        self.ui.pushButton_hint.setToolTip("Podpowiedz mi, proszę...")
        #
        self.ui.menuProfil.setStatusTip("Obsługa profili graczy")

        s_tip = "Utwórz nowego gracza - jeszcze nie działa..."
        self.ui.actionNowy_gracz.setStatusTip(s_tip)

        s_tip = "Wybierz gracza - jeszcze nie działa..."
        self.ui.actionWybierz_gracza.setStatusTip(s_tip)
        #
        s_tip = "Zdefiniuj domyślną konfigurację dla gier " \
                "(nazwa gracza, podpowiedzi, itp.)"
        self.ui.actionDomyslna_konfiguracja_gier.setStatusTip(s_tip)
        #
        self.ui.menuGra.setStatusTip("Obsługa gier")

        self.ui.menuTylko_dodawanie.setStatusTip("Twoje wyzwanie to: dodawanie")
        self.ui.actionDodawanie_10.setStatusTip("Twoje wyzwanie to: dodawanie - do 10")
        self.ui.actionDodawanie_20.setStatusTip("Twoje wyzwanie to: dodawanie - do 20")
        self.ui.actionDodawanie_30.setStatusTip("Twoje wyzwanie to: dodawanie - do 30")
        self.ui.actionDodawanie_40.setStatusTip("Twoje wyzwanie to: dodawanie - do 40")
        self.ui.actionDodawanie_50.setStatusTip("Twoje wyzwanie to: dodawanie - do 50")
        self.ui.actionDodawanie_100.setStatusTip("Twoje wyzwanie to: dodawanie - do 100")
        self.ui.actionDodawanie_zakres.setStatusTip("Twoje wyzwanie to: dodawanie - w wybranym zakresie")
        self.ui.actionDodawanie_popraw.setStatusTip("Twoje wyzwanie to: dodawanie - popraw swoje błędy")
        #
        self.ui.menuTylko_odejmowanie.setStatusTip("Twoje wyzwanie to: odejmowanie")
        self.ui.actionOdejmowanie_10.setStatusTip("Twoje wyzwanie to: odejmowanie - do 10")
        self.ui.actionOdejmowanie_20.setStatusTip("Twoje wyzwanie to: odejmowanie - do 20")
        self.ui.actionOdejmowanie_30.setStatusTip("Twoje wyzwanie to: odejmowanie - do 30")
        self.ui.actionOdejmowanie_40.setStatusTip("Twoje wyzwanie to: odejmowanie - do 40")
        self.ui.actionOdejmowanie_50.setStatusTip("Twoje wyzwanie to: odejmowanie - do 50")
        self.ui.actionOdejmowanie_100.setStatusTip("Twoje wyzwanie to: odejmowanie - do 100")
        self.ui.actionOdejmowanie_zakres.setStatusTip("Twoje wyzwanie to: odejmowanie - w wybranym zakresie")
        self.ui.actionOdejmowanie_popraw.setStatusTip("Twoje wyzwanie to: odejmowanie - popraw swoje błędy")
        #
        self.ui.menuTylko_mnozenie.setStatusTip("Twoje wyzwanie to: mnożenie")
        self.ui.actionMnozenie_20.setStatusTip("Twoje wyzwanie to: mnożenie - do 20")
        self.ui.actionMnozenie_30.setStatusTip("Twoje wyzwanie to: mnożenie - do 30")
        self.ui.actionMnozenie_40.setStatusTip("Twoje wyzwanie to: mnożenie - do 40")
        self.ui.actionMnozenie_50.setStatusTip("Twoje wyzwanie to: mnożenie - do 50")
        self.ui.actionMnozenie_100.setStatusTip("Twoje wyzwanie to: mnożenie - do 100")
        self.ui.actionMnozenie_zakres.setStatusTip("Twoje wyzwanie to: mnożenie - w wybranym zakresie")
        self.ui.actionMnozenie_popraw.setStatusTip("Twoje wyzwanie to: mnożenie - popraw swoje błędy")
        self.ui.actionMnozenie_przez_n.setStatusTip("Twoje wyzwanie to: mnożenie - przez wybraną liczbę, do 100")
        #
        self.ui.menuDod_Od.setStatusTip("Twoje wyzwanie to: dodawanie i odejmowanie")
        self.ui.actionDod_Od_10.setStatusTip("Twoje wyzwanie to: dodawanie i odejmowanie - do 10")
        self.ui.actionDod_Od_20.setStatusTip("Twoje wyzwanie to: dodawanie i odejmowanie - do 20")
        self.ui.actionDod_Od_30.setStatusTip("Twoje wyzwanie to: dodawanie i odejmowanie - do 30")
        self.ui.actionDod_Od_40.setStatusTip("Twoje wyzwanie to: dodawanie i odejmowanie - do 40")
        self.ui.actionDod_Od_50.setStatusTip("Twoje wyzwanie to: dodawanie i odejmowanie - do 50")
        self.ui.actionDod_Od_100.setStatusTip("Twoje wyzwanie to: dodawanie i odejmowanie - do 100")
        self.ui.actionDod_Od_zakres.setStatusTip("Twoje wyzwanie to: dodawanie i odejmowanie - w wybranym zakresie")
        #
        self.ui.actionKonfiguruj_gre.setStatusTip("Skonfiguruj swoje wyzwanie - jeszcze nie działa...")
        self.ui.actionKoniec.setStatusTip("Wyjdź z programu")

        # connecting actions
        self.ui.actionNowy_gracz.triggered.connect(self.demo_growing_image)
        self.ui.pushButton_check.clicked.connect(self.checkAnswer)
        self.ui.pushButton_hint.clicked.connect(self.getHint)

        self.ui.actionKoniec.triggered.connect(self.koniec)

        self.ui.actionDomyslna_konfiguracja_gier.triggered.connect(
            self.default_configuration)

        self.ui.actionOdejmowanie_10.triggered.connect(self.odejmowanie_10)
        self.ui.actionOdejmowanie_20.triggered.connect(self.odejmowanie_20)
        self.ui.actionOdejmowanie_30.triggered.connect(self.odejmowanie_30)
        self.ui.actionOdejmowanie_40.triggered.connect(self.odejmowanie_40)
        self.ui.actionOdejmowanie_50.triggered.connect(self.odejmowanie_50)
        self.ui.actionOdejmowanie_zakres.triggered.connect(
            self.odejmowanie_konf)
        self.ui.actionOdejmowanie_popraw.triggered.connect(
            self.odejmowanie_poprawki)

        self.ui.actionDodawanie_10.triggered.connect(self.dodawanie_10)
        self.ui.actionDodawanie_20.triggered.connect(self.dodawanie_20)
        self.ui.actionDodawanie_30.triggered.connect(self.dodawanie_30)
        self.ui.actionDodawanie_40.triggered.connect(self.dodawanie_40)
        self.ui.actionDodawanie_50.triggered.connect(self.dodawanie_50)
        self.ui.actionDodawanie_zakres.triggered.connect(self.dodawanie_konf)
        self.ui.actionDodawanie_popraw.triggered.connect(
            self.dodawanie_poprawki)

        self.ui.actionDod_Od_10.triggered.connect(self.dod_od_10)
        self.ui.actionDod_Od_20.triggered.connect(self.dod_od_20)
        self.ui.actionDod_Od_30.triggered.connect(self.dod_od_30)
        self.ui.actionDod_Od_40.triggered.connect(self.dod_od_40)
        self.ui.actionDod_Od_50.triggered.connect(self.dod_od_50)
        self.ui.actionDod_Od_zakres.triggered.connect(self.dod_od_konf)

        self.ui.actionMnozenie_20.triggered.connect(self.mnozenie_20)
        self.ui.actionMnozenie_30.triggered.connect(self.mnozenie_30)
        self.ui.actionMnozenie_40.triggered.connect(self.mnozenie_40)
        self.ui.actionMnozenie_50.triggered.connect(self.mnozenie_50)
        self.ui.actionMnozenie_100.triggered.connect(self.mnozenie_100)
        self.ui.actionMnozenie_zakres.triggered.connect(self.mnozenie_konf)
        self.ui.actionMnozenie_popraw.triggered.connect(self.mnozenie_poprawki)
        self.ui.actionMnozenie_przez_n.triggered.connect(self.mnozenie_przez_n)

        self.ui.actionDzwiek_wlaczony.triggered.connect(self.sounds_on_off)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./resources/sound_high.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.ui.actionDzwiek_wlaczony.setIcon(icon)
        if not self.game_configuration.default_sound_on:
            self.ui.actionDzwiek_wlaczony.setText("Dźwięk: wyłączony")
            self.game_sound_on = False
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("./resources/speaker_off_32.png"),
                           QtGui.QIcon.Normal, QtGui.QIcon.On)
            self.ui.actionDzwiek_wlaczony.setIcon(icon)

        self.ui.textEdit_result.installEventFilter(self)
        # all events will call self.eventFilter(self.textedit, event)

        QMainWindow.setWindowTitle(self, "Matematyka na 5!")
        iconM = QtGui.QIcon()
        # iconM.addPixmap(QtGui.QPixmap("./resources/lm_i1.png"),
        #                 QtGui.QIcon.Normal, QtGui.QIcon.On)
        iconM.addPixmap(QtGui.QPixmap("./resources/lm_i2.gif"),
                        QtGui.QIcon.Normal, QtGui.QIcon.On)
        QMainWindow.setWindowIcon(self, iconM)

        self.update_title()

        self.center()

    def center(self):
        """Centers app on desktop."""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def eventFilter(self, obj, ev):
        """Method required by PyQt for handling key events.

        :param obj: source object of evebt
        :param ev: event
        """
        if ev.type() == QtCore.QEvent.KeyPress:
            if ev.key() == QtCore.Qt.Key_Return \
                    or ev.key() == QtCore.Qt.Key_Enter:
                self.checkAnswer()
                return True
                # If we return True, it's not possible
                # to enter text in the TextEdit.
                # It's possible to check if event.key() == Qt.Key_Return
                # and then return True and emit a signal,
                # otherwise return False

                # From the documentation:
                # In your reimplementation of this function,
                # if you want to filter the event out,
                # i.e. stop it being handled further,
                # return true; otherwise return false.
            return False
        QWidget.eventFilter(self, obj, ev)
        return False

    def closeEvent(self, event):
        """Method required by PyQt for handling close window event."""
        result = QMessageBox.question(self, "Koniec?", "Zamknąć aplikację?")
        if result == QMessageBox.Yes:
            event.accept()
            QCoreApplication.instance().quit()
        else:
            event.ignore()

    def koniec(self):
        """Responsible for closing application.\n
        Shows question dialog to confirm decision."""
        result = QMessageBox.question(self, "Koniec?", "Zamknąć aplikację?")
        if result == QMessageBox.Yes:
            QCoreApplication.instance().quit()

    def demo_growing_image(self):
        """Test method for growing image."""
        # todo:: to delete
        self.logger.debug(("Current eq counter = ",
                           self.game_current_equation_counter))
        self.game_current_equation_counter += 1
        self.logger.debug(("Długość strzalki = ",
                           self.game_current_equation_counter))
        if self.game_current_equation_counter > \
                self.game_configuration.game_equations:
            self.game_current_equation_counter = 1
        self.calculate_growing_image(self.game_current_equation_counter)
        self.ui.retranslateUi(self)

    def set_growing_image(self, path_to_image):
        """ Function draws initial growing image scaled to available height
        divided by number of equations in game.
        Initial height is > 0.
        game_growing_delta is also set. This parameter is used to increase
        the height of growing image during the game,
        when correct answer is given

        :param path_to_image: path to image
        :returns: True if growing image is draw correctly, false otherwise.
        :rtype: bool
        """
        self.base_pixmap = QtGui.QPixmap(path_to_image)

        if self.base_pixmap is None:
            return False

        # pixmap = pixmap.scaled(QtCore.QSize(w, h),
        #                        QtCore.Qt.KeepAspectRatio,
        #                        QtCore.Qt.SmoothTransformation);
        fix = 50
        scaled_height = int(
            (self.ui.gridLayout_main.totalSizeHint().height() - fix)
            / self.game_configuration.game_equations)

        # set the game_growing_delta.
        # It should be used with current equation counter during the game
        self.game_growing_delta = scaled_height

        self.logger.debug(self.game_configuration.game_equations)
        self.logger.debug(scaled_height)

        self.logger.debug(
            ("Czy " + str(self.ui.gridLayout_main.totalSizeHint().height()) +
             " rowna sie " + str(self.game_growing_delta) + " (delta)  * " +
             str(self.game_configuration.game_equations) + "? czyli " +
             str(self.game_growing_delta *
                 self.game_configuration.game_equations)))
        pixmap = self.base_pixmap.scaledToHeight(scaled_height)
        self.ui.label_growing_image.setPixmap(pixmap)
        return True

    def show_image_for_given_answer(self, answer_correct):
        """
        Shows random image basing on answer (correct or bad).

        :param answer_correct: True if answer is correct, False otherwise
        :type answer_correct: bool
        """
        # path_to_image = "D:/Mirek/Priv/MyProjects/LearnMath/resources/"
        path_to_image = "./resources/"
        if answer_correct:
            path_to_image += "ans_ok/160_ok_" + str(randint(1, 4))
        else:
            path_to_image += "ans_bad/160_bad_" + str(randint(1, 4))
        self.base_pixmap = QtGui.QPixmap(path_to_image)
        pixmap = self.base_pixmap.scaled(QtCore.QSize(160, 530),
                                         QtCore.Qt.KeepAspectRatio,
                                         QtCore.Qt.SmoothTransformation)
        self.ui.label_growing_image.setPixmap(pixmap)
        return True

    def set_logo_image(self, path_to_image):
        """
        Sets image for logo.

        :param path_to_image: path to image
        :type param: str
        :returns: True if image was founf, False otherwise
        :rtype: bool
        """
        self.base_pixmap = QtGui.QPixmap(path_to_image)

        if self.base_pixmap is None:
            return False

        pixmap = self.base_pixmap.scaled(QtCore.QSize(160, 530),
                                         QtCore.Qt.KeepAspectRatio,
                                         QtCore.Qt.SmoothTransformation)
        self.ui.label_growing_image.setPixmap(pixmap)
        return True

    def calculate_growing_image(self, current_equation_counter):
        """Test method for growing image - calculate."""
        scaled_height = int(self.game_growing_delta * current_equation_counter)
        pixmap = self.base_pixmap.scaledToHeight(scaled_height)
        self.ui.label_growing_image.setPixmap(pixmap)

    def hide_growing_area(self):
        """Hides growing image."""
        self.ui.label_growing_image.hide()

    def hide_description_area(self):
        """Hides description area."""
        self.ui.label_description.hide()

    def hide_equation_area(self):
        """Hides equation area."""
        self.ui.label_number_1.hide()
        self.ui.label_operation.hide()
        self.ui.label_number_2.hide()
        self.ui.label_equals.hide()
        self.ui.textEdit_result.hide()

    def hide_comment_area(self):
        """Hides comment area."""
        self.ui.label_comment.hide()

    def hide_controls_area(self):
        """Hides controls area."""
        self.ui.pushButton_hint.hide()
        self.ui.pushButton_check.hide()

    def hide_score_area(self):
        """Hides control area."""
        self.ui.label_score.hide()

    def hide_all_game_elements(self):
        """Hides all game elements excluding main menu bar."""
        self.hide_growing_area()
        self.hide_description_area()
        self.hide_equation_area()
        self.hide_comment_area()
        self.hide_controls_area()
        self.hide_score_area()

    def show_growing_area(self):
        """Shows growing are."""
        self.ui.label_growing_image.show()

    def show_description_area(self):
        """Shows description area."""
        self.ui.label_description.show()

    def show_equation_area(self):
        """Shows equation area."""
        self.ui.label_number_1.show()
        self.ui.label_operation.show()
        self.ui.label_number_2.show()
        self.ui.label_equals.show()
        self.ui.textEdit_result.show()

    def show_comment_area(self):
        """Shows commment area."""
        self.ui.label_comment.show()

    def show_controls_area(self):
        """Shows controls area."""
        self.ui.pushButton_hint.show()
        self.ui.pushButton_check.show()

    def show_score_area(self):
        """Shows score area."""
        self.ui.label_score.show()

    def show_all_game_elements(self):
        """Ahows all game elements."""
        self.ui.label_growing_image.clear()
        self.show_growing_area()
        self.show_description_area()
        self.show_equation_area()
        self.show_comment_area()
        self.show_controls_area()
        self.show_score_area()
        self.ui.textEdit_result.setEnabled(True)
        self.ui.pushButton_check.setEnabled(True)
        self.ui.pushButton_hint.setEnabled(True)

    def update_all_game_elements_before_user_input(self):
        """Updates all game elements after random equation and before user
        input."""
        # self.calculate_growing_image(self.game_correct_counter)
        self.ui.textEdit_result.setText("")
        self.ui.label_comment.clear()
        n = self.game_current_equation_counter + 1
        nn = self.game_configuration.game_equations
        corr = self.game_correct_counter
        incorr = self.game_current_equation_counter - self.game_correct_counter
        to_do = nn - self.game_current_equation_counter
        if self.game_configuration.game_hints_mode == \
                GameConfiguration.GAME_HINTS_MODE_MAX_NUMBER \
                or self.game_configuration.game_hints_mode == \
                        GameConfiguration.GAME_HINTS_MODE_MAX_AS_PERCENT:
            str_hints = str(self.game_max_hints)
        elif self.game_configuration.game_hints_mode == \
                GameConfiguration.GAME_HINTS_MODE_UNLIMITED:
            str_hints = "bez limitu"
        elif self.game_configuration.game_hints_mode == \
                GameConfiguration.GAME_HINTS_MODE_NO_HINTS:
            str_hints = "brak"

        score_text = "Działanie: " + str(n) + " z " + str(nn) + \
                     "            Poprawnie: " + str(corr) + \
                     "           Błędnie: " + str(incorr) + \
                     "   \n\n  Podpowiedzi: " + str_hints + \
                     "    Pozostało do rozwiązania: " + str(to_do)
        self.ui.label_score.setText(score_text)

    def update_all_game_elements_after_user_input(self):
        """Updates all games elements after user input. Depends on
        correctness of user input."""
        # self.calculate_growing_image(self.game_correct_counter)
        n = self.game_current_equation_counter + 1
        nn = self.game_configuration.game_equations
        if n > nn:
            n = nn
        corr = self.game_correct_counter
        incorr = self.game_current_equation_counter - self.game_correct_counter
        to_do = nn - self.game_current_equation_counter
        if self.game_configuration.game_hints_mode == \
                GameConfiguration.GAME_HINTS_MODE_MAX_NUMBER or \
                        self.game_configuration.game_hints_mode == \
                        GameConfiguration.GAME_HINTS_MODE_MAX_AS_PERCENT:
            str_hints = str(self.game_max_hints)
        elif self.game_configuration.game_hints_mode == \
                GameConfiguration.GAME_HINTS_MODE_UNLIMITED:
            str_hints = "bez limitu"
        elif self.game_configuration.game_hints_mode == \
                GameConfiguration.GAME_HINTS_MODE_NO_HINTS:
            str_hints = "brak"

        score_text = "Działanie: " + str(n) + " z " + str(nn) + \
                     "            Poprawnie: " + str(corr) + \
                     "           Błędnie: " + str(incorr) + \
                     "   \n\n  Podpowiedzi: " + str_hints + \
                     "    Pozostało do rozwiązania: " + str(to_do)
        self.ui.label_score.setText(score_text)

    def get_score_info(self):
        """Returns string description of user score.

        :returns: string for user score
        :rtype: str
        """
        nn = self.game_configuration.game_equations
        corr = self.game_correct_counter
        # incorr = self.game_current_equation_counter - self.game_correct_counter
        pr = corr / nn * 100.0
        return "Twój wynik to:\n" \
               + str(corr) + " poprawnych odpowiedzi z " + str(nn) + \
               "\n(poprawnych: " + str(int(pr)) + "%)"

    def get_str_bad_answers(self):
        """
        :returns: Multi line text with equations with incorrect user's answer
        :rtype: str`
        """
        str_bad_answers = "Twoje błędne odpowiedzi:\n"
        for eq in self.game_bad_answers:
            # if len(str_bad_answers) <= 0:
            #     str_bad_answers = eq.__str__()
            # else:
            str_bad_answers = str_bad_answers + "\n" + eq.__str__()
        return str_bad_answers

    def sounds_on_off(self):
        """Handles switching sound on/off."""
        c = self.ui.actionDzwiek_wlaczony.isChecked()
        txt = "Dźwięk: włączony" if c else "Dźwięk: wyłączony"
        self.ui.actionDzwiek_wlaczony.setText(txt)
        self.game_sound_on = c
        icon = QtGui.QIcon()
        if c:
            icon.addPixmap(QtGui.QPixmap("./resources/sound_high.png"),
                           QtGui.QIcon.Normal, QtGui.QIcon.On)
        else:
            icon.addPixmap(QtGui.QPixmap("./resources/speaker_off_32.png"),
                           QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.ui.actionDzwiek_wlaczony.setIcon(icon)

    def odejmowanie_10(self):
        """Starts gane: subtracting - 10"""
        self.game_configuration.game_mode = GameConfiguration.GAME_MODE_NORMAL
        self.start_single_operation_game("-", RANGE_0_10)

    def odejmowanie_20(self):
        """Starts gane: subtracting - 20"""
        self.game_configuration.game_mode = GameConfiguration.GAME_MODE_NORMAL
        self.start_single_operation_game("-", RANGE_0_20)

    def odejmowanie_30(self):
        """Starts gane: subtracting - 30"""
        self.game_configuration.game_mode = GameConfiguration.GAME_MODE_NORMAL
        self.start_single_operation_game("-", RANGE_0_30)

    def odejmowanie_40(self):
        """Starts gane: subtracting - 40"""
        self.game_configuration.game_mode = GameConfiguration.GAME_MODE_NORMAL
        self.start_single_operation_game("-", RANGE_0_40)

    def odejmowanie_50(self):
        """Starts gane: subtracting - 50"""
        self.game_configuration.game_mode = GameConfiguration.GAME_MODE_NORMAL
        self.start_single_operation_game("-", RANGE_0_50)

    def odejmowanie_konf(self):
        """Starts gane: subtracting - with custom rules."""
        self.dzialanie_konf("-", "Odejmowanie")

    def odejmowanie_poprawki(self):
        """Starts gane in learnig top mistakes mode: subtracting."""
        self.dzialanie_poprawki("-", "Odejmowanie")

    def dodawanie_10(self):
        """Starts gane: addition - 10"""
        self.game_configuration.game_mode = GameConfiguration.GAME_MODE_NORMAL
        self.start_single_operation_game("+", RANGE_0_10)

    def dodawanie_20(self):
        """Starts gane: addition - 20"""
        self.game_configuration.game_mode = GameConfiguration.GAME_MODE_NORMAL
        self.start_single_operation_game("+", RANGE_0_20)

    def dodawanie_30(self):
        """Starts gane: addition - 30"""
        self.game_configuration.game_mode = GameConfiguration.GAME_MODE_NORMAL
        self.start_single_operation_game("+", RANGE_0_30)

    def dodawanie_40(self):
        """Starts gane: addition - 40"""
        self.game_configuration.game_mode = GameConfiguration.GAME_MODE_NORMAL
        self.start_single_operation_game("+", RANGE_0_40)

    def dodawanie_50(self):
        """Starts gane: addition - 50"""
        self.game_configuration.game_mode = GameConfiguration.GAME_MODE_NORMAL
        self.start_single_operation_game("+", RANGE_0_50)

    def dodawanie_konf(self):
        """Starts gane: addition - custom rules"""
        self.dzialanie_konf("+", "Dodawanie")

    def dodawanie_poprawki(self):
        """Starts gane: addition - improve top N worst"""
        self.dzialanie_poprawki("+", "Dodawanie")

    def dod_od_10(self):
        """Starts gane: addition and subtraction - 10"""
        self.game_configuration.game_mode = GameConfiguration.GAME_MODE_NORMAL
        self.start_multiple_operations_game(["+", "-"], RANGE_0_10)

    def dod_od_20(self):
        """Starts gane: addition and subtraction - 20"""
        self.game_configuration.game_mode = GameConfiguration.GAME_MODE_NORMAL
        self.start_multiple_operations_game(["+", "-"], RANGE_0_20)

    def dod_od_30(self):
        """Starts gane: addition and subtraction - 30"""
        self.game_configuration.game_mode = GameConfiguration.GAME_MODE_NORMAL
        self.start_multiple_operations_game(["+", "-"], RANGE_0_30)

    def dod_od_40(self):
        """Starts gane: addition and subtraction - 40"""
        self.game_configuration.game_mode = GameConfiguration.GAME_MODE_NORMAL
        self.start_multiple_operations_game(["+", "-"], RANGE_0_40)

    def dod_od_50(self):
        """Starts gane: addition and subtraction - 50"""
        self.game_configuration.game_mode = GameConfiguration.GAME_MODE_NORMAL
        self.start_multiple_operations_game(["+", "-"], RANGE_0_50)

    def dod_od_konf(self):
        """Starts gane: addition and subtraction - custom rules"""
        # self.game_configuration.game_mode = GameConfiguration.GAME_MODE_NORMAL
        # self.start_multiple_operations_game(["+", "-"], None)
        QMessageBox.information(self, "Informacja", "Funkcja nie jest "
                                                    "wspierana")

    def mnozenie_20(self):
        """Starts gane: multiply - 20"""
        try:
            self.game_configuration.game_mode = \
                GameConfiguration.GAME_MODE_NORMAL
            self.start_single_operation_game("*", RANGE_0_20)
        except Exception as exc:
            self.logger.error(exc)

    def mnozenie_30(self):
        """Starts gane: multiply - 30"""
        try:
            self.game_configuration.game_mode = \
                GameConfiguration.GAME_MODE_NORMAL
            self.start_single_operation_game("*", RANGE_0_30)
        except Exception as exc:
            self.logger.error(exc)

    def mnozenie_40(self):
        """Starts gane: multiply - 40"""
        try:
            self.game_configuration.game_mode = \
                GameConfiguration.GAME_MODE_NORMAL
            self.start_single_operation_game("*", RANGE_0_40)
        except Exception as exc:
            self.logger.error(exc)

    def mnozenie_50(self):
        """Starts gane: multiply - 50"""
        self.game_configuration.game_mode = GameConfiguration.GAME_MODE_NORMAL
        self.start_single_operation_game("*", RANGE_0_50)

    def mnozenie_100(self):
        """Starts gane: multiply - 100"""
        self.game_configuration.game_mode = GameConfiguration.GAME_MODE_NORMAL
        self.start_single_operation_game("*", RANGE_0_100)

    def mnozenie_konf(self):
        """Starts gane: multiply - custom rules"""
        self.dzialanie_konf("*", "Mnożenie")

    def mnozenie_poprawki(self):
        """Starts gane: multiply - improve top N worst"""
        self.dzialanie_poprawki("*", "Mnożenie")

    def mnozenie_przez_n(self):
        """Starts gane: multiply - by given number"""
        self.game_configuration.game_mode = GameConfiguration.GAME_MODE_NORMAL
        n, ok = QInputDialog.getInt(self, "Mnożenie do 100 przez wybraną "
                                          "liczbę",
                                    'Przez jaką liczbę chcesz mnożyć?\n\n'
                                    '(podaj liczbę większą od 1)            '
                                    '                                        '
                                    '             ',
                                    3, 2, 10)
        if ok:
            self.logger.debug(str(n))
            # prepare custom rules with N
            text_cr = "L1=" + str(n) + "\nL2>=1\nL2<=10"
            # and try to start a game
            try:
                custom_rules = Rule.parse(text_cr.splitlines())
                self.start_single_operation_game_custom_rules("*", custom_rules)
            except RuleParsingSingleLineException as rpsle:
                err_desc = "Konfiguracja:\n\n" + str(text_cr) + \
                           "\n\nnie jest prawidłowa.\n Sprawdź wprowadzone " \
                           "reguły.\n\n" + \
                           rpsle.__str__()
                QMessageBox.information(self, "Nieprawidłowa konfiguracja",
                                        err_desc)
                self.logger.debug("Nieprawidłowa konfiguracja:\n\n" + err_desc)

    def dzialanie_konf(self, dzialanie_mat, dzialanie_mat_txt):
        """
        Method for starting game with custo rules for given operator.

        :param dzialanie_mat: operation = ["+" | "-" | "/" | "*"}
        See Game.OPERATION_xxx values.
        :type dzialanie_mat: str
        :param dzialanie_mat_txt: name of operation. Text used to configure
        window title.
        :type dzialanie_mat_txt: str
        """
        self.game_configuration.game_mode = GameConfiguration.GAME_MODE_NORMAL
        text, ok = QInputDialog.getMultiLineText(self,
                                                 dzialanie_mat_txt.upper() +
                                                 ' - konfiguracja',
                                                 'Wpisz reguły.\n'
                                                 'Format: [L1|L2|W] ['
                                                 '==|=|<=|<|>=|>] liczba')
        if ok:
            self.logger.debug(str(text))
            try:
                custom_rules = Rule.parse(text.splitlines())
                if len(custom_rules) > 0:
                    self.start_single_operation_game_custom_rules(
                        dzialanie_mat, custom_rules)
                else:
                    err_desc = "Brak konfiguracji!"
                    QMessageBox.information(self, "Nieprawidłowa "
                                                  "konfiguracja", err_desc)
                    self.logger.debug("Nieprawidłowa konfiguracja:\n\n" +
                                      err_desc)
            except RuleParsingSingleLineException as rpsle:
                err_desc = "Konfiguracja:\n\n" + str(text) + \
                           "\n\nnie jest prawidłowa.\n" \
                           "Sprawdź wprowadzone reguły.\n\n" + \
                           rpsle.__str__()
                QMessageBox.information(self, "Nieprawidłowa konfiguracja",
                                        err_desc)
                self.logger.debug("Nieprawidłowa konfiguracja:\n\n" + err_desc)

    def dzialanie_poprawki(self, dzialanie_mat, dzialanie_mat_txt):
        """
        Starts game in improve top N worst mode for given operator.

        :param dzialanie_mat: operation = ["+" | "-" | "/" | "*"}
        See Game.OPERATION_xxx values.
        :type dzialanie_mat: str
        :param dzialanie_mat_txt: name of operation. Text used to configure
        window title.
        :type dzialanie_mat_txt: str
        """
        self.game_configuration.game_mode = GameConfiguration.GAME_MODE_NORMAL

        topN, ok = QInputDialog.getInt(self, dzialanie_mat_txt.upper() +
                                       ' - popraw błędne odpowiedzi',
                                       'Ile równań chcesz poprawić?\n\n'
                                       '(podaj liczbę większą od zera) ' \
                                       '                                    '
                                       '                            ',
                                       10, 1)
        if ok:
            self.logger.debug(str(topN))
            eq_to_learn = self.db_s.getTopWorstEquations(self.game_player_id,
                                                         dzialanie_mat,
                                                         str(topN))
            start_repeating = False
            if eq_to_learn is not None:
                if len(eq_to_learn) > 0:
                    start_repeating = True

            if start_repeating:
                self.game_bad_answers_saved = eq_to_learn[:]
                self.game_configuration.game_type = \
                    GameConfiguration.GAME_TYPE_SINGLE_OPERATIONS
                self.game_configuration.game_mode = \
                    GameConfiguration.GAME_MODE_REPEAT
                self.game_configuration.game_equations = len(
                    self.game_bad_answers_saved)
                self.logger.debug(self.game_config)
                self.start_single_operation_game(
                    dzialanie_mat, None,
                    self.game_configuration.game_equations)
            else:
                QMessageBox.information(self, "Informacja",
                                        "Nie masz nic do powtórki, brawo!")

    def start_single_operation_game_custom_rules(
            self, operation, custom_rules, game_equations=None):
        """
        Starts single operator game - a game with only one kind of used
        opertor.

        :param operation: operator = ["+" | "-" | "/" | "*"}
        See Game.OPERATION_xxx values.
        :type operation: str
        :param custom_rules: custom rules.
        :param game_equations: ??????????????
        """
        if game_equations is None:
            self.game_configuration.game_equations = \
                self.game_configuration.default_equations
        else:
            self.game_configuration.game_equations = game_equations
        self.game_config.clear()
        self.game_bad_answers.clear()

        if operation == OPERATION_SUBTRACTION:
            self.game_config.append(
                ConfigSubtraction(None, without_zero=True,
                                  minuend_condition=None,
                                  minuend_value=None,
                                  subtrahend_condition=None,
                                  subtrahend_value=None,
                                  minuend_ge_subtrahend=None,
                                  result_condition=None, result_value=None,
                                  custom_rules=custom_rules))
        elif operation == OPERATION_ADDITION:
            self.game_config.append(
                ConfigAddition(None, without_zero=True,
                               summand_1_condition=None,
                               summand_1_value=None,
                               summand_2_condition=None,
                               summand_2_value=None, result_condition=None,
                               result_value=None, custom_rules=custom_rules))
        elif operation == OPERATION_MULTIPLY:
            self.game_config.append(
                ConfigMultiply(None, without_zero=True, without_one=True,
                               element_1_condition=None,
                               element_1_value=None,
                               element_2_condition=None,
                               element_2_value=None, result_condition=None,
                               result_value=None, custom_rules=custom_rules))
        else:
            self.logger.debug(("Operation ", operation, " is not supported, "
                                                        "sorry..."))
            raise Exception("Not supported operation")

        # the rest of game initialization
        self.game_in_progress = True
        self.game_configuration.game_type = \
            GameConfiguration.GAME_TYPE_SINGLE_OPERATIONS
        self.game_current_equation_counter = 0
        self.game_correct_counter = 0
        self.show_all_game_elements()
        self.update_all_game_elements_before_user_input()
        self.ui.textEdit_result.setFocus()
        self.prepareEquation()  # temporary commented out

    def start_single_operation_game(self, operation, range_dict=None,
                                    game_equations=None):
        """
        Starts single operator game.

        :param operation: operator = ["+" | "-" | "/" | "*"}
        See Game.OPERATION_xxx values.
        :type operation: str
        :param range_dict: dict with range used to limit generated equations
        :param game_equations: ???????????
        """
        if game_equations is None:
            self.game_configuration.game_equations = \
                self.game_configuration.default_equations
        else:
            self.game_configuration.game_equations = game_equations
        self.game_config.clear()
        self.game_bad_answers.clear()

        if operation == OPERATION_SUBTRACTION:
            if range_dict is None:
                range_dict = RANGE_0_20
                self.game_config.append(
                    ConfigSubtraction(range_dict, without_zero=True,
                                      minuend_condition=">",
                                      minuend_value=10,
                                      subtrahend_condition="<",
                                      subtrahend_value=10,
                                      minuend_ge_subtrahend=True,
                                      result_condition="<", result_value=10))
            else:
                self.game_config.append(
                    ConfigSubtraction(range_dict, without_zero=True))
        elif operation == OPERATION_ADDITION:
            if range_dict is None:
                range_dict = RANGE_0_20
                max_n = range_dict["to"]
                max_n_minus_ten = max_n - 10
                self.game_config.append(
                    ConfigAddition(range_dict, without_zero=True,
                                   summand_1_condition="<",
                                   summand_1_value=max_n - 10,
                                   summand_2_condition="<",
                                   summand_2_value=max_n - 10,
                                   result_condition=">=",
                                   result_value=max_n - 10 + 1))

            else:
                max_n = range_dict["to"]
                self.game_config.append(
                    ConfigAddition(range_dict, without_zero=True,
                                   summand_1_condition="<=",
                                   summand_1_value=max_n,
                                   summand_2_condition="<=",
                                   summand_2_value=max_n,
                                   result_condition="<=", result_value=max_n))
        elif operation == OPERATION_MULTIPLY:
            if range_dict is None:
                range_dict = RANGE_0_10
                self.game_config.append(
                    ConfigMultiply(range_dict, without_zero=True,
                                   without_one=False,
                                   element_1_condition="<=",
                                   element_1_value=10,
                                   element_2_condition="<=",
                                   element_2_value=10,
                                   result_condition="<=", result_value=20))
            else:
                max_result = int(range_dict["to"])
                self.game_config.append(
                    ConfigMultiply(range_dict, without_zero=True,
                                   without_one=True,
                                   element_1_condition="<=",
                                   element_1_value=10,
                                   element_2_condition="<=",
                                   element_2_value=10,
                                   result_condition="<=",
                                   result_value=max_result))
        else:
            self.logger.debug(("Operation ", operation, " is not supported, "
                                                        "sorry..."))
            raise Exception("Not supported operation")

        # the rest of game initialization
        # set max hints number
        if self.game_configuration.game_hints_mode == \
                GameConfiguration.GAME_HINTS_MODE_MAX_NUMBER:
            self.game_max_hints = self.game_configuration.game_hints_value
        elif self.game_configuration.game_hints_mode == \
                GameConfiguration.GAME_HINTS_MODE_MAX_AS_PERCENT:
            percent = self.game_configuration.game_hints_value
            eq_c = self.game_configuration.default_equations
            self.game_max_hints = int((percent / 100.0) * eq_c)
        self.logger.debug(("Liczba podpowiedzi: ", self.game_max_hints))
        self.game_in_progress = True
        self.game_configuration.game_type = \
            GameConfiguration.GAME_TYPE_SINGLE_OPERATIONS
        self.game_current_equation_counter = 0
        self.game_correct_counter = 0
        self.show_all_game_elements()
        self.update_all_game_elements_before_user_input()
        self.ui.textEdit_result.setFocus()
        try:
            self.prepareEquation()
        except Exception as exc:
            self.logger.error(exc)
            raise

    def start_multiple_operations_game(self, operations_list,
                                       range_dict=None, game_equations=None):
        """
        Starts game with multiple operators.

        :param operations_list: list  with operators, eg.: ["+", "-"]
        :type operations_list: list[str]
        :param range_dict: dictionary with range. {'from': min_n, 'to': max_n}
        :type range_dict: dict
        """
        if game_equations is None:
            self.game_configuration.game_equations = \
                self.game_configuration.default_equations
        else:
            self.game_configuration.game_equations = game_equations
        self.game_config.clear()
        self.game_bad_answers.clear()
        for operation in operations_list:
            if operation == OPERATION_SUBTRACTION:
                if range_dict is None:
                    range_dict = RANGE_0_20
                    self.game_config.append(
                        ConfigSubtraction(range_dict, without_zero=True,
                                          minuend_condition=">",
                                          minuend_value=10,
                                          subtrahend_condition="<",
                                          subtrahend_value=10,
                                          minuend_ge_subtrahend=True,
                                          result_condition="<",
                                          result_value=10))
                else:
                    self.game_config.append(
                        ConfigSubtraction(range_dict, without_zero=True))
            elif operation == OPERATION_ADDITION:
                if range_dict is None:
                    range_dict = RANGE_0_20
                    max_n = range_dict["to"]
                    max_n_minus_ten = max_n - 10
                    self.game_config.append(
                        ConfigAddition(range_dict, without_zero=True,
                                       summand_1_condition="<",
                                       summand_1_value=max_n - 10,
                                       summand_2_condition="<",
                                       summand_2_value=max_n - 10,
                                       result_condition=">=",
                                       result_value=max_n - 10 + 1))

                else:
                    max_n = range_dict["to"]
                    self.game_config.append(
                        ConfigAddition(range_dict, without_zero=True,
                                       summand_1_condition="<=",
                                       summand_1_value=max_n,
                                       summand_2_condition="<=",
                                       summand_2_value=max_n,
                                       result_condition="<=",
                                       result_value=max_n))

        # the rest of game initialization
        self.game_in_progress = True
        self.game_configuration.game_type = \
            GameConfiguration.GAME_TYPE_MULTIPLE_OPERATIONS
        self.game_current_equation_counter = 0
        self.game_correct_counter = 0
        self.show_all_game_elements()
        self.update_all_game_elements_before_user_input()
        self.ui.textEdit_result.setFocus()
        self.prepareEquation()

    def prepareEquation(self):
        """
        Method prepares equation based on current game mode (new, repeat)
        and game operator mode (single, multiple).
        """
        try:
            repeat_mode = self.game_configuration.game_mode == \
                          GameConfiguration.GAME_MODE_REPEAT  # to comment out?
            if not repeat_mode:
                if len(self.game_config) == 1:
                    preparedEquation = \
                        Equation.prepare_equation_basing_on_single_operator(
                            self.game_config[0])
                    if preparedEquation is not None:
                        self.drawEquation(preparedEquation)
                        self.game_current_equation_counter += 1
                        self.game_current_equation = preparedEquation
                    else:
                        raise Exception("Preparing equation failed, "
                                        "can't draw equation!")
                else:
                    preparedEquation = \
                        Equation.prepare_equation_basing_on_multiple_operator(
                            self.game_config)
                    if preparedEquation is not None:
                        self.drawEquation(preparedEquation)
                        self.game_current_equation_counter += 1
                        self.game_current_equation = preparedEquation
                    else:
                        raise Exception("Preparing equation failed, "
                                        "can't draw equation!")
                        # print("Equation.prepare_equation_basing_on_
                        #        multiple_operator(self.game_config) - not
                        #        handled yet...")
            else:  # repeat_mode = True,
                # go through equation in self.game_bad_answers
                repeated_equation = self.game_bad_answers_saved[
                    self.game_current_equation_counter]
                self.drawEquation(repeated_equation)
                self.game_current_equation_counter += 1
                self.game_current_equation = repeated_equation
        except RuleException as re:
            err = re.__str__()
            self.logger.error(err)
            QMessageBox.critical(self, "Błąd",
                                 "Nieprawidłowa konfiguracja.\n Popraw "
                                 "konfigurację.\n\n\n" + err)
            self.hide_all_game_elements()

    def drawEquation(self, p_equation):
        """
        Draws passed equation on screen.

        :param p_equation: equation
        :type p_equation: Game.Equation
        """
        self.ui.label_number_1.setText(str(p_equation.number_1))
        self.ui.label_operation.setText(str(p_equation.operator))
        self.ui.label_number_2.setText(str(p_equation.number_2))
        self.ui.textEdit_result.clear()
        self.ui.pushButton_hint.setEnabled(True)

    @staticmethod
    def get_all_files_from_directory(directory, file_mask="*"):
        """
        Returns list of all files from passed directory which meet given
        file_mask.

        :param directory: directory to read files from
        :type directory: str
        :param file_mask: pattern for files to read. Default: * (all)
        :type file_mask: str
        :returns: list of all files from passed directory which meet given
        :rtype: list[str]
        """
        path_and_filter = directory + "/" + file_mask
        list_f = glob.glob(path_and_filter)
        return list_f

    def get_random_yes_no_sound(self, correct_answer):
        """
        Returns random sound (full path to it) for given correct or bad answer.

        :param correct_answer: True for correct answer, False otherwise
        :returns: random sound (full path to it) for given correct or bad answer.
        :rtype: str
        """
        all_files = None
        if correct_answer:
            # get all "yes" files
            # all_files = self.get_all_files_from_directory(
            # "./resources/ans_ok/fx", "*.wav")
            all_files = self.get_all_files_from_directory(
                "./resources/ans_ok/fx", "*.wav")
        else:
            # get all "no" files
            # all_files = self.get_all_files_from_directory(
            # "./LearnMath/resources/ans_bad/fx", "*.wav")
            all_files = self.get_all_files_from_directory(
                "./resources/ans_bad/fx", "*.wav")
        self.logger.debug(all_files)
        # random one of them
        a_max = len(all_files) - 1
        rnd = randint(0, a_max)
        # and return it as QSound
        # print("rnd = ", rnd)
        self.logger.debug(("file for rnd: ", all_files[rnd]))
        print("file for rnd: ", all_files[rnd])
        print("File exists?: " +
              "TAK" if os.path.exists(all_files[rnd]) else "NIE")
        self.logger.debug("File exists?: " +
                          "TAK" if os.path.exists(all_files[rnd]) else "NIE")
        return all_files[rnd]

    def comment_answer(self, comment_for_answer, correct):
        """
        Shows comment for answer for const delay or length of played sound.

        :param comment_for_answer: comment for answer
        :type comment_for_answer: str
        :param correct: True if answer is correct, False otherwise
        :type correct: bool
        """
        self.ui.label_comment.setText(comment_for_answer)
        self.show_image_for_given_answer(correct)
        timer = QtCore.QTimer()

        f_length = self.game_delay
        if self.game_sound_on:  # the game sounds are on
            f_name = self.get_random_yes_no_sound(correct)
            f_length = max(int(LM_Utils.get_wave_length(f_name) * 1000),
                           self.game_delay)
            # print("playing sound")
            self.logger.debug("playing sound")
            QtMultimedia.QSound.play(f_name)

        timer.singleShot(f_length, self.clear_answer_label_and_continue_game)

    def checkAnswer(self):
        """Checks and validates user answer."""
        self.ui.pushButton_check.setEnabled(False)
        self.ui.pushButton_hint.setEnabled(False)
        self.ui.textEdit_result.setEnabled(False)
        correct = True
        answer = self.ui.textEdit_result.toPlainText()

        if len(answer) <= 0:
            QMessageBox.information(self, "Brak wyniku:", "Wpisz wynik.")
            self.ui.pushButton_check.setEnabled(True)
            self.ui.pushButton_hint.setEnabled(True)
            self.ui.textEdit_result.setEnabled(True)
            self.ui.textEdit_result.setFocus()
            return

        try:
            answer = int(answer)
        except Exception:
            correct = False
            QMessageBox.information(self, "Błąd:", "Wpisz liczbę.")
            self.ui.pushButton_check.setEnabled(True)
            self.ui.pushButton_hint.setEnabled(True)
            self.ui.textEdit_result.setEnabled(True)
            self.ui.textEdit_result.setText("")
            self.ui.textEdit_result.setFocus()
        else:
            correct = self.game_current_equation.check_user_result(answer)

            if correct:
                self.game_correct_counter += 1
            else:
                self.game_bad_answers.append(self.game_current_equation)

            # zapis działania i udzielonego wyniku do statystyki
            # do pliku csv
            self.statistic.add_equation_to_statistic(
                self.game_current_equation, correct)
            # do bazy danych
            try:
                self.db_s.log_equation(self.game_player_id,
                                       self.game_current_equation.number_1,
                                       self.game_current_equation.number_2,
                                       self.game_current_equation.operator,
                                       correct)
            except Exception as exc:
                self.logger.error(exc.__str__())

            comment_for_answer = Answers.get_random_comment_for_answer(
                correct, self.game_last_comment_for_answer)
            self.game_last_comment_for_answer = comment_for_answer
            # comment_for_answer = "Brawo!" if correct else "Niepoprawnie..."
            self.comment_answer(comment_for_answer, correct)

    def clear_answer_label_and_continue_game(self):
        """Continue game after user answer or ends game if necessary."""
        # clear answer label
        self.ui.label_comment.setText("")
        self.ui.label_growing_image.clear()
        # self.ui.textEdit_result.setFocus()

        # update game status info
        self.update_all_game_elements_after_user_input()

        # check if it is the end of game (checked last question)
        if self.game_current_equation_counter == \
                self.game_configuration.game_equations:  # if yes, then finish game
            self.game_in_progress = False
            # show window with summary
            QMessageBox.information(self, "Twój wynik", self.get_score_info())

            # if there are bad answers, show them
            if len(self.game_bad_answers) > 0:
                QMessageBox.information(self, "Twoje błędy",
                                        self.get_str_bad_answers())
                # ask for repeating equations with incorrect answer
                result = QMessageBox.question(self, "Decyzja", "Czy chcesz "
                                                               "się poprawić?")
                if result == QMessageBox.Yes:
                    self.game_bad_answers_saved = self.game_bad_answers[:]
                    if self.game_configuration.game_type == \
                            GameConfiguration.GAME_TYPE_SINGLE_OPERATIONS:
                        self.game_configuration.game_mode = \
                            GameConfiguration.GAME_MODE_REPEAT
                        self.game_configuration.game_equations = len(
                            self.game_bad_answers_saved)
                        self.start_single_operation_game(
                            self.game_config[0].operator,
                            self.game_config[0].range_dict,
                            self.game_configuration.game_equations)
                    else:
                        # game_type == MULTIPLE_OPERATIONS
                        self.game_configuration.game_mode = \
                            GameConfiguration.GAME_MODE_REPEAT
                        self.game_configuration.game_equations = len(
                            self.game_bad_answers_saved)
                        self.game_bad_answers.clear()
                        self.game_in_progress = True
                        self.game_configuration.game_type = \
                            GameConfiguration.GAME_TYPE_MULTIPLE_OPERATIONS
                        self.game_current_equation_counter = 0
                        self.game_correct_counter = 0
                        self.show_all_game_elements()
                        self.update_all_game_elements_before_user_input()
                        self.ui.textEdit_result.setFocus()
                        self.prepareEquation()
                else:
                    self.logger.debug("Szkoda, że nie chcesz poćwiczyć :(")
                    # koniec gry
                    # ToDo: ekran na koniec gry
            else:
                # wszystkie odpowiedzi poprawne
                # ToDo: ekran na koniec gry
                self.logger.debug("Koniec gry - wszystkie odpowiedzi poprawne")
                self.hide_all_game_elements()
        else:  # if no, then continue game
            # Prepare next equation to solve
            self.prepareEquation()
            # Enable buttons
            self.ui.pushButton_check.setEnabled(True)
            self.ui.pushButton_hint.setEnabled(True)
            self.ui.textEdit_result.setEnabled(True)
            self.ui.textEdit_result.setFocus()

    def getHint(self):
        """
        Handler for 'hint' button. Show available hint for equation
        depending on game hints mode.
        """
        if self.game_configuration.game_hints_mode == \
                GameConfiguration.GAME_HINTS_MODE_NO_HINTS:
            self.ui.label_comment.setText("Wybrano grę bez podpowiedzi.")
            return
        elif self.game_configuration.game_hints_mode == \
                GameConfiguration.GAME_HINTS_MODE_MAX_NUMBER or \
                        self.game_configuration.game_hints_mode == \
                        GameConfiguration.GAME_HINTS_MODE_MAX_AS_PERCENT:
            if self.game_max_hints > 0:
                self.game_max_hints -= 1
            else:
                self.ui.label_comment.setText("Wykorzystano wszystkie "
                                              "podpowiedzi.")
                self.ui.textEdit_result.setFocus()
                return
        # else:
        hint = Equation.get_hint_for_equation(self.game_current_equation)
        self.ui.label_comment.setText(hint)
        self.ui.textEdit_result.setFocus()
        self.ui.pushButton_hint.setEnabled(False)

    def default_configuration(self):
        """
        Handler for "default configuration" menu. Shows dialog for default
        game configuration.
        """
        self.logger.debug(("def conf - game_in_progress = ",
                           self.game_in_progress))
        if not self.game_in_progress:
            open_config = False
            text, ok = QInputDialog.getText(self, "Dostęp kontrolowany",
                                            "Wpisz hasło              "
                                            "                         "
                                            "        ", QLineEdit.Password)
            if ok:
                if text == "mrkmj19":
                    open_config = True

            if open_config:
                self.conf_dialog = DefaultConfigurationDialog(self)
                self.conf_dialog.set_configuration_data(
                    self.game_configuration)

                if self.conf_dialog.exec_() == self.conf_dialog.Accepted:
                    self.logger.debug("New settings accepted")
                    self.game_configuration = \
                        self.conf_dialog.get_configuration()
                    try:
                        LearnMathConfiguration.saveConfigurationToFile(
                            self.game_configuration)
                        self.game_player_id = self.db_s.switch_player(
                            self.game_configuration.player_name)
                        self.update_title()
                    except Exception as exc:
                        self.logger.error(exc.__str__())
                else:
                    self.logger.debug("Settings cancelled :(")
        else:
            QMessageBox.information(self, "Informacja",
                                    "Nie można zmienić konfiguracji w "
                                    "trakcie gry.")

    def update_title(self):
        """Updates application title with current user name."""
        self.setWindowTitle("Matematyka na 5!  [" +
                            self.game_configuration.player_name + "]")


if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        myapp = LearnMathGui()
        myapp.show()
        sys.exit(app.exec_())
    except Exception as ex:
        print(ex)
