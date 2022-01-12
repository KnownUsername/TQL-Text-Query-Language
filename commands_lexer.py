
import ply.lex as plex
from ply.lex import TOKEN

class CommandsLexer:
    """ Recognizes tokens of a TQL query """

    operations = ("LOAD", "DISCARD", "SAVE", "SHOW", "SELECT", "CREATE", "PROCEDURE")
    syntax = ("AS", "FROM", "WHERE", "DO", "JOIN", "TABLE", "USING", 'LIMIT')

    comparison_ch = ['>', '<', '=']
    literals = ['*', ';', ',', '(', ')'] + comparison_ch

    tokens = operations + ("file", "var", "nr",) + syntax
    t_ignore = ' '

    def __init__(self):
        self.lexer = None

    def build(self, **kwargs):
        self.lexer = plex.lex(module=self, **kwargs)

    def input(self, string):
        self.lexer.input(string)


    #   --- Token Rules ---   #

    # Error manager
    def t_error(self, t):
        print(f"Unexpected tokens: {t.value[0:10]}")
        exit(1)

    @TOKEN("|".join(operations))
    def t_operation(self, t):
        t.type = t.value
        return t

    @TOKEN("|".join(syntax))
    def t_syntax(self, t):
        t.type = t.value
        return t

    def t_file(self, t):
        r'"\.[\/[^<>:\"\/\|?*]+]+" | "[^<>:\"\/\|?*]+" '
        t.value = t.value[1:-1]
        #t.type = "file"
        return t

    def t_nr(self, t):
        r'[0-9]+(\.[0-9]+)?'
        t.value = float(t.value)
        return t

    def t_var(self, t):
        r"_[a-zA-Z0-9_@$]+ | [a-zA-Z][a-zA-Z0-9_@$]*"
        return t
