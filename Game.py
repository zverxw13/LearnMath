# -*- coding: utf-8 -*-
import LM_Utils
from random import randint, choice

from Rule import *

OPERATION_SUBTRACTION = "-"
OPERATION_ADDITION = "+"
OPERATION_MULTIPLY = "*"
OPERATION_DIVISION = "/"

RANGE_0_10 = {'from': 0, 'to': 10}
RANGE_0_20 = {'from': 0, 'to': 20}
RANGE_0_30 = {'from': 0, 'to': 30}
RANGE_0_40 = {'from': 0, 'to': 40}
RANGE_0_50 = {'from': 0, 'to': 50}
RANGE_0_100 = {'from': 0, 'to': 100}


# class Configuration

class ConfigEquation(object):
    def __init__(self, operator, range_dict, without_zero=True, custom_rules=None):
        """
        :param operator: one from "+" | "-" | "*"
        :param range_dict: dictionary with range {"from":min_value, "to":max_value}
        :param without_zero: set True to not random zero to equation elements | czy losować 0 do działań?
        :param custom_rules: custom rules for equation elements L1, L2, W. Array of tuples
        (element, operand, value) | reguły użytkownika dla L1, L2 i W. Array of tuples (element, operand, value)
        """
        self.operator = operator
        self.range_dict = range_dict
        self.without_zero = without_zero
        self.custom_rules = custom_rules


class ConfigAddition(ConfigEquation):
    def __init__(self, range_dict, without_zero=True, summand_1_condition=">=", summand_1_value=0,
                 summand_2_condition=">=", summand_2_value=0, result_condition=None, result_value=None,
                 custom_rules=None):
        """
        :param range_dict: zakres
        :param without_zero: czy losować 0 do działań?
        :param summand_1_condition: składnik_1 - warunek = ["<" | ">", "="]
        :param summand_1_value: składnik_1 - wartość
        :param summand_2_condition: składnik_2 - warunek = ["<" | ">", "="]
        :param summand_2_value: składnik_2 - wartość
        :param result_condition: wynik - warunek = ["<" | ">", "="]
        :param result_value: wynik - wartość
        :param custom_rules: reguły uzytkownika na L1, L2 i W. Array of tuples (element, operand, value)
        :return:
        """
        ConfigEquation.__init__(self, "+", range_dict, without_zero, custom_rules)
        self.summand_1_condition = summand_1_condition
        self.summand_1_value = summand_1_value
        self.summand_2_condition = summand_2_condition
        self.summand_2_value = summand_2_value
        self.result_condition = result_condition
        self.result_value = result_value


class ConfigSubtraction(ConfigEquation):
    def __init__(self, range_dict, without_zero=True, minuend_condition=">=", minuend_value=0,
                 subtrahend_condition=">=", subtrahend_value=0, minuend_ge_subtrahend=True, result_condition=
                 None, result_value=None, custom_rules=None):
        """
        :param range_dict: zakres
        :param without_zero: czy losować 0 dla odjemnej?
        :param minuend_condition: odjemna - warunek = ["<" | ">", "="]
        :param minuend_value: odjemna - wartość
        :param subtrahend_condition: odjemnik - warunek = ["<" | ">", "="
        :param subtrahend_value: odjemnik - wartość
        :param minuend_ge_subtrahend: odjemna większa bądź równa niż odjemnik, domyślnie True
        :param result_condition: wynik - warunek = ["<" | ">", "="]
        :param result_value: wynik - wartość
        :param custom_rules: reguły uzytkownika na L1, L2 i W. Array of tuples (element, operand, value)
        :return:
        """
        ConfigEquation.__init__(self, "-", range_dict, without_zero, custom_rules)
        self.minuend_condition = minuend_condition
        self.minuend_value = minuend_value
        self.subtrahend_condition = subtrahend_condition
        self.subtrahend_value = subtrahend_value
        self.minuend_ge_subtrahend = minuend_ge_subtrahend
        self.result_condition = result_condition
        self.result_value = result_value

class ConfigMultiply(ConfigEquation):
    def __init__(self, range_dict, without_zero=True, without_one = False, element_1_condition=">=", element_1_value=0,
                 element_2_condition=">=", element_2_value=1, result_condition=None, result_value=None, custom_rules=None):
        """

        :param range_dict: zakres (dictioniary = {"from":x, "to":y}, x,y - integers)
        :param without_zero: czy losować 0 do działań?
        :param element_1_condition: składnik 1 - warunek = ["<" | ">", "="]
        :param element_1_value: składnik 1 - wartość dla wyrażenia warunkowego
        :param element_2_condition: składnik 2 - warunek = ["<" | ">", "="]
        :param element_2_value: składnik 2 - wartość dla wyrażenia warunkowego
        :param result_condition: wynik - warunek = ["<" | ">", "="]
        :param result_value: wynik - wartość dla wyrażenia warunkowego
        :param custom_rules: reguły użytkownika na L1, L2 i W. Array of tuples (element, operand, value)
        :return:
        """
        ConfigEquation.__init__(self, "*", range_dict, without_zero, custom_rules)
        self.without_one = without_one
        self.element_1_condition = element_1_condition
        self.element_1_value = element_1_value
        self.element_2_condition = element_2_condition
        self.element_2_value = element_2_value
        self.result_condition = result_condition
        self.result_value = result_value



class Answers(object):
    @staticmethod
    def get_random_comment_for_answer(is_answer_correct, last_answer):
        CORRECT_ANSWERS = ["Brawo!", "Świetnie!", "Super!", "Wspaniale!", "Bardzo dobrze!", "Tak!", "Dobrze!",
                           "Bezbłędna odpowiedź!"]
        BAD_ANSWERS = ["Nie...", "Błąd...", "Pomyłka...", "Zły wynik...", "Niestety nie...", "Oj, nie...",
                       "Niepoprawnie...", "Błędna odpowiedź..."]
        if is_answer_correct:
            number = randint(0, len(CORRECT_ANSWERS) - 1)
            random = CORRECT_ANSWERS[number]
            while last_answer == CORRECT_ANSWERS[number]:
                number = randint(0, len(CORRECT_ANSWERS) - 1)
            comment = CORRECT_ANSWERS[number]
        else:
            number = randint(0, len(BAD_ANSWERS) - 1)
            random = BAD_ANSWERS[number]
            while last_answer == BAD_ANSWERS[number]:
                number = randint(0, len(BAD_ANSWERS) - 1)
            comment = BAD_ANSWERS[number]
        return comment


class Equation(object):
    def __init__(self, number_1, operator, number_2):
        self.number_1 = number_1
        self.operator = operator
        self.number_2 = number_2
        self.user_answer = None

    def __str__(self):
        return str(self.number_1) + " " + self.operator + " " + str(self.number_2) + " = " + str(self.user_answer)

    @staticmethod
    def get_hint_for_equation(equation):
        hint = ""
        if equation.operator == OPERATION_ADDITION:
            hint = Equation.get_hint_for_addition(equation)
        elif equation.operator == OPERATION_SUBTRACTION:
            hint = Equation.get_hint_for_subtraction(equation)
        elif equation.operator == OPERATION_MULTIPLY:
            hint = Equation.get_hint_for_multiply(equation)
        elif equation.operator == OPERATION_DIVISION:
            print("get_hint_for_division() - not handled yet")
        return hint

    @staticmethod
    def get_hint_for_multiply(eq):
        hint = "Brak podpowiedzi, sorry..."
        hint_const = str(eq.number_1) + " * " + str(eq.number_2) + " = "

        if eq.number_1 == 0 or eq.number_2 == 0:
            hint = hint_const
        elif eq.number_1 == 1 or eq.number_2 == 1:
            hint = hint_const
        else:
            exp = ""
            for i in range(eq.number_1):
                exp = exp + str(eq.number_2) + " + "
            exp_ok = exp[:len(exp)-3]
            hint_exp = exp_ok + " = "
            hint = hint_const + hint_exp

        return hint


    @staticmethod
    def get_hint_for_subtraction(eq):
        hint = "Brak podpowiedzi, sorry..."
        hint_const = str(eq.number_1) + " - " + str(eq.number_2) + " = "

        if (eq.number_1 > 10) and (eq.number_2 < 10) and (eq.number_1 - eq.number_2 < 10):  #
            #  np. 13-5, 16 - 8, itp
            # number_1 - number_2 = number_1 - to_ten - rest
            to_ten = eq.number_1 - 10
            rest = eq.number_2 - to_ten
            hint = str(eq.number_1) + " - " + str(eq.number_2) + " = " + str(eq.number_1) + " - " + str(
                to_ten) + " - " + str(rest) + " = ..."
            # print("hint: ", hint)

        n1_ile10 = int(eq.number_1 / 10)
        n1_ile1 = eq.number_1 - (n1_ile10 * 10)
        n2_ile10 = int(eq.number_2 / 10)
        n2_ile1 = eq.number_2 - (n2_ile10 * 10)

        if n1_ile1 - n2_ile1 < 0 :
            # jest pożyczka z dziesiątek
            n1_ile10_po_pozyczce = n1_ile10 - 1
            if n1_ile10_po_pozyczce == 0:
                # równanie typu: 12 - 8
                hint_exp = ""
                n1_ile_do_10 = eq.number_1 - 10
                hint_exp = str(eq.number_1) + " - " + str(n1_ile_do_10) + " - " + str(eq.number_2 - n1_ile_do_10) + \
                           " = "
                hint = hint_const + hint_exp
                return hint
            else:  # 44 - 8,  44 - 18, 91 - 82, ...
                # coś bardziej skomplikowanego
                # ToDo: sprawdzić jak to trzeba rozpisać!
                # 67 - 39 = 67 - 7 - 32 = 60 - 32 =
                hint_exp = ""
                hint_exp = hint_exp + str(eq.number_1) + " - " + str(n1_ile1) + " - " + str(eq.number_2 - n1_ile1) + \
                           " = "
                hint = hint_const + hint_exp
                # if eq.number_2 <= 9:
                #     hint_exp = ""
                #     hint_exp = hint_exp + str(n1_ile10_po_pozyczce * 10) + " + " if n1_ile10_po_pozyczce > 0 else \
                #         hint_exp
                #     hint_exp = hint_exp + str(10 + n1_ile1) + " - " if n1_ile1 >= 0 else hint_exp
                #     hint_exp = hint_exp + str(n2_ile1)
                return hint
        else:
            # nie ma pożyczki z dziesiątek
            # 15 - 5, 17 - 5, 28 - 3
            if n1_ile1 - n2_ile1 == 0:
                # np.: 15 - 5, 27 - 7
                hint = hint_const
            elif eq.number_2 == 10:
                hint = hint_const
            else:
                if n2_ile10 >= 1:
                    # np. 67 - 23 = 60 - 7 - 16 =
                    hint_exp = ""
                    hint_exp = hint_exp + str(eq.number_1) + " - " + str(n1_ile1) + " - " + \
                               str(eq.number_2 - n1_ile1) + " = "
                    hint = hint_const + hint_exp
                    pass
                else:
                    # np. 28 - 3
                    hint_exp = ""
                    hint_exp = str(n1_ile10 * 10) + " + " + str(n1_ile1) + " - " + str(eq.number_2) + " = "
                    hint = hint_const + hint_exp
            return hint

    @staticmethod
    def get_hint_for_addition(eq):
        hint = "Brak podpowiedzi, sorry..."
        hint_const = str(eq.number_1) + " + " + str(eq.number_2) + " = "

        n1_ile10 = int(eq.number_1 / 10)
        n1_ile1 = eq.number_1 - (n1_ile10 * 10)
        n2_ile10 = int(eq.number_2 / 10)
        n2_ile1 = eq.number_2 - (n2_ile10 * 10)

        if n1_ile1 + n2_ile1 <= 9 :
            #print("przy dodawaniu liczb nie ma przeniesienia na dziesiątki")
            # przy dodawaniu liczb nie ma przeniesienia na dziesiątki
            # np.: 13 + 13, 11 + 18, 34 + 25, 66 + 11, itp.
            # hint_exp = dziesiatki_n1 + dziesiatki_n2 + jednosci_n1 + jednosci_n2 + " = "
            hint_exp = ""
            hint_exp = hint_exp + str(n1_ile10 * 10) + " + " if n1_ile10 > 0 else hint_exp
            hint_exp = hint_exp + str(n2_ile10 * 10) + " + " if n2_ile10 > 0 else hint_exp
            hint_exp = hint_exp + str(n1_ile1) + " + " + str(n2_ile1) + " = "
            hint = hint_const + hint_exp
        else:
            #print("przy dodawaniu liczb jest przeniesienie na dziesiątki")
            # przy dodawaniu liczb jest przeniesienie na dziesiątki
            # np.: 13 + 18, 34 + 29, itp.
            n1_ile_do_10 = 10 - n1_ile1
            n2_reszta_1 = n2_ile1 - n1_ile_do_10
            # hint_exp = dziesiatki_n1 + dziesiatki_n2 + jednosci_n1 + n1_ile_do_10 + n2_reszta_1 + " = "
            if n1_ile10 > 0: #spr dla 7 + 13
                hint_exp = ""
                hint_exp = hint_exp + str(n1_ile10 * 10) + " + " if n1_ile10 > 0 else hint_exp
                hint_exp = hint_exp + str(n1_ile1) + " + " if n1_ile1 > 0 else hint_exp
                hint_exp = hint_exp + str(n1_ile_do_10) + " + " if n1_ile_do_10 > 0 else hint_exp
                hint_exp = hint_exp + str(n2_ile10 * 10) + " + " if n2_ile10 > 0 else hint_exp
                hint_exp = hint_exp + str(n2_reszta_1) + " = " if n2_reszta_1 > 0 else hint_exp

                if hint_exp[len(hint_exp)-2] == "+":
                    hint_exp = hint_exp[:len(hint_exp)-2] + "= "
                # hint_exp = str(n1_ile10 * 10) + " + " + str(n2_ile10 * 10) + " + " + \
                #            str(n1_ile1) + " + " + str(n1_ile_do_10) + " + " + str(n2_reszta_1) + " = "
            else:
                hint_exp = ""
                hint_exp = hint_exp + str(n1_ile1) + " + " if n1_ile1 > 0 else hint_exp
                hint_exp = hint_exp + str(n1_ile_do_10) + " + " if n1_ile_do_10 > 0 else hint_exp
                hint_exp = hint_exp + str(n2_ile10 * 10) + " + " if n2_ile10 > 0 else hint_exp
                hint_exp = hint_exp + str(n2_reszta_1) + " = " if n2_reszta_1 > 0 else hint_exp
                if hint_exp[len(hint_exp)-2] == "+":
                    hint_exp = hint_exp[:len(hint_exp)-2] + "= "
                # hint_exp = str(n1_ile1) + " + " + str(n2_ile10 * 10) + " + " + \
                #            str(n1_ile_do_10) + " + " + str(n2_reszta_1) + " = "

            hint = hint_const + hint_exp

        return hint

    @staticmethod
    def is_subtraction_result_met(n1, n2, result_condition, result_value):
        """
        Returns True if conditon is met for: n1 - n2 result_condition result_value
        :rtype : bool
        """
        if result_condition is None and result_value is None:
            return True
        elif result_condition is not None and result_value is not None:
            if result_condition == "=" or result_condition == "==":
                return n1 - n2 == result_value
            elif result_condition == "<":
                return n1 - n2 < result_value
            elif result_condition == "<=":
                return n1 - n2 <= result_value
            elif result_condition == ">":
                return n1 - n2 > result_value
            elif result_condition == ">=":
                return n1 - n2 >= result_value
        else:
            return False

    @staticmethod
    def is_addition_result_met(n1, n2, result_condition, result_value):
        """
        Returns True if conditon is met for: n1 + n2 result_condition result_value
        :rtype : bool
        """
        if result_condition is None and result_value is None:
            return True
        elif result_condition is not None and result_value is not None:
            if result_condition == "=" or result_condition == "==":
                return n1 + n2 == result_value
            elif result_condition == "<":
                return n1 + n2 < result_value
            elif result_condition == "<=":
                return n1 + n2 <= result_value
            elif result_condition == ">":
                return n1 + n2 > result_value
            elif result_condition == ">=":
                return n1 + n2 >= result_value
        else:
            return False

    @staticmethod
    def is_multiply_result_met(n1, n2, result_condition, result_value):
        """
        Returns True if conditon is met for: n1 * n2 result_condition result_value
        :rtype : bool
        """
        if result_condition is None and result_value is None:
            return True
        elif result_condition is not None and result_value is not None:
            if result_condition == "=" or result_condition == "==":
                return n1 * n2 == result_value
            elif result_condition == "<":
                return n1 * n2 < result_value
            elif result_condition == "<=":
                return n1 * n2 <= result_value
            elif result_condition == ">":
                return n1 * n2 > result_value
            elif result_condition == ">=":
                return n1 * n2 >= result_value
        else:
            return False


    @staticmethod
    def prepareEquationAddition(game_config):
        if game_config.custom_rules is None:
            return Equation.prepareEquationAdditionSimpleConfig(game_config)
        else:
            return Equation.prepareEquationAdditionConfigCustomRules(game_config)

    @staticmethod
    def prepareEquationAdditionConfigCustomRules(game_config):
        c_rules = game_config.custom_rules

        condition_end = False
        conditions_for_rules = []

        min_value_l1 = None
        max_value_l1 = None
        min_value_l1, max_value_l1 = Equation.getMinMaxValues(Rule.RULE_ELEMENT_1, c_rules)

        min_value_l2 = None
        max_value_l2 = None
        min_value_l2, max_value_l2 = Equation.getMinMaxValues(Rule.RULE_ELEMENT_2, c_rules)

        min_value_w = None
        max_value_w = None
        min_value_w, max_value_w = Equation.getMinMaxValues(Rule.RULE_ELEMENT_W, c_rules)

        while not condition_end:
            conditions_for_rules = []
            for i in c_rules:
                conditions_for_rules.append(False)

            try:
                if min_value_l1 is None or max_value_l1 is None:
                    raise RuleException("Rules for L1 don't determine it's min and max value.")
                n1 = randint(min_value_l1, max_value_l1)
                # print("n1 = ", n1)

                if min_value_l2 is None or max_value_l2 is None:
                    raise RuleException("Rules for L2 don't determine it's min and max value.")
                n2 = randint(min_value_l2, max_value_l2)
                # print("n2 = ", n2)

                idx = 0
                Equation.validate_rules_for_W(c_rules)
                for rule in c_rules:
                    if rule[0] == Rule.RULE_ELEMENT_1 or rule[0] == Rule.RULE_ELEMENT_2:
                        conditions_for_rules[idx] = True
                    elif rule[0] == Rule.RULE_ELEMENT_W:
                        if Equation.is_addition_result_met(n1, n2, rule[1], rule[2]):
                            conditions_for_rules[idx] = True
                    idx += 1

                condition_user_rules = True
                for idx in range(len(conditions_for_rules)):
                    condition_user_rules = condition_user_rules and conditions_for_rules[idx]

                condition_end = condition_user_rules
            except ValueError as ve:
                #  Temporary !!!!!!!!!!!!!!!!!!!!!!!!!!!!
                if ve.__str__().find("empty range for randrange()") >= 0:
                    # there is invalid range for L1 or L2, eg.: [50, 20]
                    raise RuleException("Empty set evauluated for given rules")
            except Exception as exc:
                # print(exc.__str__())
                raise exc

        # print("n1 = ", n1, "   and n2 = ", n2)

        # print(game_config.__str__())
        p_equation = Equation(n1, OPERATION_ADDITION, n2)
        return p_equation

    @staticmethod
    def prepareEquationAdditionSimpleConfig(game_config):
        number_1 = game_config.summand_1_value  # składnik_1
        number_1_condition = game_config.summand_1_condition
        number_2 = game_config.summand_2_value  # składnik_2
        number_2_condition = game_config.summand_2_condition
        number_range_dict = game_config.range_dict  # range
        number_range_min = number_range_dict["from"]
        number_range_max = number_range_dict["to"]

        condition_end = False
        while not condition_end:
            condition_addition_result_met = True
            condition_without_zero = True
            # print("n1")
            n1 = LM_Utils.random_int_with_additional_condition(number_range_min, number_range_max, number_1_condition,
                                                               number_1)
            # print("n2")
            n2 = LM_Utils.random_int_with_additional_condition(number_range_min, number_range_max, number_2_condition,
                                                            number_2)
            if (game_config.result_condition is not None) and (game_config.result_value is not None):
                # gdy podano warunek na wynik
                if not Equation.is_addition_result_met(n1, n2, game_config.result_condition,
                                                          game_config.result_value):
                    condition_addition_result_met = False

            if game_config.without_zero:
                if n1 == 0 or n2 == 0:
                    condition_without_zero = False

            condition_end = condition_addition_result_met and condition_without_zero

        # print("n1 = ", n1, "   and n2 = ", n2)

        # print(game_config.__str__())
        p_equation = Equation(n1, OPERATION_ADDITION, n2)
        return p_equation

    @staticmethod
    def prepareEquationSubtraction(game_config):
        if game_config.custom_rules is None:
            return Equation.prepareEquationSubtractionSimpleConfig(game_config)
        else:
            return Equation.prepareEquationSubtractionConfigCustomRules(game_config)

    @staticmethod
    def prepareEquationSubtractionConfigCustomRules(game_config):
        c_rules = game_config.custom_rules

        condition_end = False
        conditions_for_rules = []

        min_value_l1 = None
        max_value_l1 = None
        min_value_l1, max_value_l1 = Equation.getMinMaxValues(Rule.RULE_ELEMENT_1, c_rules)

        min_value_l2 = None
        max_value_l2 = None
        min_value_l2, max_value_l2 = Equation.getMinMaxValues(Rule.RULE_ELEMENT_2, c_rules)

        min_value_w = None
        max_value_w = None
        min_value_w, max_value_w = Equation.getMinMaxValues(Rule.RULE_ELEMENT_W, c_rules)

        while not condition_end:
            conditions_for_rules = []
            for i in c_rules:
                conditions_for_rules.append(False)

            try:
                if min_value_l1 is None or max_value_l1 is None:
                    raise RuleException("Rules for L1 don't determine it's min and max value.")
                n1 = randint(min_value_l1, max_value_l1)
                # print("n1 = ", n1)

                if min_value_l2 is None or max_value_l2 is None:
                    raise RuleException("Rules for L2 don't determine it's min and max value.")
                n2 = randint(min_value_l2, max_value_l2)
                # print("n2 = ", n2)

                idx = 0
                Equation.validate_rules_for_W(c_rules)
                for rule in c_rules:
                    if rule[0] == Rule.RULE_ELEMENT_1 or rule[0] == Rule.RULE_ELEMENT_2:
                        conditions_for_rules[idx] = True
                    elif rule[0] == Rule.RULE_ELEMENT_W:
                        if Equation.is_subtraction_result_met(n1, n2, rule[1], rule[2]):
                            conditions_for_rules[idx] = True
                    idx += 1

                condition_user_rules = True
                for idx in range(len(conditions_for_rules)):
                    condition_user_rules = condition_user_rules and conditions_for_rules[idx]

                condition_end = condition_user_rules
            except ValueError as ve:
                #  Temporary !!!!!!!!!!!!!!!!!!!!!!!!!!!!
                if ve.__str__().find("empty range for randrange()") >= 0:
                    # there is invalid range for L1 or L2, eg.: [50, 20]
                    raise RuleException("Empty set evauluated for given rules")
            except Exception as exc:
                # print(exc.__str__())
                raise exc

        # print("n1 = ", n1, "   and n2 = ", n2)

        # print(game_config.__str__())
        p_equation = Equation(n1, OPERATION_SUBTRACTION, n2)
        return p_equation

    @staticmethod
    def prepareEquationSubtractionSimpleConfig(game_config):
        number_1 = game_config.minuend_value  # odjemna
        number_1_condition = game_config.minuend_condition
        number_2 = game_config.subtrahend_value  # odjemnik
        number_2_condition = game_config.subtrahend_condition
        number_range_dict = game_config.range_dict  # range
        number_range_min = number_range_dict["from"]
        number_range_max = number_range_dict["to"]

        condition_end = False
        while not condition_end:
            condition_minuend_ge_subtrahend = True
            condition_subtraction_result_met = True
            condition_without_zero = True
            # print("n1")
            n1 = LM_Utils.random_int_with_additional_condition(number_range_min, number_range_max, number_1_condition,
                                                               number_1)
            # print("n2")
            n2 = LM_Utils.random_int_with_additional_condition(number_range_min, number_range_max, number_2_condition,
                                                               number_2)
            if game_config.minuend_ge_subtrahend:
                # gdy odjemna ma być większa bądź równa niż odjemnik
                if not (n1 >= n2):
                    condition_minuend_ge_subtrahend = False

            if (game_config.result_condition is not None) and (game_config.result_value is not None):
                # gdy podano warunek na wynik
                if not Equation.is_subtraction_result_met(n1, n2, game_config.result_condition,
                                                          game_config.result_value):
                    condition_subtraction_result_met = False

            if game_config.without_zero:
                if n2 == 0:
                    condition_without_zero = False

            condition_end = condition_minuend_ge_subtrahend \
                            and condition_subtraction_result_met \
                            and condition_without_zero

        # print("n1 = ", n1, "   and n2 = ", n2)

        # print(game_config.__str__())
        p_equation = Equation(n1, OPERATION_SUBTRACTION, n2)

        return p_equation

    @staticmethod
    def getMinMaxValues(str_element, custom_rules):
        """
        Returns min_value, max_value for str_element basing on custom_rules
        :param str_element: one from ["L1|"L2"|"W"]
        :param custom_rules: array of tuples (element, operand, value). Value is int.
        :return: min_value, max_value for str_element basing on custom_rules
        """

        el_min = None
        el_max = None
        for rule in custom_rules:
            if rule[0] == str_element:
                # print(str_element + " rule found: " + rule[0] + " " + rule[1] + " " + str(rule[2]))
                r_op = rule[1]
                r_val = rule[2]
                if r_op == "==" or r_op == "=":
                    el_max = r_val
                    el_min = r_val
                elif r_op == "<=":
                    el_max = r_val
                elif r_op == "<":
                    el_max = r_val - 1
                elif r_op == ">=":
                    el_min = r_val
                elif r_op == ">":
                    el_min = r_val + 1
        return el_min, el_max

    @staticmethod
    def validate_rules_for_W(custom_rules):
        """
        Raises RuleException when rules for W are not valid.
        :param custom_rules:
        :return:
        """
        op_eq = 0
        op_less = 0
        op_greater = 0

        for rule in custom_rules:
            if rule[0] == Rule.RULE_ELEMENT_W:
                if rule[1] == "==" or rule[1] == "=":
                    op_eq += 1
                elif rule[1] == "<" or rule[1] == "<=":
                    op_less += 1
                elif rule[1] == ">" or rule[1] == ">=":
                    op_greater += 1

        if op_eq > 1:
            raise RuleException("Rules for W contain multiple rules with operator = or ==.\n "
                                "It's not allowed - fix the rules.")

        if op_eq > 0 and (op_less + op_greater) > 0:
            # gdy jest operator = i przynajmniej jeden z operatorów >=, >, <, <=
            raise RuleException("Rules for W contain operator == and another operator.\n "
                                "It's not allowed - fix the rules.")
        if op_less > 1:
            raise RuleException("Rules for W contain multiple rules with operator < or <=.\n "
                                "It's not allowed - fix the rules.")
        if op_greater > 1:
            raise RuleException("Rules for W contain multiple rules with operator > or >=.\n "
                                "It's not allowed - fix the rules.")

        if (op_less == 1 and op_greater == 0) or (op_less == 0 and op_greater == 1):
            raise RuleException("Rules for W don't contain rules to determine min and max value for W.\n "
                                "It's not allowed - fix the rules.")

        min, max = Equation.getMinMaxValues("W", custom_rules)
        if min is not None and max is not None:
            if min > max:
                raise RuleException("Rules for W contain rules which determine an empty set for W values.\n "
                                    "It's not allowed - fix the rules.")

    @staticmethod
    def prepareEquationMultiply(game_config):
        if game_config.custom_rules is None:
            return Equation.prepareEquationMultiplySimpleConfig(game_config)
        else:
            return Equation.prepareEquationMultiplyConfigCustomRules(game_config)

    @staticmethod
    def prepareEquationMultiplyConfigCustomRules(game_config):
        c_rules = game_config.custom_rules

        condition_end = False
        conditions_for_rules = []

        min_value_l1 = None
        max_value_l1 = None
        min_value_l1, max_value_l1 = Equation.getMinMaxValues(Rule.RULE_ELEMENT_1, c_rules)

        min_value_l2 = None
        max_value_l2 = None
        min_value_l2, max_value_l2 = Equation.getMinMaxValues(Rule.RULE_ELEMENT_2, c_rules)

        min_value_w = None
        max_value_w = None
        min_value_w, max_value_w = Equation.getMinMaxValues(Rule.RULE_ELEMENT_W, c_rules)

        while not condition_end:
            conditions_for_rules = []
            for i in c_rules:
                conditions_for_rules.append(False)

            try:
                if min_value_l1 is None or max_value_l1 is None:
                    raise RuleException("Rules for L1 don't determine it's min and max value.")
                n1 = randint(min_value_l1, max_value_l1)
                # print("n1 = ", n1)

                if min_value_l2 is None or max_value_l2 is None:
                    raise RuleException("Rules for L2 don't determine it's min and max value.")
                n2 = randint(min_value_l2, max_value_l2)
                # print("n2 = ", n2)

                idx = 0
                Equation.validate_rules_for_W(c_rules)
                for rule in c_rules:
                    if rule[0] == Rule.RULE_ELEMENT_1 or rule[0] == Rule.RULE_ELEMENT_2:
                        conditions_for_rules[idx] = True
                    elif rule[0] == Rule.RULE_ELEMENT_W:
                        if Equation.is_multiply_result_met(n1, n2, rule[1], rule[2]):
                            conditions_for_rules[idx] = True
                    idx += 1

                condition_user_rules = True
                for idx in range(len(conditions_for_rules)):
                    condition_user_rules = condition_user_rules and conditions_for_rules[idx]

                condition_end = condition_user_rules
            except ValueError as ve:
                #  Temporary !!!!!!!!!!!!!!!!!!!!!!!!!!!!
                if ve.__str__().find("empty range for randrange()") >= 0:
                    # there is invalid range for L1 or L2, eg.: [50, 20]
                    raise RuleException("Empty set evauluated for given rules")
            except Exception as exc:
                # print(exc.__str__())
                raise exc

        # print("n1 = ", n1, "   and n2 = ", n2)

        # print(game_config.__str__())
        p_equation = Equation(n1, OPERATION_MULTIPLY, n2)
        return p_equation

    @staticmethod
    def prepareEquationMultiplySimpleConfig(game_config):
        number_1 = game_config.element_1_value
        number_1_condition = game_config.element_1_condition
        number_2 = game_config.element_2_value
        number_2_condition = game_config.element_2_condition
        number_range_dict = game_config.range_dict  # range
        number_range_min = number_range_dict["from"]
        number_range_max = number_range_dict["to"]

        condition_end = False
        while not condition_end:
            # condition_minuend_ge_subtrahend = True
            condition_multiply_result_met = True
            condition_without_zero = True
            condition_without_one = True
            # print("n1")
            n1 = LM_Utils.random_int_with_additional_condition(number_range_min, number_range_max, number_1_condition,
                                                               number_1)
            # print("n2")
            n2 = LM_Utils.random_int_with_additional_condition(number_range_min, number_range_max, number_2_condition,
                                                               number_2)
            # if game_config.minuend_ge_subtrahend:
            #     # gdy odjemna ma być większa bądź równa niż odjemnik
            #     if not (n1 >= n2):
            #         condition_minuend_ge_subtrahend = False

            if (game_config.result_condition is not None) and (game_config.result_value is not None):
                # gdy podano warunek na wynik
                if not Equation.is_multiply_result_met(n1, n2, game_config.result_condition,
                                                          game_config.result_value):
                    condition_multiply_result_met = False

            if game_config.without_zero:
                if n1 == 0 or n2 == 0:
                    condition_without_zero = False

            if game_config.without_one:
                if n1 == 1 or n2 == 1:
                    condition_without_one = False

            condition_end = condition_multiply_result_met \
                            and condition_without_zero \
                            and condition_without_one

        # print("n1 = ", n1, "   and n2 = ", n2)

        # print(game_config.__str__())
        p_equation = Equation(n1, OPERATION_MULTIPLY, n2)

        return p_equation


    @staticmethod
    def prepareEquationBasingOnSingleOperator(g_config):
        n_equation = None

        if g_config.operator == OPERATION_ADDITION:
            n_equation = Equation.prepareEquationAddition(g_config)
        elif g_config.operator == OPERATION_SUBTRACTION:
            n_equation = Equation.prepareEquationSubtraction(g_config)
        elif g_config.operator == OPERATION_MULTIPLY:
            n_equation = Equation.prepareEquationMultiply(g_config)
        elif g_config.operator == OPERATION_DIVISION:
            print("prepareEquationDivision() - not handled yet")

        return n_equation

    @staticmethod
    def prepareEquationBasingOnMultipleOperator(g_config_list):
        n_equation = None

        g_config = choice(g_config_list)
        # r = randint(0, len(g_config_list-1))
        # g_config =  g_config_list[r]
        if g_config.operator == OPERATION_ADDITION:
            n_equation = Equation.prepareEquationAddition(g_config)
        elif g_config.operator == OPERATION_SUBTRACTION:
            n_equation = Equation.prepareEquationSubtraction(g_config)
        elif g_config.operator == OPERATION_MULTIPLY:
            print("prepareEquationMultiply() - not handled yet")
        elif g_config.operator == OPERATION_DIVISION:
            print("prepareEquationDivision() - not handled yet")

        return n_equation


    def checkUserResult(self, userResult):
        """ Check user answer against correct result.
        Return True if userResult is correct answer, False otherwise.
        """
        self.user_answer = userResult
        correctResult = 0
        # if self.operator == OPERATION_ADDITION:
        #     correctResult = self.number_1 + self.number_2
        # elif self.operator == OPERATION_SUBTRACTION:
        #     correctResult = self.number_1 - self.number_2
        # elif self.operator == OPERATION_MULTIPLY:
        #     correctResult = self.number_1 * self.number_2
        # elif self.operator == OPERATION_DIVISION:
        #     correctResult = self.number_1 / self.number_2

        correctResult2 = eval(str(self.number_1) + self.operator + str(self.number_2))

        return correctResult2 == userResult
