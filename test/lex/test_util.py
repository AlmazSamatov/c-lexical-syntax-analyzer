from src.lex.util import *


def test_to_str():
    assert to_str(['777', 'is that the best c lexer?', 'True']) == '777is that the best c lexer?True'


def test_1_find_type():
    assert find_type(';') == 85


def test_2_find_type():
    assert find_type('-2sd;3') == -1


def test_3_find_type():
    assert find_type('+') == 2


def test_1_is_real_num():
    assert is_real_num('-3984.18223') is True


def test_2_is_real_num():
    assert is_real_num('-398418223') is True


def test_1_is_int():
    assert is_int('asdasd') is False


def test_2_is_int():
    assert is_int('-2323') is True


def test_3_is_int():
    assert is_int('-2323L') is True
