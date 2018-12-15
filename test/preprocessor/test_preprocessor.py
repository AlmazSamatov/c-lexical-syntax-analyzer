from src.preprocessor.preprocessor import *


def test_replace_all():
    input_string = '#define DVA 2\n' \
                   '// user-defined function to check prime number \n\
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
    valid_string = '\n// user-defined function to check prime number \n\
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
    assert replace_all(input_string, 'DVA', '2') == valid_string


def scan_for_define():
    input_string = '#define DVA 2\n' \
                   '// user-defined function to check prime number \n\
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
    result = {
        'DVA': '2'
    }
    assert scan_for_define(input_string) == result


def test_start():
    input_string = '#define DVA 2\n' \
                   '// user-defined function to check prime number \n\
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
    valid_string = '\n\
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
    assert start(input_string) == valid_string


def test_oneline_comment():
    in_c = '// Simple comment that says it should be deleted'
    assert delete_oneline_comments(in_c) == ''


def test_delete_comments_universal():
    in_c = '#  what if comments start not like in c? \nHope this line isn\'t deleted'
    assert delete_comments_universal(in_c, '#', '\n') == 'Hope this line isn\'t deleted'


def test_delete_comments():
    in_c = '// HOLY COW!!! \n' \
           '/* THIS \nTHING \nCAN \nDELETE \nALL \nTYPES \nOF \nC \nCOMMENTS!'
    assert delete_comments(in_c) == ''


def test_delete_multiline_comments():
    in_c = '/* this \n is \n very \n big \n comment*/'
    assert delete_multiline_comments(in_c) == ''


def test_delete_from_string_indexes():
    string = 'Hello*delete this*!'
    assert delete_from_string_indexes(string, [(5, 17)]) == 'Hello!'
    pass
