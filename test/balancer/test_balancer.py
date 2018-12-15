from src.balancer.balancer import balance
from src.syntax.tree import Tree


def check(tree):
    if tree.left == 'a' and tree.right == ';' and tree.node_value is None:
        return True
    return False


def get_tree():
    tree = Tree()
    tree.left = 'a'
    tree.node_value = Tree()
    tree.right = ';'
    return tree


def test():
    assert check(balance(get_tree()))
