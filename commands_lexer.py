
import ply.lex as plex


class CommandsLexer:
    """ Recognizes tokens of a TQL query """

    operations = ("LOAD", "DISCARD", "SAVE", "SHOW", "SELECT", "CREATE", "PROCEDURE")
    syntax = ("AS", "FROM", "WHERE", "DO", "JOIN", "TABLE")

    comparison_ch = ['>', '<', '=']
    literals = ['*', ';', ','] + comparison_ch

    tokens = operations + ("filename", "variable", "number",) + syntax
    t_ignore = ' <= >= <>'

    def __init__(self):
        self.lexer = None

    def process(self, string):
        self.lexer = plex.lex(module=self)
        self.lexer.input(string)

        for token in iter(self.lexer.token, None):
            pass


    #   --- Token Rules ---   #

    # Error manager
    def t_error(self, t):
        print(f"Unexpected tokens: {t.value[0:10]}")
        exit(1)

    def t_operation(self, t):
        r"LOAD|DISCARD|SAVE|SHOW|SELECT|CREATE|PROCEDURE"
        t.type = t.value
        return t

    def t_syntax(self, t):
        r"AS|FROM|WHERE|DO|JOIN|TABLE"
        t.type = t.value
        return t

    def t_filename(self, t):
        r'"[^<>:\"/\|?*]+"'
        t.type = "filename"
        return t

    def t_number(self, t):
        r'[0-9]+(\.[0-9]+)?'
        t.type = 'number'
        return t

    def t_variable(self,t):
        r"_[a-zA-Z0-9_@$]+ | [a-zA-Z][a-zA-Z0-9_@$]*"
        return t
