from src.lex.lexical_analyzer import *


def test_1_is_delimiter():
    assert is_delimiter('(') is True


def test_2_is_delimiter():
    assert is_delimiter('+') is False


def test_1_is_operator():
    assert is_operator('+') is True


def test_2_is_operator():
    assert is_operator('0') is False


def test_3_is_operator():
    assert is_operator(True) is False


def test_scan():
    in_c = 'int checkPrimeNumber(int n) \n\
            { \n\
                int j, flag = 1; \n\
                for(j=2; j <= n/2; ++j) \n\
                { \n\
                    if (n%j == 0) \n\
                    { \n\
                        flag =0; \n\
                         break; \n\
                    } \n\
                 } \n\
            return flag;\n\
            }'
    tokens = [('int', 65), ('checkPrimeNumber', 82), ('(', 39), ('int', 65), ('n', 82), (')', 40), ('{', 41), ('int', 65), ('j', 82), (',', 34), ('flag', 82), ('=', 7), ('1', 1), (';', 85), ('for', 62), ('(', 39), ('j', 82), ('=', 7), ('2', 1), (';', 85), ('j', 82), ('<=', 18), ('n', 82), ('/', 5), ('2', 1), (';', 85), ('++', 87), ('j', 82), (')', 40), ('{', 41), ('if', 64), ('(', 39), ('n', 82), ('%', 6), ('j', 82), ('==', 13), ('0', 1), (')', 40), ('{', 41), ('flag', 82), ('=', 7), ('0', 1), (';', 85), ('break', 50), (';', 85), ('}', 42), ('}', 42), ('return', 68), ('flag', 82), (';', 85), ('}', 42)]
    assert scan(in_c) == tokens


def test_1_next_token():
    in_c = 'int'
    output = ('int', 65)
    assert get_next_token(in_c) == output


def test_2_next_token():
    in_c = ''
    output = ('_EOF', 0)
    assert get_next_token(in_c) == output