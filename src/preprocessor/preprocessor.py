import os

from src.preprocessor.preprocessor_tool import PreprocessorTool
from src.lex.util import to_str


def start(c_code):
    """
    Starting preprocessing tools for input C code
    :param c_code: C code that need to be preprocessed
    :return: preprocessed C code
    """
    c_code = delete_comments(c_code)
    replacing = scan_for_define(c_code)
    for key, value in replacing.items():
        c_code = replace_all(c_code, key, value)
    c_code = parse_include_files(c_code)
    return c_code


def scan_for_define(c_code):
    """
    Scans for '#define' tokens and what string should be replaced in input C code
    :param c_code: C code in which scan is taking place
    :return: dictionary with following format: {what_should_be_replaced: on_what_should_be_replaced}
    """
    replacing = {}
    preprocessor_tool = PreprocessorTool(c_code)
    define_indexes = preprocessor_tool.find_all("#define ")
    for define_index in define_indexes:
        preprocessor_tool.set_iterator(define_index + 7)
        preprocessor_tool.skip()
        replace_what = ''
        current_char = preprocessor_tool.get_next_char()
        if current_char == '_EOF':
            return replacing
        while current_char != ' ' and current_char != '\n':
            replace_what += current_char
            current_char = preprocessor_tool.get_next_char()
            if current_char == '_EOF':
                return replacing
        preprocessor_tool.skip()
        replace_to = ''
        current_char = preprocessor_tool.get_next_char()
        if current_char == '_EOF':
            return replacing
        while current_char != ' ' and current_char != '\n':
            replace_to += current_char
            current_char = preprocessor_tool.get_next_char()
            if current_char == '_EOF':
                replacing[replace_what] = replace_to
                return replacing
        replacing[replace_what] = replace_to
    return replacing


def replace_all(c_code, replace_what, replace_to):
    """
    Replace all 'replace_what' entries with 'replace_to' (only where it is needed)
    :param c_code: C code in which replace is taking place
    :param replace_what: string that should be replaced
    :param replace_to: string that should be placed instead of 'replace_what'
    :return: C code (string)
    """
    preprocessor_tool = PreprocessorTool(c_code)
    define_string = '#define ' + replace_what + ' ' + replace_to
    preprocessor_tool.remove_first(define_string)
    preprocessor_tool.replace_all(replace_what, replace_to)
    return preprocessor_tool.c_code


def delete_comments(code):
    """
    Deletes all types of C comments in an input
    :param code: C code in which comments should be deleted
    :return: C code without comments
    """
    code = delete_oneline_comments(code)
    return delete_multiline_comments(code)


def delete_comments_universal(code, begin_str, end_str):
    """
    Deletes all substrings
    :param code: input string
    :param begin_str: beginning of the substring
    :param end_str: ending of the substring
    :return: string with deleted substrings
    """
    indexes = []
    current_index = code.find(begin_str, 0)
    while current_index != -1:
        next_end_index = code.find(end_str, current_index)
        if next_end_index == -1:
            indexes.append((current_index, len(code) - 1))
        else:
            indexes.append((current_index, next_end_index + len(end_str) - 1))
        current_index = code.find('//', next_end_index)
    return delete_from_string_indexes(code, indexes)


def delete_oneline_comments(code):
    """
    Deletes all C one line comments
    :param code: input C code
    :return: C code without one line comments
    """
    return delete_comments_universal(code, '//', '\n')


def delete_multiline_comments(code):
    """
    Deletes all C multi line comments
    :param code: input C code
    :return: C code without multi line comments
    """
    return delete_comments_universal(code, '/*', '*/')


def delete_from_string_indexes(code, indexes):
    """
    Removes everything in code between values in 'indexes'
    :param code: input code
    :param indexes: indices for removing
    :return: code without substrings defined by 'indexes'
    """
    if len(indexes) == 0:
        return code
    new_code = []
    curr_index = 0
    for i, (start, end) in enumerate(indexes):
        new_code.append(code[curr_index:start])
        curr_index = end + 1
        if i == len(indexes) - 1:
            new_code.append(code[curr_index:len(code)])
    return to_str(new_code)


def parse_include_files(input_code):
    """
    Parses '#include' entries
    :param input_code: input C code
    :return: C code with parsed '#include' statements
    """
    while input_code.find('#include') != -1:

        include_index = input_code.find('#include')
        begin_index = include_index + len('#include')

        if include_index == -1:
            return input_code

        while begin_index < len(input_code) and input_code[begin_index] == ' ':
            begin_index += 1

        if input_code[begin_index] != '"' and input_code[begin_index] != "<":
            raise Exception('After #include statement came {} symbol instead of dual quote symbol (") or "<" symbol.')
        elif input_code[begin_index] == '"':
            # search in directory
            end_index = input_code.find('"', begin_index + 1)
            file_name = input_code[begin_index + 1:end_index]
            with open('libs/' + file_name, "r") as file:
                file.seek(0)
                code = file.read()
                input_code = input_code[:include_index] + code + parse_include_files(input_code[end_index + 1:])

        elif input_code[begin_index] == '<':
            # search in /libs, because this is system library
            end_index = input_code.find('>', begin_index + 1)
            input_code = input_code[:end_index + 1] + parse_include_files(input_code[end_index + 1:])

    return input_code
