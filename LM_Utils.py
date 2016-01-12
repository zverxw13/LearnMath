import uuid
import time
from random import randint
import math
import operator
import wave
import contextlib
import logging


def my_random_string(string_length=10):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4()) # Convert UUID format to a Python string.
    random = random.upper() # Make all characters uppercase.
    random = random.replace("-","") # Remove the UUID '-'.
    return random[0:string_length] # Return the random string.


def sleep_in_sec(sec):
    time.sleep(sec)


def sleep_in_mili_sec(mili):
    time.sleep(float(mili/1000))


def checkCondition(a, oper, b):
    """
    Checks condition: a op b, where:
    a,b - number
    op - operator = [< | > | <= | >= | == | =]
    Return True if condition is met, False otherwise.
    :param a: number
    :param oper: operator = [< | > | <= | >= | == | =]
    :param b: number
    :return: True if condition is met
    """

    if type(a) is not int:
        a_n = int(a)
    else:
        a_n = a

    if type(b) is not int:
        b_n = int(b)
    else:
        b_n = b

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


def random_int_with_additional_condition(min, max, condition_operator, condition_value):
    """
    Generate and return random number N with base condition:  min <= N <= max
    and additional condition:  N [condition_operator]  [condition_value]

    Note: Both conditions (base and additional are reached!

    :param min: min range for generated N
    :param max: max range for generated N
    :param condition_operator: condition operator, can be: < | > | <= | >= | =
    :param condition_value: value for condition
    :return: generated N
    """

    condition_compare_result = False
    while not condition_compare_result:
        number = randint(min, max)
        condition_compare_result = checkCondition(number, condition_operator, condition_value)
        # print("......  ", number, " ", condition_operator, " ", condition_value, "  -->  ", condition_compare_result)

    return number


def get_wave_length(fname):
    with contextlib.closing(wave.open(fname,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
    print("\n", fname, " - duration: ", duration)
    return duration


def createLoggerForScreenAndFile(file_name, s_format=None):
    """
    Create and return a logger for screen and file with file_name.
    Format can be set with s_format.
    Usage: returned logger.critical, logger.error, logger.warning, logger.info, logger.debug
    :param file_name: log file name (with path)
    :param s_format: format for logger's formatter
    :return: logger
    """

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(filename)s:%(lineno)s - %(funcName)20s() - %(levelname)s - %('
                                  'message)s' if s_format is None else s_format)

    fh = logging.FileHandler(file_name)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger
    # logger.debug('This is a test log message.')


