from src.syntax.tree import Tree

five_spaces = '     '


def to_json(tree, spaces_needed=0):
    json_tree = [spaces_needed * five_spaces, '{\n']
    branches = [(tree.left, 'Left'), (tree.node_value, 'Node value'), (tree.right, 'Right')]
    for branch, branch_name in branches:
        if branch is None:
            continue
        if isinstance(branch, str):
            json_tree.append((spaces_needed + 1) * five_spaces)
            json_tree.append('"{}" : "{}"'.format(branch_name, branch))
        elif isinstance(branch, Tree):
            json_tree.append((spaces_needed + 1) * five_spaces)
            json_tree.append('"{}" : \n'.format(branch_name))
            json_tree.append(to_json(branch, spaces_needed + 1))
        elif branch is None:
            json_tree.append((spaces_needed + 1) * five_spaces)
            json_tree.append('"{}" : "{}"'.format(branch_name, branch))

        if branch_name == 'Right':
            json_tree.append('\n')  # Right is last and there is no need for comma
        else:
            json_tree.append(',\n')

    json_tree.append(spaces_needed * five_spaces)
    json_tree.append('}')
    return ''.join(json_tree)
