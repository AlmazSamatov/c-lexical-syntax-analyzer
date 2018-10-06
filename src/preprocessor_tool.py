import re
from src.operators import _dictionary as op_dict
from src.delimiters import _dictionary as del_dict


class PreprocessorTool:
    """
    Tool that helps preprocessor to handle C code
    """
    iterator = -1
    c_code = ''

    def __init__(self, c_code):
        self.c_code = c_code

    def find(self, string):
        """
        Finding first entry of a string in the C code
        :param string: input string
        :return: index of the input string in C code
        """
        return self.c_code.find(string)

    def find_all(self, string):
        """
        Finding all entries of a string and returns it as a list
        :param string: input string
        :return: all indices of the input string in C code as a list
        """
        return [m.start() for m in re.finditer(string, self.c_code)]

    def set_iterator(self, iterator):
        """
        Set iterator of a preprocessor tool
        :param iterator: value of the iterator
        """
        if type(iterator) is int:
            self.iterator = iterator

    def get_next_char(self):
        """
        Moving iterator and getting new char
        :return: char at the iterator
        """
        self.iterator += 1
        if self.iterator == len(self.c_code):
            return '_EOF'
        return self.c_code[self.iterator]

    def remove_first(self, string):
        """
        Removes first entry of the input string in C code
        :param string: input string
        """
        self.c_code = self.c_code.replace(string, '', 1)

    def replace_all(self, replace_what, replace_to):
        """
        Replaces, where necessary, 'replace_what' with 'replace_to'
        :param replace_what: string that need to be replaced
        :param replace_to: replaces 'replace_what'
        """
        all_d_quotes = self.find_all('"')
        all_replace_what = self.find_all(replace_what)
        while not len(all_replace_what) == 0:
            skip = False
            for i in range(0, len(all_d_quotes), 2):
                if all_replace_what[0] > all_d_quotes[i] and all_replace_what[0] < all_d_quotes[i+1]:
                    skip = True
                    all_replace_what.remove(all_replace_what[0])
            if all_replace_what[0] - 1 > -1 and (self.c_code[all_replace_what[0]-1] != ' ' and
                                                 self.c_code[all_replace_what[0]-1] != '\n' and
                                                 not self.c_code[all_replace_what[0]-1] in op_dict and
                                                 not self.c_code[all_replace_what[0]-1] in del_dict):
                skip = True
                all_replace_what.remove(all_replace_what[0])
            elif all_replace_what[0] + len(replace_what) < len(self.c_code) and \
                    (self.c_code[all_replace_what[0] + len(replace_what)] != ' ' and
                     self.c_code[all_replace_what[0] + len(replace_what)] != '\n' and
                     not self.c_code[all_replace_what[0] + len(replace_what)] in op_dict and
                     not self.c_code[all_replace_what[0] + len(replace_what)] in del_dict):
                skip = True
                all_replace_what.remove(all_replace_what[0])
            if not skip:
                self.c_code = self.c_code[:all_replace_what[0]] + replace_to + \
                              self.c_code[all_replace_what[0]+len(replace_what):]
                all_d_quotes = self.find_all('"')
                all_replace_what = self.find_all(replace_what)

    def skip(self):
        """
        Skips spaces
        """
        while self.c_code[self.iterator + 1] == ' ':
            self.get_next_char()