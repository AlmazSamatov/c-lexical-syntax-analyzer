class Tree:
    """
    AST
    """
    left = None
    right = None
    node_value = None

    def __init__(self, left=None, node_value=None, right=None):
        self.left = left
        self.node_value = node_value
        self.right = right