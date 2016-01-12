# -*- coding: utf-8 -*-

import os
import csv
import shutil
from collections import namedtuple
import sqlite3

from Game import *
import logging


class DB_Statistic(object):
    def __init__(self, db_file='learn_math.db'):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self._create_database()
        self.logger = logging.getLogger()

    def _create_database(self):
        # Create table Player
        self.cursor.execute('''CREATE TABLE if not exists Player (Id INTEGER PRIMARY KEY, Name TEXT)''')

        # Create table Equations
        self.cursor.execute('''CREATE TABLE if not exists Equations (Player_id INTEGER NOT NULL, L1 TEXT, Op TEXT,
        L2 TEXT, Cnt_correct INTEGER, Cnt_bad INTEGER)''')

        self.conn.commit()

    def switch_player(self, player_name="Hubert"):
        """
        Switching player. Add player to database if it doesn't exist.
        :param player_name:
        :return: player_id
        """
        t = [str(player_name)]
        self.logger.debug("in switch_player")
        self.logger.debug(type(player_name))
        self.logger.debug(player_name)
        try:
            self.cursor.execute('SELECT Id FROM Player WHERE Name=?', t)
            rec_l = self.cursor.fetchall()
            if len(rec_l) > 0:
                self.logger.debug("id of " + player_name + ": ")
                self.logger.debug(str(rec_l[0][0]))
                self.logger.debug("==")
            else:
                self.cursor.execute('INSERT INTO Player (Name) VALUES (?)', t)
                self.conn.commit()
                self.cursor.execute('SELECT Id FROM Player WHERE Name=?', t)
                rec_l = self.cursor.fetchall()
                self.logger.debug("inserting player into database")
                self.logger.debug(str(rec_l[0][0]))
            return rec_l[0][0]
        except Exception as exc:
            self.logger.error(exc)
            raise exc

    def log_equation(self, player_id, l_1, l_2, op, correct):
        try:
            t_eq_exists = [int(player_id), str(l_1), str(op), str(l_2)]
            self.logger.debug("= start log equation =")
            self.logger.debug(t_eq_exists)
            select_eq_exists = "SELECT * FROM Equations WHERE Player_id = ? AND L1 = ? AND Op = ? AND L2 = ?"
            self.cursor.execute(select_eq_exists, t_eq_exists)
            rec_eq_exists = self.cursor.fetchall()
            if len(rec_eq_exists) > 0:
                self.logger.debug(("equation exists!   ", l_1, " ", op, " ", l_2, " for player id ", player_id))
                self.logger.debug(str(rec_eq_exists[0]))
                self.logger.debug("==")

                #so update equation in DB depending on correct parameter: increase Cnt_correct or Cnt.
                cnt_corr = rec_eq_exists[0][4]
                cnt_bad = rec_eq_exists[0][5]
                self.logger.debug(("loaded: correct: ", cnt_corr, "  and bad: ", cnt_bad))
                if correct:
                    cnt_corr += 1
                else:
                    cnt_bad += 1
                self.logger.debug(("updated: correct: ", cnt_corr, "  and bad: ", cnt_bad))
                t_eq_upd = (int(cnt_corr), int(cnt_bad), int(player_id), str(l_1), str(op), str(l_2))
                self.logger.debug(t_eq_upd)
                sql_upd_eq = "UPDATE Equations SET Cnt_correct = ?, Cnt_bad = ? WHERE " \
                             "Player_id = ? AND L1 = ? AND Op = ? AND L2 = ?"
                self.cursor.execute(sql_upd_eq, t_eq_upd)
                self.logger.debug(("Total number of rows updated :", self.conn.total_changes))
                self.conn.commit()
                self.logger.debug("= equation updated =")
            else:
                self.logger.debug(("equation DOESN'T exist!   ", l_1, " ", op, " ", l_2, " for player id ", player_id))

                #so insert equation into DB
                cnt_corr = 0
                cnt_bad = 0
                if correct:
                    cnt_corr = 1
                else:
                    cnt_bad = 1
                t_eq_add = [int(player_id), str(l_1), str(op), str(l_2), int(cnt_corr), int(cnt_bad)]
                self.cursor.execute('INSERT INTO Equations (Player_id, L1, Op, L2, Cnt_correct, Cnt_bad) '
                                    'VALUES (?, ?, ?, ?, ?, ?)', t_eq_add)
                self.conn.commit()
                self.logger.debug("= equation added into db =")
        except Exception as exc:
            self.logger.error(exc.__str__())
            raise exc

    def getTopWorstEquations(self, player_id, operator, top_N):
        """
        Pobiera z DB najgorszych top_N równań (lub mniej jeśli nie ma ich aż N) - czyli takich, gdzie użytkownik
        najcześciej się mylił, gdzie różnica bad - correct jest największa.
        Zwraca listę Equation
        Gdy nie ma top_N, zwracany jest None.
        :param player_id:
        :param operator:
        :param top_N:
        :return:
        """
        # sql_select_topN_v1 = "SELECT L1, Op, L2, Cnt_bad, Cnt_correct, Cnt_bad-Cnt_correct as roznica FROM Equations " \
        #                   "WHERE Player_id = ? AND Op = ? AND roznica > 0 ORDER BY roznica DESC LIMIT ?"

        sql_select_topN = "SELECT L1, Op, L2, Cnt_bad, Cnt_correct, Cnt_bad-Cnt_correct as roznica FROM Equations " \
                          "WHERE Player_id = ? AND Op = ? AND roznica > 0 ORDER BY roznica DESC, Cnt_bad DESC LIMIT ?"

        t_sql_topN = (int(player_id), str(operator), str(top_N))
        self.cursor.execute(sql_select_topN, t_sql_topN)
        rec_topN = self.cursor.fetchall()
        self.logger.debug(("rec_topN = \n", rec_topN))
        if len(rec_topN) > 0:
            # są równania do poprawy
            ret_topN_eq = list()
            for rec in rec_topN:
                self.logger.debug(("==>  ", rec))
                p_equation = Equation(int(rec[0]), rec[1], int(rec[2]))
                ret_topN_eq.append(p_equation)
            return ret_topN_eq
        else:
            # nie ma równań do poprawy
            return None

    def getTopPlayersWithTheBiggestCountOfEquations(self, player_id, topN):
        # ToDo: To implement this
        sql_select_top_n = "select p.name, count(eq.player_id) from equations eq, player p " \
                           "where p.id =  eq.player_id group by eq.player_id"
        raise NotImplementedError("Function getTopPlayersWithTheBiggestCountOfEquations is not implemented yet.")


class Statistic(object):
    def __init__(self, player_name):
        self.player_name = player_name
        self.file_name = player_name + ".csv"
        self.file_path_name= os.getcwd() + "\\" + self.file_name
        self.equation_list = None
        self.logger = logging.getLogger()

    def load_statistic_from_file(self):
        """
        Load statistic from csv file and returns list of namedtuple('EquationRecord', 'equation, number_1, operator,
        number_2, ans_correct, ans_bad').
        Raises FileNotFoundError if file doesn't exist.
        :return:
        """
        if not self.is_file_exist():
            # file doesn't exist
            self.equation_list = list()
            raise FileNotFoundError("File " + self.file_path_name + "doesn't exist.")

        EquationRecord = namedtuple('EquationRecord', 'equation, number_1, operator, number_2, ans_correct, ans_bad')
        equation_list = list()
        f = open(self.file_path_name, "r", newline='')
        for eqt in map(EquationRecord._make, csv.reader(f)):
            # print(eqt.equation, "correct: ", eqt.ans_correct, " bad: ", eqt.ans_bad)
            equation_list.append(eqt)

        f.close()
        self.equation_list = equation_list
        return self.equation_list

    def is_file_exist(self):
        return os.path.exists(self.file_path_name) and os.path.isfile(self.file_path_name)

    def _append_equation_to_file(self, equation, correct):
        with open(self.file_path_name, 'a', newline='') as f:
            writer = csv.writer(f)
            # data
            EquationRecord = namedtuple('EquationRecord', 'equation, number_1, operator, number_2, ans_correct, ans_bad')
            cnt_correct = 0
            cnt_bad = 0
            if correct:
                cnt_correct += 1
            else:
                cnt_bad += 1
            equal_pos = equation.__str__().find("=") - 1
            er = EquationRecord(equation=equation.__str__()[:equal_pos], number_1=str(equation.number_1),
                                operator=equation.operator,
                                number_2=equation.number_2, ans_correct=cnt_correct, ans_bad=cnt_bad)
            writer.writerow(list(er))
        f.close()
        self.load_statistic_from_file()

    def _write_header_and_equation_to_file(self, equation, correct):
        with open(self.file_path_name, 'w', newline='') as f:
            writer = csv.writer(f)
            # field header
            writer.writerow(('equation', 'number_1', 'operator', 'number_2', 'ans_correct', 'ans_bad'))
            # data
            EquationRecord = namedtuple('EquationRecord', 'equation, number_1, operator, number_2, ans_correct, ans_bad')
            cnt_correct = 0
            cnt_bad = 0
            if correct:
                cnt_correct += 1
            else:
                cnt_bad += 1
            equal_pos = equation.__str__().find("=") - 1
            er = EquationRecord(equation=equation.__str__()[:equal_pos], number_1=str(equation.number_1),
                                operator=equation.operator,
                                number_2=equation.number_2, ans_correct=cnt_correct, ans_bad=cnt_bad)
            writer.writerow(list(er))
        f.close()

        self.load_statistic_from_file()

    def _update_equation_in_file(self, equation, correct):
        try:
            temp_file_name = self.file_path_name + ".tmp"
            EquationRecord = namedtuple('EquationRecord', 'equation, number_1, operator, number_2, ans_correct, ans_bad')

            with open(self.file_path_name, 'r', newline='') as f, open(temp_file_name, 'w', newline='') as \
                    tempfile:
                writer = csv.writer(tempfile)

                for eqt in map(EquationRecord._make, csv.reader(f)):
                    # print(eqt.equation, "correct: ", eqt.ans_correct, " bad: ", eqt.ans_bad)
                    # equation_list.append(eqt)
                    leqt = list(eqt)
                    # print(eqt.equation, eqt.ans_bad)
                    # print(type(eqt))
                    if not eqt.ans_bad == "ans_bad":
                        if equation.__str__().startswith(eqt.equation):
                            ac = int(eqt.ans_correct)
                            ab = int(eqt.ans_bad)
                            if correct:
                                ac += 1
                            else:
                                ab += 1

                            eqt_upd = EquationRecord(equation=eqt.equation, number_1=eqt.number_1,
                                                     operator=eqt.operator, number_2=eqt.number_2,
                                                     ans_correct=str(ac), ans_bad=str(ab))
                            writer.writerow(list(eqt_upd))
                        else:
                            writer.writerow(list(eqt))
                    else:
                        writer.writerow(list(eqt))

            f.close()
            tempfile.close()
            shutil.move(temp_file_name, self.file_path_name)
        except Exception as exc:
            self.logger.error(exc)

    def add_equation_to_statistic(self, equation, correct):
        if self.equation_list is None:
            self.load_statistic_from_file()

        if self.is_file_exist():
            # append data: add new record or update existing equation

            # check if equation exists in file - if it exists in loaded self.equation_list
            # if yes then update existing row
            # or if no - insert new row
            if len(self.equation_list) > 0:
                # są jakieś wpisy
                # check if equation exists if file
                # if yes then update existing row
                # or if no - append new row
                EquationRecord = namedtuple('EquationRecord', 'equation, number_1, operator, number_2, ans_correct, ans_bad')
                equal_pos = equation.__str__().find("=") - 1
                cur_eqt = equation.__str__()[:equal_pos]
                el = [elem for elem in self.equation_list]
                existing_eqt_list = [elem for elem in self.equation_list if
                                     elem.equation == cur_eqt]
                if len(existing_eqt_list) >= 1:
                    # update existing row
                    self._update_equation_in_file(equation, correct)
                else:
                    # append new row
                    self._append_equation_to_file(equation, correct)
            else:
                # brak wpisów
                # insert new row
                self._append_equation_to_file(equation, correct)
        else:
            # create new file, write data
            self._write_header_and_equation_to_file(equation, correct)
