from src.preprocessor.preprocessor_tool import PreprocessorTool


def test_skip():
    input_string = '       iterator should point to 6th char (char before non space)'
    tool = PreprocessorTool(input_string)
    tool.skip()
    assert tool.iterator == 6


def test_find():
    input_string = 'Do I really need to test built-in features?'
    tool = PreprocessorTool(input_string)
    assert tool.find('really') == 5


def test_find_all():
    input_string = 'This bad boy can find so many "a" in it (4)'
    tool = PreprocessorTool(input_string)
    assert tool.find_all('a') == [6, 14, 26, 31]


def test_set_iterator():
    input_string = 'Useless string, but it is needed to create an object'
    tool = PreprocessorTool(input_string)
    tool.set_iterator(2)
    assert tool.iterator == 2


def test_1_get_next_char():
    input_string = 'It\'s 3AM and I\'m writing this test'
    tool = PreprocessorTool(input_string)
    assert tool.get_next_char() == 'I'


def test_2_get_next_char():
    input_string = ''
    tool = PreprocessorTool(input_string)
    assert tool.get_next_char() == '_EOF'


def test_1_remove_first():
    input_string = 'Removing first entry'
    tool = PreprocessorTool(input_string)
    tool.remove_first('first')
    assert tool.c_code == 'Removing  entry'


def test_2_remove_first():
    input_string = '#define KAZAN_CODE 843'
    tool = PreprocessorTool(input_string)
    tool.remove_first('#define KAZAN_CODE 843')
    assert tool.c_code == ''


def test_replace_all():
    input_string = '// user-defined function to check prime number \n\
            int checkPrimeNumber(int n) \n\
            { \n\
                int j, flag = 1; \n\
                for(j=DVA; j <= n/DVA; ++j) \n\
                { \n\
                    if (n%j == 0) \n\
                    { \n\
                        flag =0; \n\
                         break; \n\
                    } \n\
                 } \n\
            return flag;\n\
            }'
    tool = PreprocessorTool(input_string)
    tool.replace_all('DVA', '2')
    valid_string = '// user-defined function to check prime number \n\
            int checkPrimeNumber(int n) \n\
            { \n\
                int j, flag = 1; \n\
                for(j=2; j <= n/2; ++j) \n\
                { \n\
                    if (n%j == 0) \n\
                    { \n\
                        flag =0; \n\
                         break; \n\
                    } \n\
                 } \n\
            return flag;\n\
            }'
    assert tool.c_code == valid_string