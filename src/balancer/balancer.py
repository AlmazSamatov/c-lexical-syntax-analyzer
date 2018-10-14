from src.syntax.tree import Tree


def is_tree(object):
    return isinstance(object, Tree)


def is_one(tree):
    branches = []

    if tree.left is not None:
        branches.append((tree.left, 'left'))
    if tree.right is not None:
        branches.append((tree.right, 'right'))
    if tree.node_value is not None:
        branches.append((tree.node_value, 'node_value'))

    if len(branches) == 1:
        return branches[0]
    return None


def balance(tree):
    subtrees = []

    if is_tree(tree.node_value):
        subtrees.append((tree.node_value, 'node_value'))
    if is_tree(tree.right):
        subtrees.append((tree.right, 'right'))
    if is_tree(tree.left):
        subtrees.append((tree.left, 'left'))

    for subtree, name in subtrees:

        if subtree.left is None and subtree.right is None and subtree.node_value is None:
            setattr(tree, name, None)

        one = is_one(subtree)
        if one:
            while one:
                if is_tree(one[0]) and is_one(one[0]):
                    one = is_one(one[0])
                else:
                    break
            setattr(tree, name, one[0])

    # if tree.left is None and tree.right is None and subtree.left is None and subtree.right is None and \
    #         is_tree(subtree.node_value, Tree) \
    #         and ((is_tree(subtree.node_value.node_value, Tree) and
    #               subtree.node_value.right is not None and subtree.node_value.left is not None)
    #              or not is_tree(subtree.node_value.node_value, Tree)):
    #     tree.left = subtree.node_value.left
    #     tree.right = subtree.node_value.right
    #     tree.node_value = subtree.node_value.node_value
    #
    # if subtree.left is None and subtree.right is None and subtree.node_value is not None:
    #     while subtree.left is None and subtree.right is None and subtree.node_value is not None:
    #         subtree = subtree.node_value
    #     tree.node_value = subtree
    #
    # if subtree.node_value is None and subtree.right is None and subtree.left is not None:
    #     while subtree.node_value is None and subtree.right is None and subtree.left is not None:
    #         subtree = subtree.left
    #     tree.node_value = subtree
    #
    # if subtree.left is None and subtree.node_value is None and subtree.right is not None:
    #     while subtree.left is None and subtree.node_value is None and subtree.right is not None:
    #         subtree = subtree.right
    #     tree.node_value = subtree

    if is_tree(tree.right):
        tree.right = balance(tree.right)
    if is_tree(tree.left):
        tree.left = balance(tree.left)
    if is_tree(tree.node_value):
        tree.node_value = balance(tree.node_value)
    return tree
