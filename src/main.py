import src.preprocessor.preprocessor as preprocessor
from src.json.generate_json import to_json
from src.lex.lexical_analyzer import get_next_token
from src.syntax.syntax_analyzer import generate_syntax_tree

with open("in.txt", "r") as input_file:
    tokens = []
    try:
        preprocessed_code = preprocessor.start(input_file.read())
        tokens = []
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

    with open("out.txt", 'w') as output_file:
        output_file.write(to_json(generate_syntax_tree(tokens)))
