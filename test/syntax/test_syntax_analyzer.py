from src.balancer.balancer import balance
from src.lex.lexical_analyzer import get_next_token
from src.syntax.syntax_analyzer import generate_syntax_tree
import src.preprocessor.preprocessor as preprocessor


def get_json(code):
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
        return get_json(tree)
    return None


def test_for_loop():
    code = '''
    int main(){
        int i = 0;
        int sum = 0;
        for(i; i < 10; i++){
             sum += i;
        }
    }
    '''
    tree = '''
    {
         "Left" : 
         {
              "Left" : "int",
              "Node value" : "main",
         },
         "Node value" : 
         {
              "Left" : "(",
              "Right" : ")"
         },
         "Right" : 
         {
              "Left" : "{",
              "Node value" : 
              {
                   "Left" : 
                   {
                        "Left" : 
                        {
                             "Left" : "int",
                             "Node value" : 
                             {
                                  "Left" : "i",
                                  "Node value" : "=",
                                  "Right" : "0"
                             },
                             "Right" : ";"
                        },
                        "Node value" : 
                        {
                             "Left" : "int",
                             "Node value" : 
                             {
                                  "Left" : "sum",
                                  "Node value" : "=",
                                  "Right" : "0"
                             },
                             "Right" : ";"
                        },
                   },
                   "Node value" : 
                   {
                        "Left" : "for",
                        "Node value" : 
                        {
                             "Left" : "(",
                             "Node value" : 
                             {
                                  "Left" : 
                                  {
                                       "Left" : "i",
                                       "Node value" : ";",
                                  },
                                  "Node value" : 
                                  {
                                       "Left" : 
                                       {
                                            "Left" : "i",
                                            "Node value" : "<",
                                            "Right" : "10"
                                       },
                                       "Node value" : ";",
                                  },
                                  "Right" : 
                                  {
                                       "Node value" : "i",
                                       "Right" : "++"
                                  }
                             },
                             "Right" : ")"
                        },
                        "Right" : 
                        {
                             "Left" : "{",
                             "Node value" : 
                             {
                                  "Node value" : 
                                  {
                                       "Left" : "sum",
                                       "Node value" : "+=",
                                       "Right" : "i"
                                  },
                                  "Right" : ";"
                             },
                             "Right" : "}"
                        }
                   },
              },
              "Right" : "}"
         }
    }
    '''
    assert get_json(code) == tree


def test_if_condition():
    code = '''
    int main(){
        int i = 0;
        int sum = 0;
        for(i; i < 10; i++){
             sum += i;
        }
    }
    '''
    tree = '''
    {
         "Left" : 
         {
              "Left" : "int",
              "Node value" : "main",
         },
         "Node value" : 
         {
              "Left" : "(",
              "Right" : ")"
         },
         "Right" : 
         {
              "Left" : "{",
              "Node value" : 
              {
                   "Left" : 
                   {
                        "Left" : 
                        {
                             "Left" : "int",
                             "Node value" : 
                             {
                                  "Left" : "i",
                                  "Node value" : "=",
                                  "Right" : "1"
                             },
                             "Right" : ";"
                        },
                        "Node value" : 
                        {
                             "Left" : "int",
                             "Node value" : 
                             {
                                  "Left" : "j",
                                  "Node value" : "=",
                                  "Right" : 
                                  {
                                       "Left" : "-",
                                       "Node value" : "1",
                                  }
                             },
                             "Right" : ";"
                        },
                   },
                   "Node value" : 
                   {
                        "Left" : "if",
                        "Node value" : 
                        {
                             "Left" : "(",
                             "Node value" : 
                             {
                                  "Left" : "i",
                                  "Node value" : "==",
                                  "Right" : "0"
                             },
                             "Right" : ")"
                        },
                        "Right" : 
                        {
                             "Left" : "{",
                             "Node value" : 
                             {
                                  "Node value" : 
                                  {
                                       "Left" : "j",
                                       "Node value" : "+=",
                                       "Right" : "1"
                                  },
                                  "Right" : ";"
                             },
                             "Right" : "}"
                        }
                   },
              },
              "Right" : "}"
         }
    }
    '''
    assert get_json(code) == tree

if __name__ == '__main__':
    test_for_loop()
    test_if_condition()
