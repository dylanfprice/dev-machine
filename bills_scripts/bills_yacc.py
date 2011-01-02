
#----------------------------------------
# bills_yacc.py
# 
# parser for bills.txt
#----------------------------------------

import ply.yacc as yacc
import ply.lex as lex

# Get the token map from the lexer.
import bills_lexer
tokens = bills_lexer.tokens

def p_bills(p):
    '''bills : bill bills
             | NEWLINE bills
             | empty '''
    if not p[1]:
        p[0] = []
    elif type(p[1]) is dict:
        p[2].append(p[1])
        p[0] = p[2]
    else:
        p[0] = p[2]

def p_bill(p):
    'bill : STRING COLON AMOUNT STRING STRING DATE NEWLINE names'
    p[0] = {
        'bill'      : p[1],
        'amount'    : p[3],
        'due_date'  : p[6],
        'names'     : p[8]
    }

def p_names(p):
    '''names : name_asterisk names 
             | name_x names
             | empty '''
    if not p[1]:
        p[0] = {}
    else:
        p[0] = dict(p[2], **p[1])

def p_name_asterisk(p):
    'name_asterisk : ASTERISK STRING EQUALS AMOUNT NEWLINE'
    p[0] = {p[2] : (p[4], False)}

def p_name_x(p):
    'name_x : X STRING EQUALS AMOUNT NEWLINE'
    p[0] = {p[2] : (p[4], True)}

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    print "Syntax error in input!"

parser = yacc.yacc(debug=0)
def parse(input):
    return parser.parse(input, lexer=lex.lex(module=bills_lexer))

# Tests the parser
def main():
    parser = yacc.yacc(debug=1)

    input = '''
    Comcast: $50 due on 01/1
    * Alex = $50
    * Dylan = $20
    X Mark = $30
    
    Utilities: $250 due on 02/21
    
    
    '''
    
    print parser.parse(input, lexer=lex.lex(module=bills_lexer))

if __name__ == "__main__":
    main()
