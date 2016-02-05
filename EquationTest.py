import unittest
from Game import *


class GeneralTests(unittest.TestCase):

    def test_randint_first_gt_second(self):
        a = 40
        b = 20
        res = randint(a, b)
        self.assertGreaterEqual(res, b)
        self.assertLessEqual(res, a)


class AddingTest(unittest.TestCase):

    def test_adding_7_13(self):
        # 7 + 13
        n1 = 7
        n2 = 13
        op = "+"
        eq = Equation(n1, op, n2)
        self.assertTrue(eq.check_user_result(n1 + n2), eq.__str__() + " should be " + str(n1 + n2))
        print(">>> " + eq.get_hint_for_equation(eq))
        self.assertEqual(eq.get_hint_for_equation(eq), "7 + 13 = 7 + 3 + 10 = ")

    def test_adding_7_18(self):
        # 7 + 18
        n1 = 7
        n2 = 18
        op = "+"
        eq = Equation(n1, op, n2)
        self.assertTrue(eq.check_user_result(n1 + n2), eq.__str__() + " should be " + str(n1 + n2))
        print(">>> " + eq.get_hint_for_equation(eq))
        self.assertEqual(eq.get_hint_for_equation(eq), "7 + 18 = 7 + 3 + 10 + 5 = ")

    def test_adding_13_7(self):
        # 13 + 7
        n1 = 13
        n2 = 7
        op = "+"
        eq = Equation(n1, op, n2)
        self.assertTrue(eq.check_user_result(n1 + n2), eq.__str__() + " should be " + str(n1 + n2))
        print(">>> " + eq.get_hint_for_equation(eq))
        self.assertEqual(eq.get_hint_for_equation(eq), "13 + 7 = 10 + 3 + 7 = ")

    def test_adding_18_7(self):
        # 18 + 7
        n1 = 18
        n2 = 7
        op = "+"
        eq = Equation(n1, op, n2)
        self.assertTrue(eq.check_user_result(n1 + n2), eq.__str__() + " should be " + str(n1 + n2))
        print(">>> " + eq.get_hint_for_equation(eq))
        self.assertEqual(eq.get_hint_for_equation(eq), "18 + 7 = 10 + 8 + 2 + 5 = ")

    def test_adding_7_3(self):
        # 7 + 3
        n1 = 7
        n2 = 3
        op = "+"
        eq = Equation(n1, op, n2)
        self.assertTrue(eq.check_user_result(n1 + n2), eq.__str__() + " should be " + str(n1 + n2))
        print(">>> " + eq.get_hint_for_equation(eq))
        self.assertEqual(eq.get_hint_for_equation(eq), "7 + 3 = 7 + 3 = ")

    def test_adding_17_13(self):
        # 17 + 13
        n1 = 17
        n2 = 13
        op = "+"
        eq = Equation(n1, op, n2)
        self.assertTrue(eq.check_user_result(n1 + n2), eq.__str__() + " should be " + str(n1 + n2))
        print(">>> " + eq.get_hint_for_equation(eq))
        self.assertEqual(eq.get_hint_for_equation(eq), "17 + 13 = 10 + 7 + 3 + 10 = ")

    def test_adding_27_31(self):
        # 27 + 31
        n1 = 27
        n2 = 31
        op = "+"
        eq = Equation(n1, op, n2)
        self.assertTrue(eq.check_user_result(n1 + n2), eq.__str__() + " should be " + str(n1 + n2))
        print(">>> " + eq.get_hint_for_equation(eq))
        self.assertEqual(eq.get_hint_for_equation(eq), "27 + 31 = 20 + 30 + 7 + 1 = ")

    def test_adding_27_39(self):
        # 27 + 39
        n1 = 27
        n2 = 39
        op = "+"
        eq = Equation(n1, op, n2)
        self.assertTrue(eq.check_user_result(n1 + n2), eq.__str__() + " should be " + str(n1 + n2))
        print(">>> " + eq.get_hint_for_equation(eq))
        self.assertEqual(eq.get_hint_for_equation(eq), "27 + 39 = 20 + 7 + 3 + 30 + 6 = ")

    def test_adding_27_0(self):
        # 27 + 0
        n1 = 27
        n2 = 0
        op = "+"
        eq = Equation(n1, op, n2)
        self.assertTrue(eq.check_user_result(n1 + n2), eq.__str__() + " should be " + str(n1 + n2))
        print(">>> " + eq.get_hint_for_equation(eq))
        self.assertEqual(eq.get_hint_for_equation(eq), "27 + 0 = 20 + 7 + 0 = ")

    def test_adding_3_0(self):
        # 3 + 0
        n1 = 3
        n2 = 0
        op = "+"
        eq = Equation(n1, op, n2)
        self.assertTrue(eq.check_user_result(n1 + n2), eq.__str__() + " should be " + str(n1 + n2))
        print(">>> " + eq.get_hint_for_equation(eq))
        self.assertEqual(eq.get_hint_for_equation(eq), "3 + 0 = 3 + 0 = ")

    def test_adding_0_5(self):
        # 0 + 5
        n1 = 0
        n2 = 5
        op = "+"
        eq = Equation(n1, op, n2)
        self.assertTrue(eq.check_user_result(n1 + n2), eq.__str__() + " should be " + str(n1 + n2))
        print(">>> " + eq.get_hint_for_equation(eq))
        self.assertEqual(eq.get_hint_for_equation(eq), "0 + 5 = 0 + 5 = ")

    def test_adding_5_5(self):
        # 5 + 5
        n1 = 5
        n2 = 5
        op = "+"
        eq = Equation(n1, op, n2)
        self.assertTrue(eq.check_user_result(n1 + n2), eq.__str__() + " should be " + str(n1 + n2))
        print(">>> " + eq.get_hint_for_equation(eq))
        self.assertEqual(eq.get_hint_for_equation(eq), "5 + 5 = 5 + 5 = ")

    def test_adding_7_8(self):
        # 7 + 8
        n1 = 7
        n2 = 8
        op = "+"
        eq = Equation(n1, op, n2)
        self.assertTrue(eq.check_user_result(n1 + n2), eq.__str__() + " should be " + str(n1 + n2))
        print(">>> " + eq.get_hint_for_equation(eq))
        self.assertEqual(eq.get_hint_for_equation(eq), "7 + 8 = 7 + 3 + 5 = ")


class SubtractingTest(unittest.TestCase):

    def test_subtract_17_9(self):
        # 17 - 9
        n1 = 17
        n2 = 9
        op = "-"
        eq = Equation(n1, op, n2)
        self.assertTrue(eq.check_user_result(n1 - n2), eq.__str__() + " should be " + str(n1 - n2))
        print(">>> " + eq.get_hint_for_equation(eq))
        self.assertEqual(eq.get_hint_for_equation(eq), "17 - 9 = 17 - 7 - 2 = ")

    def test_subtract_12_8(self):
        # 12 - 8
        n1 = 12
        n2 = 8
        op = "-"
        eq = Equation(n1, op, n2)
        self.assertTrue(eq.check_user_result(n1 - n2), eq.__str__() + " should be " + str(n1 - n2))
        print(">>> " + eq.get_hint_for_equation(eq))
        self.assertEqual(eq.get_hint_for_equation(eq), "12 - 8 = 12 - 2 - 6 = ")

    def test_subtract_15_5(self):
        # 15 - 5
        n1 = 15
        n2 = 5
        op = "-"
        eq = Equation(n1, op, n2)
        self.assertTrue(eq.check_user_result(n1 - n2), eq.__str__() + " should be " + str(n1 - n2))
        print(">>> " + eq.get_hint_for_equation(eq))
        self.assertEqual(eq.get_hint_for_equation(eq), "15 - 5 = ")

    def test_subtract_27_7(self):
        # 27 - 7
        n1 = 27
        n2 = 7
        op = "-"
        eq = Equation(n1, op, n2)
        self.assertTrue(eq.check_user_result(n1 - n2), eq.__str__() + " should be " + str(n1 - n2))
        print(">>> " + eq.get_hint_for_equation(eq))
        self.assertEqual(eq.get_hint_for_equation(eq), "27 - 7 = ")

    def test_subtract_17_10(self):
        # 17 - 10
        n1 = 17
        n2 = 10
        op = "-"
        eq = Equation(n1, op, n2)
        self.assertTrue(eq.check_user_result(n1 - n2), eq.__str__() + " should be " + str(n1 - n2))
        print(">>> " + eq.get_hint_for_equation(eq))
        self.assertEqual(eq.get_hint_for_equation(eq), "17 - 10 = ")

    def test_subtract_30_10(self):
        # 30 - 10
        n1 = 30
        n2 = 10
        op = "-"
        eq = Equation(n1, op, n2)
        self.assertTrue(eq.check_user_result(n1 - n2), eq.__str__() + " should be " + str(n1 - n2))
        print(">>> " + eq.get_hint_for_equation(eq))
        self.assertEqual(eq.get_hint_for_equation(eq), "30 - 10 = ")

    def test_subtract_28_3(self):
        # 28 - 3
        n1 = 28
        n2 = 3
        op = "-"
        eq = Equation(n1, op, n2)
        self.assertTrue(eq.check_user_result(n1 - n2), eq.__str__() + " should be " + str(n1 - n2))
        print(">>> " + eq.get_hint_for_equation(eq))
        self.assertEqual(eq.get_hint_for_equation(eq), "28 - 3 = 20 + 8 - 3 = ")

    def test_subtract_67_39(self):
        # 67 - 39 = 67 - 7 - 32 = 60 - 32 =
        n1 = 67
        n2 = 39
        op = "-"
        eq = Equation(n1, op, n2)
        self.assertTrue(eq.check_user_result(n1 - n2), eq.__str__() + " should be " + str(n1 - n2))
        print(">>> " + eq.get_hint_for_equation(eq))
        self.assertEqual(eq.get_hint_for_equation(eq), "67 - 39 = 67 - 7 - 32 = ")

    def test_subtract_67_23(self):
        # 67 - 23 = 67 - 7 - 16 =
        n1 = 67
        n2 = 23
        op = "-"
        eq = Equation(n1, op, n2)
        self.assertTrue(eq.check_user_result(n1 - n2), eq.__str__() + " should be " + str(n1 - n2))
        print(">>> " + eq.get_hint_for_equation(eq))
        self.assertEqual(eq.get_hint_for_equation(eq), "67 - 23 = 67 - 7 - 16 = ")


class MultiplyingTest(unittest.TestCase):

    def test_multiply_0_10(self):
        # 0 * 10 =
        n1 = 0
        n2 = 10
        op = "*"
        eq = Equation(n1, op, n2)
        self.assertTrue(eq.check_user_result(n1 * n2), eq.__str__() + " should be " + str(n1 * n2))
        print(">>> " + eq.get_hint_for_equation(eq))
        self.assertEqual(eq.get_hint_for_equation(eq), "0 * 10 = ")

    def test_multiply_1_10(self):
        # 1 * 10 =
        n1 = 1
        n2 = 10
        op = "*"
        eq = Equation(n1, op, n2)
        self.assertTrue(eq.check_user_result(n1 * n2), eq.__str__() + " should be " + str(n1 * n2))
        print(">>> " + eq.get_hint_for_equation(eq))
        self.assertEqual(eq.get_hint_for_equation(eq), "1 * 10 = ")

    def test_multiply_3_10(self):
        # 3 * 10 = 10 + 10 + 10 =
        n1 = 3
        n2 = 10
        op = "*"
        eq = Equation(n1, op, n2)
        self.assertTrue(eq.check_user_result(n1 * n2), eq.__str__() + " should be " + str(n1 * n2))
        print(">>> " + eq.get_hint_for_equation(eq))
        self.assertEqual(eq.get_hint_for_equation(eq), "3 * 10 = 10 + 10 + 10 = ")

    def test_multiply_3_7(self):
        # 3 * 7 =
        n1 = 3
        n2 = 7
        op = "*"
        eq = Equation(n1, op, n2)
        self.assertTrue(eq.check_user_result(n1 * n2), eq.__str__() + " should be " + str(n1 * n2))
        print(">>> " + eq.get_hint_for_equation(eq))
        self.assertEqual(eq.get_hint_for_equation(eq), "3 * 7 = 7 + 7 + 7 = ")

    def test_multiply_8_6(self):
        # 8 * 6 =
        n1 = 8
        n2 = 6
        op = "*"
        eq = Equation(n1, op, n2)
        self.assertTrue(eq.check_user_result(n1 * n2), eq.__str__() + " should be " + str(n1 * n2))
        print(">>> " + eq.get_hint_for_equation(eq))
        self.assertEqual(eq.get_hint_for_equation(eq), "8 * 6 = 6 + 6 + 6 + 6 + 6 + 6 + 6 + 6 = ")