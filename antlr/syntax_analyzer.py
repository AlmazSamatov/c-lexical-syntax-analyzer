import json

from antlr.antlr.CLexer import CLexer
from antlr.antlr.CParser import CParser
from src.preprocessor.preprocessor import start
from antlr4 import *
from antlr4.tree.Tree import TerminalNodeImpl, ErrorNodeImpl, ParseTree, Tree


def parse(input_file_name):
    with open(input_file_name, "r") as input_file:
        input_code = start(input_file.read())
        lexer = CLexer(InputStream(input_code))
        stream = CommonTokenStream(lexer)
        parser = CParser(stream)
        tree = parser.translationUnit()
        return to_json(tree)


def traverse(tree, dict):
    if tree.getChildCount() == 0:
        if isinstance(tree, TerminalNodeImpl):
            dict['type'] = tree.getSymbol().type
            dict['text'] = tree.getSymbol().text
    else:
        childs = []
        name = tree.__class__.__name__.replace('Context$', '')
        dict[name[0].lower() + name[1:]] = childs

        for i in range(tree.getChildCount()):
            n = {}
            childs.append(n)
            traverse(tree.getChild(i), n)


def to_json(tree):
    ast = {}
    traverse(tree, ast)
    return json.dumps(ast, ensure_ascii=False, indent=4)


def analyze(input_file_name='in.txt', output_file_name='out.txt'):
    with open(output_file_name, "w") as output_file:
        output_file.write(parse(input_file_name))


if __name__ == '__main__':
    analyze()
