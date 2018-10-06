_LBRACKET = 37  # [
_RBRACKET = 38  # ]
_LP = 39  # (
_RP = 40  # )
_LBRACE = 41  # {
_RBRACE = 42  # }
_SPACE = 43  # ' '
_LCOM = 44  # /*
_RCOM = 45  # */
_COM = 46  # //
_SQUOTE = 47  # '
_DQUOTE = 48  # "
_SEMI = 85  # ;

# Dictionary that correlates lexeme with token
_dictionary = {
    '[': _LBRACKET,
    ']': _RBRACKET,
    '(': _LP,
    ')': _RP,
    '{': _LBRACE,
    '}': _RBRACE,
    ' ': _SPACE,
    '/*': _LCOM,
    '*/': _RCOM,
    '//': _COM,
    "'": _SQUOTE,
    '"': _DQUOTE,
    ';': _SEMI
}
