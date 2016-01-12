class RuleException(Exception):
    def __init__(self, desc, *args):
        self.desc = desc
        super(RuleException, self).__init__(desc, *args)

    def __str__(self):
        return "RuleException: " + self.desc


class RuleParsingSingleLineException(RuleException):
    def __init__(self, desc, *args):
        self.desc = desc
        super(RuleParsingSingleLineException, self).__init__(desc, *args)

    def __str__(self):
        return "RuleParsingSingleLineException: " + self.desc


class Rule(object):
    RULE_ELEMENT_1 = "L1"
    RULE_ELEMENT_2 = "L2"
    RULE_ELEMENT_W = "W"
    RULE_ELEMENTS = [RULE_ELEMENT_1, RULE_ELEMENT_2, RULE_ELEMENT_W]
    RULE_OPERANDS = ["==", "=", "<=", "<", ">=", ">"]

    @staticmethod
    def parse(txt_rule):
        """
        Function return array of tuples (element, operand, value). Each tuple relates to one line of txt_rule.
        Returns empty array when txt_rule is an empty array.
        :param txt_rule: array of string rules. Each rule has to be as array element.
        :return array of tuples (element, operand, value)
        """
        arr_rules = []
        print(type(txt_rule))
        # if isinstance(txt_rule, array)
        try:
            for line in txt_rule:
                try:
                    res_tuple = Rule.parseSingleLine(line)
                    arr_rules.append(res_tuple)
                except RuleParsingSingleLineException as rexc:
                    print(rexc.__str__())
                    raise rexc
            return arr_rules
        except TypeError:
            # print("raising RuleException from Rule.parse method")
            raise RuleException("Can't parse None (string expected)")
        except Exception as exc:
            print(exc)
            raise exc

    @staticmethod
    def parseSingleLine(str_one_rule):
        """

        :param str_one_rule: string
        :return:
        """
        element = None
        operand = None
        value = None

        print("DEBUG: str_one_rule = " + str_one_rule)

        # checking and parsing elements
        element_ok = False
        for re in Rule.RULE_ELEMENTS:
            if str_one_rule.startswith(re):
                element_ok = True
                element = re
                break
        if not element_ok:
            print("in parseSingleLine: Invalid rule element - raising error")
            raise RuleParsingSingleLineException("Invalid rule: " + str_one_rule + "\n" + "Invalid rule element.")
        str_operand_and_value = str_one_rule[len(element):]
        str_operand_and_value = str_operand_and_value.lstrip()
        print("DEBUG: str_operand_and_value = " + str_operand_and_value)

        # checking and parsing operands
        operand_ok = False
        for ro in Rule.RULE_OPERANDS:
            if str_operand_and_value.startswith(ro):
                operand_ok = True
                operand = ro
                break
        if not operand_ok:
            raise RuleParsingSingleLineException("Invalid rule: " + str_one_rule + "\n" + "Invalid rule operand.")
        str_value = str_operand_and_value[len(operand):]
        str_value = str_value.strip()
        print("DEBUG: str_value = " + str_value)

        # checking and parsing value
        value_ok = False
        if len(str_value) <= 0:
            raise RuleParsingSingleLineException("Invalid rule: " + str_one_rule + "\n" + "Missing value.")
        if not str_value.isdigit():
            raise RuleParsingSingleLineException("Invalid rule: " + str_one_rule + "\n" +
                                                 "Invalid value (should be integer)")
        try:
            value = int(str_value)
        except Exception as exc:
            raise RuleParsingSingleLineException("Invalid rule: " + str_one_rule +
                                                 "\n" + "Invalid value (should be integer.")

        # prepare returning tuple
        ret_tuple = (element, operand, value)
        return ret_tuple