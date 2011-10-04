
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
    '''bill : STRING COLON AMOUNT STRING STRING DATE NEWLINE names
            | STRING STRING COLON AMOUNT STRING STRING DATE NEWLINE names'''
    if len(p) == 9:
        p[0] = {
            'bill'      : p[1],
            'amount'    : p[3],
            'due_date'  : p[6],
            'names'     : p[8]
        }
    else:
        p[0] = {
            'bill'      : p[1] + ' ' + p[2],
            'amount'    : p[4],
            'due_date'  : p[7],
            'names'     : p[9]
        }

def p_names(p):
    '''names : names name_asterisk
             | names name_x
             | name_asterisk
             | name_x '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = dict(p[1], **p[2])

def p_name_asterisk(p):
    '''name_asterisk : ASTERISK STRING EQUALS AMOUNT NEWLINE
                     | ASTERISK STRING NEWLINE '''
    if len(p) == 6:
        p[0] = {p[2] : (p[4], False)}
    else:
        p[0] = {p[2] : (-1, False)}

def p_name_x(p):
    '''name_x : X STRING EQUALS AMOUNT NEWLINE
              | X STRING NEWLINE '''
    if len(p) == 6:
        p[0] = {p[2] : (p[4], True)}
    else:
        p[0] = {p[2] : (-1, True)}

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    print "Syntax error in input: %s!" % p

parser = yacc.yacc(debug=0)
def parse(input):
    return parser.parse(input, lexer=lex.lex(module=bills_lexer))

# Tests the parser
def main():
    parser = yacc.yacc(debug=1)

    input = '''
Comcast: $50 due on 01/3
* Alex = $50
* Dylan = $20
X Mark = $30

Utilities: $250 due on 01/8
X Mike
* Mark

Extra Deposit: $100 due on 10/31
* Alex
* Dylan
* Mark
'''

    print parser.parse(input, lexer=lex.lex(module=bills_lexer))

if __name__ == "__main__":
    main()
