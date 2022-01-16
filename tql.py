"""
    Project: TQL-TEXT-QUERY-LANGUAGE
    Purpose: Academical
    Description:

    Author: João Rodrigues
    Student No.: 16928

    Course: LESI
    Subject: Languages Processing
    College: IPCA
    Academic year: 2021/2022
"""
from commands_grammar import CommandsGrammar
from pprint import PrettyPrinter
from commands_eval import CommandsEval
import sys

cg = CommandsGrammar()
cg.build()


pp = PrettyPrinter()

# Check if has filename
if len(sys.argv) > 1:
    filename = sys.argv[1]

    with open(filename, "r") as f:
        content = f.read()
        try:
            ans = cg.parse(content)
            if ans is not None:
                print(ans)
        except Exception as exception:
            print(exception)

# For commands input on console
for expr in iter(lambda: input(">> "), ""):
    try:
        ans = cg.parse(expr)
        pp.pprint(ans)
        answer = CommandsEval.evaluate(ans)
        if answer is not None:
            print(f"<< {answer}")
    except Exception as e:
        print(e)

