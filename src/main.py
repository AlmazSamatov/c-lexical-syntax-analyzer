from src.lex.lexical_analyzer import get_next_token
from src.syntax.syntax_analyzer import start
import src.preprocessor.preprocessor as preprocessor

with open("in.txt", "r") as file:
    tokens = []
    try:
        preprocessed_code = preprocessor.start(file.read())
        tokens = []
        f = open("out.txt", 'w')
        while True:
            token = get_next_token(preprocessed_code)
            tokens.append(token)
            if token[0] == '_EOF':
                break
    except FileNotFoundError as e:
        print('Error! File in #include statement with name: {} not found.'.format(e.filename))
        exit(0)
    except BaseException as e:
        print('Error! Unable to correctly preprocess #include statement. Error in : ' + e.args[0])
        exit(0)
    start(tokens)
