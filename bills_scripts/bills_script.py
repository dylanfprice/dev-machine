#!/usr/bin/python

# Bills Script
# Last edited: 01/01/2011

# Parses bills.txt and sends e-mails to people who need to pay bills.

import bills_yacc
import sys

def main():
    billsfile = open(sys.argv[1], 'r')
    parse = bills_yacc.parse(billsfile.read())

if __name__ == "__main__":
    main()
