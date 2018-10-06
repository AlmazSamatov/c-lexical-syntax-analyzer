from src.lexical_analyzer import get_next_token, scan
import src.preprocessor as preprocessor

with open("in.txt", "r") as file:
    try:
        preprocessed_code = preprocessor.start(file.read())
        f = open("out.txt", 'w')
        while True:
            token = get_next_token(preprocessed_code)
            f.write(str(token) + "\n")
            if token[0] == '_EOF':
                break
    except FileNotFoundError as e:
        print('Error! File in #include statement with name: {} not found.'.format(e.filename))
        exit(0)
    except BaseException as e:
        print('Error! Unable to correctly preprocess #include statement. Error in : ' + e.args[0])
        exit(0)
