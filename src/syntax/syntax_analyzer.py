from src.syntax.assignment_operator import int_codes as assignment_codes
from src.syntax.unary_operator import int_codes as unary_codes
from src.syntax.struct_or_union import int_codes as struct_or_union_codes
from src.syntax.storage_class_specifier import int_codes as storage_class_specifier_codes
from src.syntax.type_specifier import int_codes as type_specifier_codes
from src.syntax.type_qualifier import int_codes as type_qualifier_codes
from src.syntax.tree import Tree

tokens = []
iterator = 0
tree = None


def translation_unit():
    """
    BNF rule for translation unit
    :return: AST
    """
    global iterator
    old_iterator = iterator
    node_value = external_declaration()
    if node_value is None:
        iterator = old_iterator
        return node_value
    while True:
        old_iterator = iterator
        temp = external_declaration()
        if temp is not None:
            node_value = Tree(node_value, temp)
        else:
            iterator = old_iterator
            break
    return node_value


def external_declaration():
    """
    BNF rule for external declaration
    :return: AST
    """
    global iterator
    old_iterator = iterator
    node_value = function_definition()
    if node_value is not None:
        return node_value
    else:
        iterator = old_iterator
    node_value = declaration()
    if node_value is not None:
        return node_value
    iterator = old_iterator
    return None


def function_definition():
    """
    BNF rule for function definition
    :return: AST
    """
    global iterator
    old_iterator = iterator
    left = declaration_specifier()
    temp_tree = None
    if left is not None:
        while True:
            old_iterator = iterator
            temp = declaration_specifier()
            if temp is not None:
                temp_tree = Tree(temp, temp_tree)
            else:
                iterator = old_iterator
                break
    left = Tree(left, temp_tree)
    iterator = old_iterator
    old_iterator = iterator
    node_value = declarator()
    if node_value is not None:
        old_iterator = iterator
        right = declaration()
        if right is not None:
            while True:
                old_iterator = iterator
                temp = declaration()
                if temp is not None:
                    right = Tree(right, temp)
                else:
                    iterator = old_iterator
                    break
        iterator = old_iterator
        node_value = Tree(node_value=node_value, right=right)
        old_iterator = iterator
        right = compound_statement()
        if right is not None:
            return Tree(left, node_value=node_value, right=right)
        iterator = old_iterator
        return None
    iterator = old_iterator
    return None


def declaration():
    """
    BNF rule for declaration
    :return: AST
    """
    global iterator
    old_iterator = iterator
    left = declaration_specifier()
    if left is not None:
        # while True:
        #     old_iterator = iterator
        #     temp = declaration_specifier()
        #     if temp is not None:
        #         left = Tree(left, temp)
        #     else:
        #
        #         break
        old_iterator = iterator
        node_value = init_declarator()
        if node_value is not None:
            counter = 0
            while True:
                counter += 1
                if counter > 5:
                    return None
                old_iterator = iterator
                temp = init_declarator()
                if temp is not None:
                    node_value = Tree(node_value, temp)
                else:
                    iterator = old_iterator
                    break
        iterator = old_iterator
        if tokens[iterator][1] == 85:
            iterator += 1
            right = tokens[iterator-1][0]
            return Tree(left, node_value, right)
    iterator = old_iterator
    return None


def init_declarator():
    """
    BNF rule for init declarator
    :return: AST
    """
    global iterator
    old_iterator = iterator
    if tokens[iterator-1][1] != 82:
        node_value = declarator()
    else:
        node_value = declarator(True)
    if node_value is not None:
        if tokens[iterator][1] == 7:
            iterator += 1
            old_iterator = iterator
            left = node_value
            node_value = tokens[iterator-1][0]
            right = initializer()
            if right is not None:
                return Tree(left, node_value, right)
            iterator = old_iterator
            return None
        return node_value
    iterator = old_iterator
    return None


def initializer():
    """
    BNF rule for initializer
    :return: AST
    """
    global iterator
    old_iterator = iterator
    node_value = assignment_expression()
    if node_value is not None:
        return node_value
    iterator = old_iterator
    if tokens[iterator][1] == 41:
        iterator += 1
        left = tokens[iterator-1][0]
        old_iterator = iterator
        node_value = initializer_list()
        if node_value is not None:
            if tokens[iterator][1] == 34:
                iterator += 1
                node_value = Tree(node_value, ',')
            if tokens[iterator][1] == 42:
                iterator += 1
                right = tokens[iterator-1][0]
                return Tree(left, node_value, right)
            return None
        iterator = old_iterator
        return None
    return None


def initializer_list():
    """
    BNF rule for initializer list
    :return: AST
    """
    global iterator
    old_iterator = iterator
    left = initializer()
    if left is not None:
        if tokens[iterator][1] == 34:
            iterator += 1
            node_value = tokens[iterator-1][0]
            old_iterator = iterator
            right = initializer_list()
            if right is None:
                iterator = old_iterator
            return Tree(left, node_value, right)
        return left
    iterator = old_iterator


def iteration_statement():
    """
    BNF rule for iteration_statement
    :return: AST
    """
    global iterator
    if tokens[iterator][1] == 79:
        iterator += 1
        left = tokens[iterator-1][0]
        if tokens[iterator][1] == 39:
            iterator += 1
            old_iterator = iterator
            node_value = expression()
            if node_value is not None:
                if tokens[iterator][1] == 40:
                    iterator += 1
                    node_value = Tree('(', node_value, ')')
                    old_iterator = iterator
                    right = statement()
                    if right is not None:
                        return Tree(left, node_value, right)
                    iterator = old_iterator
                    return None
            iterator = old_iterator
            return None
        return None
    if tokens[iterator][1] == 56:
        iterator += 1
        left = tokens[iterator-1][0]
        old_iterator = iterator
        node_value = statement()
        if node_value is not None:
            if tokens[iterator][1] == 79:
                iterator += 1
                if tokens[iterator][1] == 39:
                    iterator += 1
                    old_iterator = iterator
                    right = expression()
                    if right is not None:
                        if tokens[iterator][1] == 40:
                            iterator += 1
                            if tokens[iterator][1] == 85:
                                iterator += 1
                                right = Tree('while', Tree('(', right, ')'), ';')
                                return Tree(left, node_value, right)
                        return None
                    iterator = old_iterator
                    return None
                return None
            return None
        iterator = old_iterator
        return None
    if tokens[iterator][1] == 62:
        iterator += 1
        left = tokens[iterator-1][0]
        if tokens[iterator][1] == 39:
            iterator += 1
            old_iterator = iterator
            node_value = expression()
            if node_value is None:
                iterator = old_iterator
            if tokens[iterator][1] == 85:
                iterator += 1
                first_tree = Tree(node_value, ';')
                old_iterator = iterator
                node_value = expression()
                if node_value is None:
                    iterator = old_iterator
                if tokens[iterator][1] == 85:
                    iterator += 1
                    second_tree = Tree(node_value, ';')
                    old_iterator = iterator
                    node_value = expression()
                    if node_value is None:
                        iterator = old_iterator
                    if tokens[iterator][1] == 40:
                        iterator += 1
                        right = statement()
                        if right is not None:
                            node_value = Tree(first_tree, second_tree, node_value)
                            node_value = Tree('(', node_value, ')')
                            return Tree(left, node_value, right)
                        iterator = old_iterator
                        return None
                    return None
                return None
            return None
        return None
    return None


def statement():
    """
    BNF rule for statement
    :return: AST
    """
    global iterator
    old_iterator = iterator
    node_value = labeled_statement()
    if node_value is not None:
        return node_value
    iterator = old_iterator
    node_value = expression_statement()
    if node_value is not None:
        return node_value
    iterator = old_iterator
    node_value = compound_statement()
    if node_value is not None:
        return node_value
    iterator = old_iterator
    node_value = selection_statement()
    if node_value is not None:
        return node_value
    iterator = old_iterator
    node_value = iteration_statement()
    if node_value is not None:
        return node_value
    iterator = old_iterator
    node_value = jump_statement()
    if node_value is not None:
        return node_value

    return None


def labeled_statement():
    """
    BNF rule for labeled statement
    :return: AST
    """
    global iterator
    old_iterator = iterator
    left = identifier()
    if left is not None:
        if tokens[iterator][1] == 36:
            iterator += 1
            node_value = tokens[iterator-1][0]
            old_iterator = iterator
            right = statement()
            if right is not None:
                return Tree(left, node_value, right)
            iterator = old_iterator
            return None
        return None
    iterator = old_iterator
    return None


def expression_statement():
    """
    BNF rule for expression statement
    :return: AST
    """
    global iterator
    old_iterator = iterator
    node_value = expression()
    if tokens[iterator][1] == 85:
        iterator += 1
        right = tokens[iterator-1][0]
        return Tree(node_value=node_value, right=right)
    iterator = old_iterator
    return None


def compound_statement():
    """
    BNF rule for compound statement
    :return: AST
    """
    global iterator
    if tokens[iterator][1] == 41:
        iterator += 1
        left = tokens[iterator-1][0]
        old_iterator = iterator
        first_node_value = declaration()
        if first_node_value is not None:
            while True:
                old_iterator = iterator
                temp = declaration()
                if temp is not None:
                    first_node_value = Tree(first_node_value, temp)
                else:
                    break
        iterator = old_iterator
        old_iterator = iterator
        second_node_value = statement()
        if second_node_value is not None:
            while True:
                old_iterator = iterator
                temp = statement()
                if temp is not None:
                    second_node_value = Tree(second_node_value, temp)
                else:
                    break
        iterator = old_iterator
        node_value = Tree(first_node_value, second_node_value)
        if tokens[iterator][1] == 42:
            iterator += 1
            right = tokens[iterator-1][0]
            return Tree(left, node_value, right)
        return None
    return None


def selection_statement():
    """
    BNF rule for selection statement
    :return: AST
    """
    global iterator
    if tokens[iterator][1] == 64:
        iterator += 1
        left = tokens[iterator-1][0]
        if tokens[iterator][1] == 39:
            iterator += 1
            old_iterator = iterator
            node_value = expression()
            if node_value is not None:
                if tokens[iterator][1] == 40:
                    iterator += 1
                    node_value = Tree('(', node_value, ')')
                    old_iterator = iterator
                    right = statement()
                    if right is not None:
                        if tokens[iterator][1] == 58:
                            iterator += 1
                            more_right = tokens[iterator][0]
                            old_iterator = iterator
                            more_more_right = statement()
                            if more_more_right is not None:
                                right = Tree(right, more_right, more_more_right)
                                return Tree(left, node_value, right)
                            iterator = old_iterator
                            return None
                        return Tree(left, node_value, right)
                    iterator = old_iterator
                    return None
                return None
            iterator = old_iterator
            return None
        return None
    if tokens[iterator][1] == 73:
        iterator += 1
        left = tokens[iterator-1][0]
        if tokens[iterator][1] == 39:
            iterator += 1
            old_iterator = iterator
            node_value = expression()
            if node_value is not None:
                if tokens[iterator][1] == 40:
                    iterator += 1
                    node_value = Tree('(', node_value, ')')
                    old_iterator = iterator
                    right = statement()
                    if right is not None:
                        return Tree(left, node_value, right)
                    iterator = old_iterator
                    return None
                return None
            iterator = old_iterator
            return None
        return None
    return None


def jump_statement():
    """
    BNF rule for jump statement
    :return: AST
    """
    global iterator
    if tokens[iterator][1] == 63:
        iterator += 1
        left = tokens[iterator-1][0]
        old_iterator = iterator
        node_value = identifier()
        if node_value is not None:
            if tokens[iterator][1] == 85:
                iterator += 1
                right = tokens[iterator-1][0]
                return Tree(left, node_value, right)
            return None
        iterator = old_iterator
        return None
    if tokens[iterator][1] == 54:
        iterator += 1
        left = tokens[iterator-1][0]
        if tokens[iterator][1] == 85:
            iterator += 1
            node_value = tokens[iterator - 1][0]
            return Tree(left, node_value)
        return None
    if tokens[iterator][1] == 50:
        iterator += 1
        left = tokens[iterator-1][0]
        if tokens[iterator][1] == 85:
            iterator += 1
            node_value = tokens[iterator - 1][0]
            return Tree(left, node_value)
        return None
    if tokens[iterator][1] == 68:
        iterator += 1
        left = tokens[iterator-1][0]
        old_iterator = iterator
        node_value = expression()
        if node_value is None:
            iterator = old_iterator
        if tokens[iterator][1] == 85:
            iterator += 1
            right = tokens[iterator - 1][0]
            return Tree(left, node_value, right)
        return None


def expression():
    """
    BNF rule for expression
    :return: AST
    """
    global iterator
    old_iterator = iterator
    node_value = assignment_expression()
    if expression is not None:
        if tokens[iterator][1] == 34:
            iterator += 1
            left = node_value
            node_value = tokens[iterator-1][0]
            old_iterator = iterator
            right = expression()
            if right is None:
                iterator = old_iterator
            return Tree(left, node_value, right)
        return node_value
    iterator = old_iterator
    return None


def assignment_expression(node_return=False):
    """
    BNF rule for assignment expression
    :param node_return: force node return if true
    :return: AST
    """
    global iterator
    old_iterator = iterator
    node_value = conditional_expression()
    if (node_value is not None and node_return) or type(node_value) == Tree:
        return node_value
    iterator = old_iterator
    old_iterator = iterator
    node_value = unary_expression()
    if node_value is not None:
        left = node_value
        old_iterator = iterator
        node_value = assignment_operator()
        if node_value is not None:
            old_iterator = iterator
            right = assignment_expression(True)
            if right is not None:
                return Tree(left, node_value, right)
            iterator = old_iterator
        iterator = old_iterator
        if left is not None:
            return left
    iterator = old_iterator
    return None


def conditional_expression():
    """
    BNF rule for conditional expression
    :return: AST
    """
    global iterator
    old_iterator = iterator
    node_value = logical_or_expression()
    if node_value is not None:
        if tokens[iterator][1] == 35:
            iterator += 1
        return node_value
    iterator = old_iterator
    return None


def logical_or_expression():
    """
    BNF rule for logical or expression
    :return: AST
    """
    global iterator
    old_iterator = iterator
    node_value = logical_and_expression()
    if node_value is not None:
        if tokens[iterator][1] == 20:
            iterator += 1
            left = node_value
            node_value = tokens[iterator-1][0]
            old_iterator = iterator
            right = logical_or_expression()
            if right is None:
                iterator = old_iterator
            return Tree(left, node_value, right)
        return node_value
    iterator = old_iterator


def logical_and_expression():
    """
    BNF rule for logical and expression
    :return: AST
    """
    global iterator
    old_iterator = iterator
    node_value = inclusive_or_expression()
    if node_value is not None:
        if tokens[iterator][1] == 19:
            iterator += 1
            left = node_value
            node_value = tokens[iterator - 1][0]
            old_iterator = iterator
            right = logical_and_expression()
            if right is None:
                iterator = old_iterator
            return Tree(left, node_value, right)
        return node_value
    iterator = old_iterator


def inclusive_or_expression():
    """
    BNF rule for inclusive or expression
    :return: AST
    """
    global iterator
    old_iterator = iterator
    node_value = exclusive_or_expression()
    if node_value is not None:
        if tokens[iterator][1] == 23:
            iterator += 1
            left = node_value
            node_value = tokens[iterator - 1][0]
            old_iterator = iterator
            right = inclusive_or_expression()
            if right is None:
                iterator = old_iterator
            return Tree(left, node_value, right)
        return node_value
    iterator = old_iterator


def exclusive_or_expression():
    """
    BNF rule for exclusive or expression
    :return: AST
    """
    global iterator
    old_iterator = iterator
    node_value = and_expression()
    if node_value is not None:
        if tokens[iterator][1] == 24:
            iterator += 1
            left = node_value
            node_value = tokens[iterator - 1][0]
            old_iterator = iterator
            right = exclusive_or_expression()
            if right is None:
                iterator = old_iterator
            return Tree(left, node_value, right)
        return node_value
    iterator = old_iterator


def and_expression():
    """
    BNF rule for and expression
    :return: AST
    """
    global iterator
    old_iterator = iterator
    node_value = equality_expression()
    if node_value is not None:
        if tokens[iterator][1] == 22:
            iterator += 1
            left = node_value
            node_value = tokens[iterator - 1][0]
            old_iterator = iterator
            right = and_expression()
            if right is None:
                iterator = old_iterator
            return Tree(left, node_value, right)
        return node_value
    iterator = old_iterator


def equality_expression():
    """
    BNF rule for equality expression
    :return: AST
    """
    global iterator
    old_iterator = iterator
    node_value = relational_expression()
    if node_value is not None:
        if tokens[iterator][1] in [13, 16]:
            iterator += 1
            left = node_value
            node_value = tokens[iterator - 1][0]
            old_iterator = iterator
            right = equality_expression()
            if right is None:
                iterator = old_iterator
            return Tree(left, node_value, right)
        return node_value
    iterator = old_iterator


def relational_expression():
    """
    BNF rule for relational expression
    :return: AST
    """
    global iterator
    old_iterator = iterator
    node_value = shift_expression()
    if node_value is not None:
        if tokens[iterator][1] in [14, 15, 18, 17]:
            iterator += 1
            left = node_value
            node_value = tokens[iterator - 1][0]
            old_iterator = iterator
            right = relational_expression()
            if right is None:
                iterator = old_iterator
            return Tree(left, node_value, right)
        return node_value
    iterator = old_iterator


def shift_expression():
    """
    BNF rule for shift expression
    :return: AST
    """
    global iterator
    old_iterator = iterator
    node_value = additive_expression()
    if node_value is not None:
        if tokens[iterator][1] in [26, 27]:
            iterator += 1
            left = node_value
            node_value = tokens[iterator - 1][0]
            old_iterator = iterator
            right = shift_expression()
            if right is None:
                iterator = old_iterator
            return Tree(left, node_value, right)
        return node_value
    iterator = old_iterator


def additive_expression():
    """
    BNF rule for additive expression
    :return: AST
    """
    global iterator
    old_iterator = iterator
    node_value = multiplicative_expression()
    if node_value is not None:
        if tokens[iterator][1] in [2, 3]:
            iterator += 1
            left = node_value
            node_value = tokens[iterator - 1][0]
            old_iterator = iterator
            right = additive_expression()
            if right is None:
                iterator = old_iterator
            return Tree(left, node_value, right)
        return node_value
    iterator = old_iterator


def multiplicative_expression():
    """
    BNF rule for multiplicative expression
    :return: AST
    """
    global iterator
    old_iterator = iterator
    node_value = cast_expression()
    if node_value is not None:
        if tokens[iterator][1] in [4, 5, 6]:
            iterator += 1
            left = node_value
            node_value = tokens[iterator - 1][0]
            old_iterator = iterator
            right = multiplicative_expression()
            if right is None:
                iterator = old_iterator
            return Tree(left, node_value, right)
        return node_value
    iterator = old_iterator


def cast_expression():
    """
    BNF rule for cast expression
    :return: AST
    """
    global iterator
    old_iterator = iterator
    node_value = unary_expression()
    if node_value is not None:
        return node_value
    iterator = old_iterator
    if tokens[iterator][1] == 39:
        iterator += 1
        left = tokens[iterator - 1][0]
        old_iterator = iterator
        node_value = type_name()
        if node_value is not None:
            if tokens[iterator][1] == 40:
                iterator += 1
                right = tokens[iterator - 1][0]
                left = Tree(left, node_value, right)
                old_iterator = iterator
                node_value = cast_expression()
                if node_value is not None:
                    return Tree(left, node_value)
                iterator = old_iterator
        iterator = old_iterator
        return None
    return None


def unary_expression():
    """
    BNF rule for unary expression
    :return: AST
    """
    global iterator
    old_iterator = iterator
    node_value = postfix_expression()
    if node_value is not None:
        return node_value
    iterator = old_iterator
    if tokens[iterator][1] in [87, 88]:
        iterator += 1
        left = tokens[iterator-1][0]
        old_iterator = iterator
        node_value = unary_expression()
        if node_value is not None:
            return Tree(left, node_value)
        iterator = old_iterator
        return None
    old_iterator = iterator
    left = unary_operator()
    if left is not None:
        old_iterator = iterator
        node_value = cast_expression()
        if node_value is not None:
            return Tree(left, node_value)
        iterator = old_iterator
        return None
    iterator = old_iterator
    if tokens[iterator][1] == 28:
        iterator += 1
        left = tokens[iterator - 1][0]
        old_iterator = iterator
        node_value = unary_expression()
        if node_value is not None:
            return Tree(left, node_value)
        iterator = old_iterator
        old_iterator = iterator
        node_value = type_name()
        if node_value is not None:
            return Tree(left, node_value)
        iterator = old_iterator
    return None


# todo something with '.' and '->'
def postfix_expression():
    """
    BNF rule for postfix expression
    :return: AST
    """
    global iterator
    old_iterator = iterator
    node_value = primary_expression()
    if node_value is not None:
        if tokens[iterator][1] == 37:
            iterator += 1
            old_iterator = iterator
            node_value = expression()
            if node_value is not None:
                if tokens[iterator][1] == 38:
                    iterator += 1
                    right = Tree('[', node_value, ']')
                    old_iterator = iterator
                    left = postfix_expression()
                    if left is None:
                        iterator = old_iterator
                    return Tree(left, node_value, right)
                return None
            iterator = old_iterator
            return None
        if tokens[iterator][1] == 39:
            iterator += 1
            left = node_value
            old_iterator = iterator
            node_value = expression()
            if node_value is not None:
                while True:
                    old_iterator = iterator
                    temp = expression()
                    if temp is not None:
                        node_value = Tree(left, node_value, temp)
                    else:
                        iterator = old_iterator
                        break
                if tokens[iterator][1] == 40:
                    iterator += 1
                    right = Tree('(', node_value, ')')
                    old_iterator = iterator
                    left = postfix_expression()
                    if left is None:
                        iterator = old_iterator
                    return Tree(left, node_value, right)
                return None
            iterator = old_iterator
            return None
        if tokens[iterator][1] in [87, 88]:
            iterator += 1
            right = tokens[iterator-1][0]
            old_iterator = iterator
            left = postfix_expression()
            if left is None:
                iterator = old_iterator
            return Tree(left, node_value, right)
        return node_value
    iterator = old_iterator


def primary_expression():
    """
    BNF rule for primary expression
    :return: AST
    """
    global iterator
    old_iterator = iterator
    node_value = identifier()
    if node_value is not None:
        return node_value
    iterator = old_iterator
    old_iterator = iterator
    node_value = constant()
    if node_value is not None:
        return node_value
    iterator = old_iterator
    if tokens[iterator][1] == 84:
        iterator += 1
        node_value = tokens[iterator-1][0]
        return node_value
    if tokens[iterator][1] == 39:
        iterator += 1
        left = tokens[iterator - 1][0]
        old_iterator = iterator
        node_value = expression()
        if node_value is not None:
            if tokens[iterator][1] == 40:
                iterator += 1
                right = tokens[iterator - 1][0]
                return Tree(left, node_value, right)
            return None
        iterator = old_iterator
        return None


def assignment_operator():
    """
    BNF rule for assignment operator
    :return: operator
    """
    global iterator
    if tokens[iterator][1] in assignment_codes:
        iterator += 1
        return tokens[iterator-1][0]
    return None


def unary_operator():
    """
    BNF rule for external declaration
    :return: operator
    """
    global iterator
    if tokens[iterator][1] in unary_codes:
        iterator += 1
        return tokens[iterator-1][0]
    return None


def type_name():
    """
    BNF rule for type name
    :return: AST
    """
    global iterator
    old_iterator = iterator
    node_value = specifier_qualifier()
    if node_value is not None:
        left = node_value
        while True:
            old_iterator = iterator
            node_value = specifier_qualifier()
            if node_value is None:
                iterator = old_iterator
                break
            left = Tree(left, node_value)
        old_iterator = iterator
        node_value = abstract_declarator()
        if node_value is not None:
            return Tree(left, node_value)
        iterator = old_iterator
    iterator = old_iterator
    return None


def specifier_qualifier():
    """
    BNF rule for specifier qualifier
    :return: AST
    """
    global iterator
    old_iterator = iterator
    node_value = type_specifier()
    if node_value is not None:
        return node_value
    iterator = old_iterator
    old_iterator = iterator
    node_value = type_qualifier()
    if node_value is not None:
        return node_value
    iterator = old_iterator
    return None


def type_specifier():
    """
    BNF rule for type specifier
    :return: AST
    """
    global iterator
    if tokens[iterator][1] in type_specifier_codes:
        iterator += 1
        return tokens[iterator-1][0]
    old_iterator = iterator
    node_value = struct_or_union_specifier()
    if node_value is not None:
        return node_value
    iterator = old_iterator
    old_iterator = iterator
    node_value = enum_specifier()
    if node_value is not None:
        return node_value
    iterator = old_iterator
    old_iterator = iterator
    node_value = typedef_name()
    if node_value is not None:
        return node_value
    iterator = old_iterator
    return None


def struct_or_union_specifier():
    """
    BNF rule for struct or union specifier
    :return: AST
    """
    global iterator
    old_iterator = iterator
    left = struct_or_union()
    if left is not None:
        old_iterator = iterator
        node_value = identifier()
        if node_value is not None:
            if tokens[iterator][1] == 41:
                iterator += 1
                old_iterator = iterator
                right = struct_declaration()
                if right is not None:
                    while True:
                        old_iterator = iterator
                        temp = struct_declaration()
                        if temp is not None:
                            right = Tree(None, right, temp)
                        else:
                            iterator = old_iterator
                            break
                    if tokens[iterator][1] in struct_or_union_codes:
                        iterator += 1
                        return Tree(left, node_value, Tree('{', right, '}'))
                    return None
                iterator = old_iterator
                return None
            return Tree(left, node_value)
        iterator = old_iterator
        if tokens[iterator][1] == 41:
            iterator += 1
            old_iterator = iterator
            right = struct_declaration()
            if right is not None:
                while True:
                    old_iterator = iterator
                    temp = struct_declaration()
                    if temp is not None:
                        right = Tree(None, right, temp)
                    else:
                        iterator = old_iterator
                        break
                if tokens[iterator][1] in struct_or_union_codes:
                    iterator += 1
                    return Tree(left, node_value, Tree('{', right, '}'))
                return None
            iterator = old_iterator
            return None
    iterator = old_iterator
    return None


def struct_declaration():
    """
    BNF rule for struct declaration
    :return: AST
    """
    global iterator
    old_iterator = iterator
    left = specifier_qualifier()
    if left is not None:
        while True:
            old_iterator = iterator
            temp = specifier_qualifier()
            if temp is not None:
                left = Tree(left, temp)
            else:
                iterator = old_iterator
                break
    iterator = old_iterator
    old_iterator = iterator
    node_value = struct_declarator_list()
    if node_value is not None:
        return Tree(left, node_value)
    iterator = old_iterator
    return None


def struct_declarator_list():
    """
    BNF rule for struct declaration list
    :return: AST
    """
    global iterator
    old_iterator = iterator
    node_value = struct_declarator()
    if node_value is not None:
        if tokens[iterator][1] == 34:
            iterator += 1
            left = node_value
            node_value = tokens[iterator - 1][0]
            old_iterator = iterator
            right = struct_declarator_list()
            if right is None:
                iterator = old_iterator
            return Tree(left, node_value, right)
        return node_value
    iterator = old_iterator


def struct_declarator():
    """
    BNF rule for struct declarator
    :return: AST
    """
    global iterator
    old_iterator = iterator
    node_value = declarator()
    if node_value is not None:
        if tokens[iterator][1] in struct_or_union_codes:
            iterator += 1
            left = node_value
            node_value = tokens[iterator-1][0]
            old_iterator = iterator
            right = constant_expression()
            if right is not None:
                return Tree(left, node_value, right)
            iterator = old_iterator
            return None
        else:
            return node_value
    iterator = old_iterator


def declarator(decrease_iterator=False):
    """
    BNF rule for declarator
    :param decrease_iterator: force decrease iterator
    :return: AST
    """
    global iterator
    if decrease_iterator:
        iterator -= 1
    old_iterator = iterator
    left = pointer()
    if left is None:
        iterator = old_iterator
    old_iterator = iterator
    node_value = direct_declarator()
    if node_value is not None:
        return Tree(left, node_value)
    else:
        iterator = old_iterator
        return None


def direct_declarator():
    """
    BNF rule for direct declarator
    :return: AST
    """
    global iterator
    old_iterator = iterator
    node_value = identifier()
    if node_value is not None:
        return node_value
    iterator = old_iterator
    if tokens[iterator][1] == 39:
        iterator += 1
        left = tokens[iterator-1][0]
        old_iterator = iterator
        node_value = declarator()
        if node_value is not None:
            if tokens[iterator][1] == 40:
                iterator += 1
                right = tokens[iterator - 1][0]
                return Tree(left, node_value, right)
            return None
        iterator = old_iterator
        node_value = parameter_type_list()
        if node_value is not None:
            if tokens[iterator][1] == 40:
                iterator += 1
                node_value = Tree('(', node_value, ')')
                old_iterator = iterator
                left = direct_declarator()
                if left is None:
                    iterator = old_iterator
                return Tree(left, node_value)
            return None
        iterator = old_iterator
        old_iterator = iterator
        node_value = identifier()
        if node_value is not None:
            while True:
                old_iterator = iterator
                temp = identifier()
                if temp is not None:
                    node_value = Tree(node_value, temp)
                else:
                    iterator = old_iterator
                    break
        else:
            iterator = old_iterator
        if tokens[iterator][1] == 40:
            iterator += 1
            node_value = Tree('(', node_value, ')')
            old_iterator = iterator
            left = direct_declarator()
            if left is None:
                iterator = old_iterator
            return Tree(left, node_value)
    if tokens[iterator][1] == 37:
        iterator += 1
        old_iterator = iterator
        node_value = constant_expression()
        if node_value is None:
            iterator = old_iterator
        if tokens[iterator][1] == 38:
            iterator += 1
            node_value = Tree('[', node_value, ']')
            old_iterator = iterator
            left = direct_declarator()
            if left is None:
                iterator = old_iterator
            return Tree(left, node_value)
        return None
    return None


def constant_expression():
    """
    BNF rule for constant expression
    :return: AST
    """
    global iterator
    old_iterator = iterator
    node_value = conditional_expression()
    if node_value is not None:
        return node_value
    iterator = old_iterator
    return None


def pointer():
    """
    BNF rule for pointer
    :return: AST
    """
    global iterator
    if tokens[iterator][1] == 4:
        iterator += 1
        left = tokens[iterator-1][0]
        old_iterator = iterator
        node_value = type_qualifier()
        if node_value is not None:
            while True:
                old_iterator = iterator
                temp = type_qualifier()
                if temp is None:
                    iterator = old_iterator
                    break
                node_value = Tree(node_value, temp)
        else:
            iterator = old_iterator
        old_iterator = iterator
        right = pointer()
        if right is None:
            iterator = old_iterator
        return Tree(left, node_value, right)
    return None


def parameter_type_list():
    """
    BNF rule for parameter type list
    :return: AST
    """
    global iterator
    old_iterator = iterator
    node_value = parameter_list()
    if node_value is not None:
        if tokens[iterator][1] == 34:
            left = node_value
            iterator += 1
            old_iterator = iterator
            right = parameter_type_list()
            if right is None:
                iterator = old_iterator
            node_value = Tree(left, ',', right)
        return node_value
    iterator = old_iterator


def parameter_list():
    """
    BNF rule for parameter list
    :return: AST
    """
    global iterator
    old_iterator = iterator
    node_value = parameter_declaration()
    if node_value is not None:
        if tokens[iterator][1] == 34:
            iterator += 1
            left = node_value
            node_value = tokens[iterator - 1][0]
            old_iterator = iterator
            right = parameter_list()
            if right is None:
                iterator = old_iterator
            return Tree(left, node_value, right)
        return node_value
    iterator = old_iterator


def parameter_declaration():
    """
    BNF rule for parameter declaration
    :return: AST
    """
    global iterator
    old_iterator = iterator
    left = declaration_specifier()
    if left is not None:
        while True:
            old_iterator = iterator
            temp = declaration_specifier()
            if temp is not None:
                left = Tree(left, temp)
            else:
                iterator = old_iterator
                break
        old_iterator = iterator
        node_value = declarator()
        if node_value is not None:
            return Tree(left, node_value)
        iterator = old_iterator
        old_iterator = iterator
        node_value = abstract_declarator()
        if node_value is not None:
            return Tree(left, node_value)
        iterator = old_iterator
        return left
    iterator = old_iterator
    return None


def declaration_specifier():
    """
    BNF rule for declaration specifier
    :return: AST
    """
    global iterator
    old_iterator = iterator
    node_value = storage_class_specifier()
    if node_value is not None:
        return node_value
    iterator = old_iterator
    old_iterator = iterator
    node_value = type_specifier()
    if node_value is not None:
        return node_value
    iterator = old_iterator
    old_iterator = iterator
    node_value = type_qualifier()
    if node_value is not None:
        return node_value
    iterator = old_iterator
    return None


def abstract_declarator():
    """
    BNF rule for abstract declarator
    :return: AST
    """
    global iterator
    old_iterator = iterator
    left = pointer()
    if left is not None:
        old_iterator = iterator
        node_value = direct_abstract_declarator()
        if node_value is not None:
            return Tree(left, node_value)
        iterator = old_iterator
        return left
    iterator = old_iterator
    old_iterator = iterator
    node_value = direct_abstract_declarator()
    if node_value is not None:
        return node_value
    iterator = old_iterator


def direct_abstract_declarator():
    """
    BNF rule for direct abstract declarator
    :return: AST
    """
    global iterator
    if tokens[iterator][1] == 39:
        iterator += 1
        left = tokens[iterator-1][0]
        old_iterator = iterator
        node_value = abstract_declarator()
        if node_value is not None:
            if tokens[iterator][1] == 40:
                iterator += 1
                right = tokens[iterator - 1][0]
                if tokens[iterator][1] == 37:
                    left = Tree(left, node_value, right)
                    iterator += 1
                    old_iterator = iterator
                    node_value = constant_expression()
                    if node_value is None:
                        iterator = old_iterator
                    if tokens[iterator][1] == 38:
                        iterator += 1
                        return Tree(left, Tree('[', node_value, ']'))
                    return None
                if tokens[iterator][1] == 39:
                    iterator += 1
                    old_iterator = iterator
                    node_value = parameter_type_list()
                    if node_value is None:
                        iterator = old_iterator
                    if tokens[iterator][1] == 40:
                        iterator += 1
                        return Tree(left, Tree('(', node_value, ')'))
                    return None
                return Tree(left, node_value, right)
            return None
        iterator = old_iterator
        return None
    return None


def enum_specifier():
    """
    BNF rule for enum specifier
    :return: AST
    """
    global iterator
    if tokens[iterator][1] == 59:
        iterator += 1
        left = tokens[iterator - 1][0]
        old_iterator = iterator
        node_value = identifier()
        if node_value is not None:
            if tokens[iterator][1] == 41:
                iterator += 1
                old_iterator = iterator
                right = enumerator_list()
                if right is not None:
                    if tokens[iterator][1] == 42:
                        iterator += 1
                        return Tree(left, node_value, Tree('{', right, '}'))
                    return None
                iterator = old_iterator
                return None
            return Tree(left, node_value)
        iterator = old_iterator
    return None


def enumerator_list():
    """
    BNF rule for enumerator list
    :return: AST
    """
    global iterator
    old_iterator = iterator
    node_value = enumerator()
    if node_value is not None:
        if tokens[iterator][1] == 34:
            iterator += 1
            left = node_value
            node_value = tokens[iterator - 1][0]
            old_iterator = iterator
            right = enumerator_list()
            if right is None:
                iterator = old_iterator
            return Tree(left, node_value, right)
        return node_value
    iterator = old_iterator


def enumerator():
    """
    BNF rule for enumerator
    :return: AST
    """
    global iterator
    old_iterator = iterator
    node_value = identifier()
    if node_value is not None:
        if tokens[iterator][1] == 7:
            iterator += 1
            left = node_value
            node_value = tokens[iterator-1][0]
            old_iterator = iterator
            right = constant_expression()
            if right is not None:
                return Tree(left, node_value, right)
            iterator = old_iterator
            return None
    iterator = old_iterator
    return None


def typedef_name():
    """
    BNF rule for typedef name
    :return: AST
    """
    global iterator
    old_iterator = iterator
    node_value = identifier()
    if node_value is not None:
        return node_value
    iterator = old_iterator
    return None


def type_qualifier():
    """
    BNF rule for type qualifier
    :return: type qualifier
    """
    global iterator
    if tokens[iterator][1] in type_qualifier_codes:
        iterator += 1
        return tokens[iterator - 1][0]
    return None


def struct_or_union():
    """
    BNF rule for struct or union
    :return: struct or union
    """
    global iterator
    if tokens[iterator][1] in struct_or_union_codes:
        iterator += 1
        return tokens[iterator-1][0]
    return None


def storage_class_specifier():
    """
    BNF rule for class specifier
    :return: class specifier
    """
    global iterator
    if tokens[iterator][1] in storage_class_specifier_codes:
        iterator += 1
        return tokens[iterator-1][0]
    return None


def identifier():
    """
    BNF rule for identifier
    :return: identifier
    """
    global iterator
    if tokens[iterator][1] == 82:
        iterator += 1
        return tokens[iterator-1][0]
    return None


def integer_constant():
    """
    BNF rule for integer constant
    :return: integer constant
    """
    global iterator
    if tokens[iterator][1] == 1:
        iterator += 1
        return tokens[iterator-1][0]
    return None


def character_constant():
    """
    BNF rule for character_constant
    :return: character constant
    """
    global iterator
    if tokens[iterator][1] == 83:
        iterator += 1
        return tokens[iterator-1][0]
    return None


def floating_constant():
    """
    BNF rule for floating constant
    :return: type qualifier
    """
    global iterator
    if tokens[iterator][1] == 81:
        iterator += 1
        return tokens[iterator-1][0]
    return None


def constant():
    """
    BNF rule for constant
    :return: constant
    """
    global iterator
    old_iterator = iterator
    constant = integer_constant()
    if constant is not None:
        return constant
    iterator = old_iterator
    old_iterator = iterator
    constant = character_constant()
    if constant is not None:
        return constant
    iterator = old_iterator
    old_iterator = iterator
    constant = floating_constant()
    if constant is not None:
        return constant
    iterator = old_iterator
    return None


def generate_syntax_tree(input_tokens):
    """
    Starting parser and generating tree
    :param input_tokens: tokens to generate tree from
    :return: AST
    """
    global tokens
    tokens = input_tokens
    tree = translation_unit()
    return tree
