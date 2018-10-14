from src.syntax.tree import Tree


def balance(tree):
    if tree.node_value is not None and isinstance(tree.node_value, Tree):
        subtree = tree.node_value

        if subtree.left is None and subtree.right is None and subtree.node_value is None:
            tree.node_value = None

        branches = []

        if subtree.right is not None:
            branches.append(subtree.right)
        if subtree.left is not None:
            branches.append(subtree.left)
        if subtree.node_value is not None:
            branches.append(subtree.node_value)

        if len(branches) == 1:
            tree.node_value = branches[0]

        if tree.left is None and tree.right is None and subtree.left is None and subtree.right is None and \
                isinstance(subtree.node_value, Tree) \
                and ((isinstance(subtree.node_value.node_value, Tree) and
                      subtree.node_value.right is not None and subtree.node_value.left is not None)
                     or not isinstance(subtree.node_value.node_value, Tree)):
            tree.left = subtree.node_value.left
            tree.right = subtree.node_value.right
            tree.node_value = subtree.node_value.node_value

    if isinstance(tree.right, Tree):
        tree.right = balance(tree.right)
    if isinstance(tree.left, Tree):
        tree.left = balance(tree.left)
    if isinstance(tree.node_value, Tree):
        tree.node_value = balance(tree.node_value)
    return tree
