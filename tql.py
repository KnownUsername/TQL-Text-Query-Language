from commands_grammar import CommandsGrammar
from pprint import PrettyPrinter
from commands_eval import CommandsEval

cg = CommandsGrammar()
cg.build()


pp = PrettyPrinter()


for expr in iter(lambda: input(">> "), ""):
    try:
        ans = cg.parse(expr)
        pp.pprint(ans)
        answer = CommandsEval.evaluate(ans)
        if answer is not None:
            print(f"<< {answer}")
    except Exception as e:
        print(e)

