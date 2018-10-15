from src.balancer.balancer import balance
from src.lex.lexical_analyzer import get_next_token
import src.lex.lexical_analyzer
from src.json.generate_json import to_json
from src.syntax.syntax_analyzer import generate_syntax_tree
import src.preprocessor.preprocessor as preprocessor


def get_json(code):
    src.lex.lexical_analyzer.token_it = -1
    preprocessed_code = preprocessor.start(code)
    tokens = []
    while True:
        token = get_next_token(preprocessed_code)
        tokens.append(token)
        if token[0] == '_EOF':
            break
    tree = generate_syntax_tree(tokens)
    if tree is not None:
        tree = balance(tree)
        return to_json(tree)
    return None


def test_for_loop():
    code = '''
    int main(){
        int i = 0;
        int sum = 0;
        for(i; i < 10; i++){
             sum += i;
        }
    }'''
    assert get_json(code) is not None


def test_if_condition():
    code = '''
    int main(){
        int i = 0;
        int sum = 0;
        if(i == 0){
            sum = 1;
        }
    }
    '''
    assert get_json(code) is not None

if __name__ == '__main__':
    test_for_loop()
    test_if_condition()
