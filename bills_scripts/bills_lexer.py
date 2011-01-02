#----------------------------------------
# bills_lex.py
# 
# tokenizer for bills.txt
#----------------------------------------

from decimal import Decimal
from datetime import date

# List of token names
tokens = (
    'STRING',
    'AMOUNT',
    'DATE',
    'NEWLINE',
    'COLON',
    'ASTERISK',
    'EQUALS',
    'X'
)

t_STRING    = r'\w\w+'
t_NEWLINE   = r'\n|\r|\r\n|\n\r'
t_COLON     = r':'
t_ASTERISK  = r'\*'
t_EQUALS    = r'='
t_X         = r'X'


def t_AMOUNT(t):
    r'\$\d+(\.\d\d)?'
    t.value = Decimal(t.value[1:])
    return t

def t_DATE(t):
    r'\d\d?\/\d\d?'
    month, day = map(int, t.value.split('/'))
    t.value = date(date.today().year, month, day)
    return t

t_ignore = ' \t'

def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

# Tests the lexer
def main():
    import ply.lex as lex
    lexer = lex.lex(debug=1)
    
    input = '''
    Comcast: $50 due on 01/1
    * Alex = $50
    * Dylan = $20
    X Mark = $30
    
    Utilities: $250 due on 02/21
    
    
    '''
    
    lexer.input(input)
    
    for tok in lexer:
        print tok.type, tok.value

if __name__ == "__main__":
    main()
