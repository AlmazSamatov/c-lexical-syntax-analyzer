from src.syntax.assignment_operator import int_codes as assignment_codes
from src.syntax.unary_operator import int_codes as unary_codes
from src.syntax.struct_or_union import int_codes as struct_or_union_codes

tokens = []
iterator = -1


def assignment_operator():
    global iterator
    if tokens[iterator][1] in assignment_codes:
        iterator += 1
        return tokens[iterator-1][0]


def unary_operator():
    global iterator
    if tokens[iterator][1] in unary_codes:
        iterator += 1
        return tokens[iterator-1][0]


def struct_or_union():
    global iterator
    if tokens[iterator][1] in struct_or_union_codes:
        iterator += 1
        return tokens[iterator - 1][0]