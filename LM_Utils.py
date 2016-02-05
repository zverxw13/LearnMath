"""
Module contains general methods used in LearnMath project
"""
import uuid
import time
from random import randint
import operator
import wave
import contextlib
import logging


def my_random_string(string_length=10):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4()) # Convert UUID format to a Python string.
    random = random.upper() # Make all characters uppercase.
    random = random.replace("-", "") # Remove the UUID '-'.
    return random[0:string_length] # Return the random string.


def sleep_in_sec(sec):
    """
    Sleeps for sec seconds
    :param sec: seconds to sleep
    :type sec: int
    """
    time.sleep(sec)


def sleep_in_mili_sec(mili):
    """
    Sleeps for mili miliseconds
    :param mili:  miliseconds to sleep (eg.: 1000 for 1 second)
    :type mili: int
    """
    time.sleep(float(mili/1000))


def check_condition(operand_a, oper, operand_b):
    """
    Checks condition:
    \t**operand_a op operand_b**

    where:
    \t\t*operand_a*, *operand_b* - numbers\n
    \t\t*op* - operator = [< | > | <= | >= | == | =]
    Returns True if condition is met, False otherwise.

    :param operand_a: number
    :type operand_a: int
    :param oper: operator = [< | > | <= | >= | == | =]
    :type oper: str
    :param operand_b: number
    :type operand_b: int
    :returns: True if condition is met, False otherwise.
    :raise Exception: when operator is not in [< | > | <= | >= | == | =]
    """

    if isinstance(operand_a, int):
    # if type(operand_a) is not int:
        a_n = int(operand_a)
    else:
        a_n = operand_a

    if isinstance(operand_b, int):
    # if type(operand_b) is not int:
        b_n = int(operand_b)
    else:
        b_n = operand_b

    if oper == "=" or  oper == "==":
        return operator.eq(a_n, b_n)
    elif oper == "<=":
        return operator.le(a_n, b_n)
    elif oper == "<":
        return operator.lt(a_n, b_n)
    elif oper == ">=":
        return operator.ge(a_n, b_n)
    elif oper == ">":
        return operator.gt(a_n, b_n)
    else:
        raise Exception("Not supported operator: " + oper)


def random_int_w_condition(min_val, max_val, condition_operator,
                           condition_value):
    """
    Generate and return random number N with base condition:  min_val <= N <= max_val
    and additional condition:  N [condition_operator]  [condition_value]

    Note: Both conditions (base and additional are reached!

    :param min_val: min_val range for generated N
    :param max_val: max_val range for generated N
    :param condition_operator: condition operator, can be: < | > | <= | >= | =
    :param condition_value: value for condition
    :return: generated N
    """

    condition_compare_result = False
    while not condition_compare_result:
        number = randint(min_val, max_val)
        condition_compare_result = check_condition(number,
                                                   condition_operator,
                                                   condition_value)
        # print("......  ", number, " ", condition_operator, " ",
        #       condition_value, "  -->  ", condition_compare_result)

    return number


def get_wave_length(wave_file_name):
    """
    Returns duration of wave given in param wave_file_name
    :param wave_file_name: wave file name (full path?)
    :type wave_file_name: str
    :return: wave duration (in ms?)
    """
    with contextlib.closing(wave.open(wave_file_name, 'r')) as f_wave:
        frames = f_wave.getnframes()
        rate = f_wave.getframerate()
        duration = frames / float(rate)
    print("\n", wave_file_name, " - duration: ", duration)
    return duration


def create_logger_for_screen_and_file(file_name, s_format=None):
    """
    Create and return a logger for screen and file with file_name.
    Format can be set with s_format.
    Usage: returned logger.critical, logger.error, logger.warning,
    logger.info, logger.debug
    :param file_name: log file name (with path)
    :param s_format: format for logger's formatter
    :return: logger
    """

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(filename)s:%(lineno)s'
                                  ' -%(funcName)20s() - %(levelname)s '
                                  '- %(message)s'
                                  if s_format is None else s_format)

    f_handler = logging.FileHandler(file_name)
    f_handler.setLevel(logging.DEBUG)
    f_handler.setFormatter(formatter)
    logger.addHandler(f_handler)

    s_handler = logging.StreamHandler()
    s_handler.setLevel(logging.DEBUG)
    s_handler.setFormatter(formatter)
    logger.addHandler(s_handler)

    return logger
