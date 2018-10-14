from src.json.generate_json import to_json
from src.syntax.tree import Tree

true_json = '''{
     "Left" : "int",
     "Node value" : "main",
     "Right" : 
     {
          "Left" : "(",
          "Node value" : "None",
          "Right" : ")"
     }
}'''

def get_tree():
    tree = Tree()
    tree.left = 'int'
    tree.node_value = 'main'
    tree.right = Tree()
    tree.right.left = '('
    tree.right.right = ')'
    return tree

def test():
    assert to_json(get_tree()) == true_json
