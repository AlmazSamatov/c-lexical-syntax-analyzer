import antlr.syntax_analyzer as syntax_analyzer


def test():
    syntax_analyzer.analyze('test_in.txt', 'test_out.txt')

    with open('test_out.txt', 'r') as output:
        json = output.read()

        with open('test_true_out.txt', 'r') as output:
            assert json == output.read()


if __name__ == '__main__':
    test()
