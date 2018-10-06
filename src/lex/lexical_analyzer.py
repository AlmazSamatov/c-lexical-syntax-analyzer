from src.lex.util import to_str, find_type, is_delimiter, is_operator
from src.lex.general_tokens import _STRING, _CHAR
from src.lex.util import to_str, find_type, is_delimiter, is_operator
import src.lex.general_tokens

token_it = -1
tokens = []


def get_next_token(input_code):
    """
    Returns next token
    :param input_code: input C code
    :return: next token by iterator or _EOF if end of file
    """
    global token_it
    if token_it == -1:
        scan(input_code)
    token_it += 1
    if token_it >= len(tokens):
        eof_token = ('_EOF', src.lex.general_tokens._EOF)
        return eof_token
    return tokens[token_it]


def scan(input_code):
    """
    Scans input C code for tokens and returns list of tuples with tokens
    :param input_code: C code that need to be scanned
    :return: Tuple with tokens of following format: ('token', integer_representation)
    """
    global tokens
    tokens = []
    current_index = 0
    char_list = []

    while len(char_list) > 0 or current_index < len(input_code):
        operator_lexeme = ''

        if current_index < len(input_code):
            # if we can get access to current index element of input code
            if input_code[current_index] == '\n':
                current_index += 1
                continue
            quotes = [('"', _STRING), ("'", _CHAR)]
            for quote in quotes:
                # we find string or char literal here
                if input_code[current_index] == quote[0]:
                    end_index_of_literal = input_code.find(quote[0], current_index + 1)
                    if end_index_of_literal != -1:
                        tokens.append((input_code[current_index:end_index_of_literal + 1], quote[1]))
                        current_index = end_index_of_literal + 1
                        continue

        if current_index + 2 < len(input_code) and is_operator(input_code[current_index: current_index + 3]):
            # if we have operators as <<= etc.
            operator_lexeme = input_code[current_index: current_index + 3]
            # increment current index to operator length
            current_index += 3

        elif current_index + 1 < len(input_code) and is_operator(input_code[current_index: current_index + 2]):
            # if we have operators as ++, --, -> etc.
            operator_lexeme = input_code[current_index: current_index + 2]
            # increment current index to operator length
            current_index += 2

        elif current_index < len(input_code) and is_operator(input_code[current_index]):
            # if we have operators as +, -, {, } etc.
            operator_lexeme = input_code[current_index]
            # increment current index to operator length
            current_index += 1

        elif current_index < len(input_code) and not is_delimiter(input_code[current_index]):
            char_list.append(input_code[current_index])
            current_index += 1
        else:

            if len(char_list) > 0:
                current_lexeme = to_str(char_list)
                tokens.append((current_lexeme, find_type(current_lexeme)))
                char_list.clear()

            # add to tokens delimiter except whitespace
            if current_index < len(input_code) and input_code[current_index] != ' ':
                tokens.append((input_code[current_index], find_type(input_code[current_index])))

            current_index += 1

        # when we are go out of input code, but still have lexemes in char_list
        if current_index >= len(input_code) and len(char_list) > 0:
            current_lexeme = to_str(char_list)
            tokens.append((current_lexeme, find_type(current_lexeme)))
            char_list.clear()

        # if we found operator then initially put into the list our lexeme that ends in this index and after put operator
        if len(char_list) > 0 and len(operator_lexeme) > 0:
            # put some lexeme before operator
            current_lexeme = to_str(char_list)
            tokens.append((current_lexeme, find_type(current_lexeme)))
            char_list.clear()

            # put operator after lexeme
            tokens.append((operator_lexeme, find_type(operator_lexeme)))
        elif len(operator_lexeme) > 0:
            # if there are nothing in char_list then just put operator
            tokens.append((operator_lexeme, find_type(operator_lexeme)))

    return tokens
