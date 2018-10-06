_PLUS = 2  # +
_MINUS = 3  # -
_STAR = 4  # *
_DIV = 5  # /
_MOD = 6  # %
_ASSIGN = 7  # =
_PASSIGN = 8  # +=
_MASSIGN = 9  # -=
_MULASSIGN = 10  # *=
_DIVASSIGN = 11  # /=
_MODASSIGN = 12  # %=
_EQ = 13  # ==
_GT = 14  # >
_LT = 15  # <
_NEQ = 16  # !=
_GTEQ = 17  # >=
_LTEQ = 18  # <=
_LAND = 19  # &&
_LOR = 20  # ||
_LNOT = 21  # !
_AND = 22  # &
_BOR = 23  # |
_BXOR = 24  # ^
_BCOMP = 25  # ~
_LSHIFT = 26  # <<
_RSHIFT = 27  # >>
_SIZEOF = 28  # sizeof
_BANDASSIGN = 29  # &=
_BORASSIGN = 30  # |=
_BXORASSIGN = 31  # ^=
_LSHIFTASSIGN = 32  # <<=
_RSHIFTASSIGN = 33  # >>=
_COMMA = 34  # ,
_QUEST = 35  # ?
_COLON = 36  # :
_SELECT = 86  # ->
_INC = 87  # ++
_DEC = 88  # --

# Dictionary that correlates lexeme with token
_dictionary = {
    '+': _PLUS,
    '-': _MINUS,
    '*': _STAR,
    '/': _DIV,
    '%': _MOD,
    '=': _ASSIGN,
    '+=': _PASSIGN,
    '-=': _MASSIGN,
    '*=': _MULASSIGN,
    '/=': _DIVASSIGN,
    '%=': _MODASSIGN,
    '==': _EQ,
    '>': _GT,
    '<': _LT,
    '!=': _NEQ,
    '>=': _GTEQ,
    '<=': _LTEQ,
    '&&': _LAND,
    '||': _LOR,
    '!': _LNOT,
    '&': _AND,
    '|': _BOR,
    '^': _BXOR,
    '~': _BCOMP,
    '<<': _LSHIFT,
    '>>': _RSHIFT,
    'sizeof': _SIZEOF,
    '&=': _BANDASSIGN,
    '|=': _BORASSIGN,
    '^=': _BXORASSIGN,
    '<<=': _LSHIFTASSIGN,
    '>>=': _RSHIFTASSIGN,
    ',': _COMMA,
    '?': _QUEST,
    ':': _COLON,
    '->': _SELECT,
    '++': _INC,
    '--': _DEC
}
