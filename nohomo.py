from pyswip import *
import sys

prolog = Prolog()
prolog.consult('test.pl')

result = prolog.query('''
airport(X),
name(X, Y).
''')
for res in result:
    print(res)

