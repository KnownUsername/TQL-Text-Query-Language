from commands_lexer import CommandsLexer
import ply.yacc as pyacc

class CommandsGrammar:
    """ Grammar processor for TQL queries"""

    def __init__(self):
        self.yacc = None
        self.lexer = None
        self.tokens = None

    def build(self, **kwargs):
        self.lexer = CommandsLexer()
        self.lexer.build(**kwargs)
        self.tokens = self.lexer.tokens
        self.yacc = pyacc.yacc(module=self, **kwargs)

    def parse(self, string):
        self.lexer.input(string)
        return self.yacc.parse(lexer=self.lexer.lexer)

    def p_prompt(self, p):
        """ prompt : prompt ';' command
                       | command """

        # For only 1 var
        if len(p) == 2:
            p[0] = [p[1]]

        else:
            p[0] = [p[1]]
            p[0].append(p[3])


    def p_command(self, p):
        """ command : query
                    | q_procedure """
        p[0] = p[1]


    def p_procedure(self, p):
        """ q_procedure : PROCEDURE var DO query_list ';' END """
        p[0] = {'op': p[1], 'args': {'procedure_name': p[2], 'queries': p[4]}}


    def p_query(self, p):
        """ query : q_load
                  | q_discard
                  | q_save
                  | q_show
                  | q_create
                  | q_select
                  """
        p[0] = p[1]

    def p_query_list(self, p):
        """ query_list : query_list ';' query
                       | query """

        # For only 1 var
        if len(p) == 2:
            p[0] = [p[1]]

        else:
            p[0] = [p[1]]
            p[0].append(p[3])

    def p_load(self, p):
        """ q_load : LOAD TABLE var FROM file """
        p[0] = {"op": p[1], "args": {"table": p[3], "file": p[5]}}

    def p_discard(self, p):
        """ q_discard : DISCARD TABLE var """
        p[0] = {"op": p[1], "args": {"table": p[3]}}

    def p_save(self, p):
        """ q_save : SAVE TABLE var AS file """
        p[0] = {"op": p[1], "args": {"table": p[3], "file": p[5]}}

    def p_show(self, p):
        """ q_show : SHOW TABLE var """
        p[0] = {"op": p[1], "args": {"table": p[3]}}

    def p_select(self, p):
        """ q_select : SELECT columns FROM var param_where param_lim """
        p[0] = {'op': p[1], 'args': {'columns': p[2], 'table': p[4], 'params': {'where': p[5], 'limit': p[6]}}}

    def p_limit(self, p):
        """ param_lim : LIMIT IntNr
                     |"""
        if len(p) == 3:
            p[0] = p[2]

    def p_where(self, p):
        """ param_where : WHERE COMPARISON
                        |"""
        if len(p) == 3:
            print(p[2])
            p[0] = p[2]

    def p_comparisons(self, p):
        """ COMPARISON : var '>' nr
             | var '<' nr
             | var BE nr
             | var LE nr
             | var DIFFERENT nr
             | var '=' nr
             | var '=' file
             | var DIFFERENT file
             | B
        """
        if len(p) == 4:
            p[0] = {'op': p[2], 'column': p[1], 'value': p[3]}

        else:
            p[0] = p[1]

    def p_booleans(self, p):
        """ B : COMPARISON Bool_Op COMPARISON
             | '(' COMPARISON Bool_Op COMPARISON ')'
        """

        print(f'Actual: {p[0]}')
        if len(p) == 4:
            print(f'p[0]: {p[0]} \n p[1]: {p[1]} \n p[2]: {p[2]} \n p[3]: {p[3]}')
            p[0] = {'op': p[2], 'conditions': [p[1], p[3]]}

        elif len(p) == 6:
            p[0] = {'op': p[3], 'prioritized_conditions': [p[2], p[4]]}

    def p_OP_bools(self, p):
        """ Bool_Op : AND
                    | OR """
        p[0] = p[1]

    def p_columns(self, p):
        """ columns : '*'
                    | var_columns """
        p[0] = p[1]

    def p_varColumns(self, p):
        """ var_columns : var_columns ',' var
                        | var """

        # For only 1 var
        if len(p) == 2:
            p[0] = [p[1]]

        else:
            p[0] = p[1]
            p[0].append(p[3])


    def p_create(self, p):
        """ q_create : CREATE TABLE var FROM create_source """
        p[0] = {"op": p[1], "args": {"result_table": p[3], 'source': p[5]}}

    def p_createSource(self, p):
        """ create_source : table_join
                          | q_select """
        p[0] = p[1]

    def p_join(self, p):
        """ table_join : var JOIN var USING '(' var ')' """
        p[0] = {"op": p[2], "args": {"tables": [p[1], p[3]], "column": p[6]}}

    def p_error(self, p):
        if p:
            raise Exception(f"Syntax error: unexpected '{p.type}' on '{p.value}'")
        else:
            raise Exception("Syntax error: unexpected end of file")