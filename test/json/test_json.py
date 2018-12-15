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
    tree.right.node_value = 'None'
    tree.right.right = ')'
    return tree


def test():
    print(to_json(get_tree()))
    assert to_json(get_tree()) == true_json