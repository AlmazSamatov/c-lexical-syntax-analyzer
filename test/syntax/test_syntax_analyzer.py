from src.lex.lexical_analyzer import get_next_token
from src.syntax.syntax_analyzer import generate_syntax_tree
import src.preprocessor.preprocessor as preprocessor


def get_tree(code):
    tokens = []
    preprocessed_code = preprocessor.start(code)
    tokens = []
    while True:
        token = get_next_token(preprocessed_code)
        tokens.append(token)
        if token[0] == '_EOF':
            break
    return generate_syntax_tree(tokens)


def test_for_loop():
    code = '''
        int main(){
            int i;
            int b = 0;
            for(i = 0; i < 10; i++){
                 b--;
            }
        }
    '''
    tree = '''
        
    '''
    assert get_tree(code) is not None
