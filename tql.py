from commands_lexer import CommandsLexer

cl = CommandsLexer()

for expr in iter(lambda: input(">> "), ""):
    try:
        cl.process(expr)
    except Exception as e:
        print(f'\033[91m-> {e}\033[0m')
