import unittest
from Rule import Rule, RuleException
from Game import Equation


class ParsingTest(unittest.TestCase):

    def test_rule_txt_as_none(self):
        exceptions = (RuleException)
        with self.assertRaises(exceptions):
            Rule.parse(None)

    def test_rule_txt_as_empty_string(self):
        exceptions = (RuleException)
        self.assertEqual([], Rule.parse(""))

    def test_rule_txt_with_invalid_element_01(self):
        exceptions = (RuleException)
        with self.assertRaises(exceptions):
            txt_rule = "L5s>=20".splitlines()
            Rule.parse(txt_rule)

    def test_rule_txt_with_invalid_element_02(self):
        exceptions = (RuleException)
        with self.assertRaises(exceptions):
            txt_rule = "12>=20".splitlines()
            Rule.parse(txt_rule)

    def test_rule_txt_with_missing_element(self):
        exceptions = (RuleException)
        with self.assertRaises(exceptions):
            txt_rule = " >=20".splitlines()
            Rule.parse(txt_rule)

    def test_rule_txt_with_invalid_operand_01(self):
        exceptions = (RuleException)
        with self.assertRaises(exceptions):
            txt_rule = "L1!=20".splitlines()
            Rule.parse(txt_rule)

    def test_rule_txt_with_invalid_operand_02(self):
        exceptions = (RuleException)
        with self.assertRaises(exceptions):
            txt_rule = "L1<>20".splitlines()
            Rule.parse(txt_rule)

    def test_rule_txt_with_missing_operand(self):
        exceptions = (RuleException)
        with self.assertRaises(exceptions):
            txt_rule = "L120".splitlines()
            Rule.parse(txt_rule)

    def test_rule_txt_with_invalid_value_01(self):
        exceptions = (RuleException)
        with self.assertRaises(exceptions):
            txt_rule = "L1>=L2".splitlines()
            Rule.parse(txt_rule)

    def test_rule_txt_with_invalid_value_02(self):
        exceptions = (RuleException)
        with self.assertRaises(exceptions):
            txt_rule = "L1>=10.6".splitlines()
            Rule.parse(txt_rule)

    def test_rule_txt_with_missing_value(self):
        exceptions = (RuleException)
        with self.assertRaises(exceptions):
            txt_rule = "L1>=".splitlines()
            Rule.parse(txt_rule)

    def test_rule_txt_with_one_rule(self):
        txt_rule = "L1>=20".splitlines()
        exp_result = [("L1", ">=", 20)]
        self.assertEqual(exp_result, Rule.parse(txt_rule))

    def test_rule_txt_with_two_rules(self):
        txt_rule = "L1>=20\n" \
                   "L2=3".splitlines()
        exp_result = [("L1", ">=", 20),
                      ("L2", "=", 3)]
        self.assertEqual(exp_result, Rule.parse(txt_rule))

    def test_rule_txt_with_three_rules(self):
        txt_rule = "L1>=20\n" \
                   "L2=3\n" \
                   "W<=90".splitlines()
        exp_result = [("L1", ">=", 20),
                      ("L2", "=", 3),
                      ("W", "<=", 90)]
        self.assertEqual(exp_result, Rule.parse(txt_rule))

    def test_rule_txt_with_one_rule_and_spaces(self):
        txt_rule = "L1 >= 20".splitlines()
        exp_result = [("L1", ">=", 20)]
        self.assertEqual(exp_result, Rule.parse(txt_rule))


class ValidateRules_W(unittest.TestCase):

    def test_W_01(self):
        txt_rule = "L1>0\n" \
                   "L1<10\n" \
                   "L2>0\n" \
                   "L2<10\n" \
                   "W<=90".splitlines()
        rules = Rule.parse(txt_rule)

        exceptions = (RuleException)
        with self.assertRaises(exceptions):
            Equation.validate_rules_for_W(rules)

    def test_W_01m(self):
        txt_rule = "L1>0\n" \
                   "L1<10\n" \
                   "L2>0\n" \
                   "L2<10\n" \
                   "W<10\n" \
                   "W<=90".splitlines()
        rules = Rule.parse(txt_rule)

        exceptions = (RuleException)
        with self.assertRaises(exceptions):
            Equation.validate_rules_for_W(rules)

    def test_W_02(self):
        txt_rule = "L1>0\n" \
                   "L1<10\n" \
                   "L2>0\n" \
                   "L2<10\n" \
                   "W>90".splitlines()
        rules = Rule.parse(txt_rule)

        exceptions = (RuleException)
        with self.assertRaises(exceptions):
            Equation.validate_rules_for_W(rules)

    def test_W_02m(self):
        txt_rule = "L1>0\n" \
                   "L1<10\n" \
                   "L2>0\n" \
                   "L2<10\n" \
                   "W>=10\n" \
                   "W>90".splitlines()
        rules = Rule.parse(txt_rule)

        exceptions = (RuleException)
        with self.assertRaises(exceptions):
            Equation.validate_rules_for_W(rules)

    def test_W_03(self):
        txt_rule = "L1>0\n" \
                   "L1<10\n" \
                   "L2>0\n" \
                   "L2<10\n" \
                   "W==90".splitlines()
        rules = Rule.parse(txt_rule)

        Equation.validate_rules_for_W(rules)

    def test_W_03m(self):
        txt_rule = "L1>0\n" \
                   "L1<10\n" \
                   "L2>0\n" \
                   "L2<10\n" \
                   "W=5\n" \
                   "W==90".splitlines()
        rules = Rule.parse(txt_rule)

        exceptions = (RuleException)
        with self.assertRaises(exceptions):
            Equation.validate_rules_for_W(rules)

    def test_W_04(self):
        txt_rule = "L1>0\n" \
                   "L1<10\n" \
                   "L2>0\n" \
                   "L2<10\n" \
                   "W<20\n" \
                   "W>90".splitlines()
        rules = Rule.parse(txt_rule)

        exceptions = (RuleException)
        with self.assertRaises(exceptions):
            Equation.validate_rules_for_W(rules)

    def test_W_05(self):
        txt_rule = "L1>0\n" \
                   "L1<10\n" \
                   "L2>0\n" \
                   "L2<10\n" \
                   "W==20\n" \
                   "W>90".splitlines()
        rules = Rule.parse(txt_rule)

        exceptions = (RuleException)
        with self.assertRaises(exceptions):
            Equation.validate_rules_for_W(rules)

    def test_W_05b(self):
        txt_rule = "L1>0\n" \
                   "L1<10\n" \
                   "L2>0\n" \
                   "L2<10\n" \
                   "W==20\n" \
                   "W<=90".splitlines()
        rules = Rule.parse(txt_rule)

        exceptions = (RuleException)
        with self.assertRaises(exceptions):
            Equation.validate_rules_for_W(rules)

    def test_W_06(self):
        txt_rule = "L1>0\n" \
                   "L1<10\n" \
                   "L2>0\n" \
                   "L2<10\n" \
                   "W>20\n" \
                   "W<90".splitlines()
        rules = Rule.parse(txt_rule)

        Equation.validate_rules_for_W(rules)