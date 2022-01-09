
class CommandsGrammar:
    """ Grammar processor for TQL queries"""

    def p_query(self, p):
        """ query : q_load
                  | q_discard
                  | q_save
                  | q_show
                  | q_create
                  | q_select
                  """

    def p_load(self, p):
        """ q_load : LOAD TABLE var FROM file """
        p[0] = {"op": p[1], "args": {"table": p[3], "file": p[5]}}

    def p_discard(self, p):
        """ q_discard: DISCARD TABLE var """
        p[0] = {"op": p[1], "args": {"table": p[3]}}

    def p_save(self, p):
        """ q_save: SAVE TABLE var AS file """
        p[0] = {"op": p[1], "args": {"table": p[3], "file": p[5]}}

    def p_show(self, p):
        """ q_show: SHOW TABLE var """
        p[0] = {"op": p[1], "args": {"table": p[3]}}

    def p_select(self, p):
        """ q_select: SELECT columns FROM var param_where param_lim """
        p[0] = {'op': p[1], 'columns': p[2], 'table': p[4], 'params': [p[5], p[6]]}

    def p_limit(self, p):
        """ param_lim:
                     | LIMIT nr """
        if len(p) == 3:
            p[0] = {'param': p[1], 'value': p[2]}
        #else:
        #    p[0] = p[1]

    def p_where(self, p):
        """ param_where:
                        | WHERE B """
        if len(p) == 3:
            p[0] = {'param': p[1], 'value': p[2]}
        #else:
        #    p[0] = p[1]

    def p_booleans(self, p):
        """ B: var > nr
             | var < nr
             | var >= nr
             | var <= nr
             | var <> nr
             | var = nr
             | var = file
             | var <> file
        """
        p[0] = {'op': p[2], 'args': {'column': p[1], 'value': p[3]}}

    def p_columns(self, p):
        """ columns : *
                    | var_columns """
        p[0] = p[1]

    def p_varColumns(self, p):
        """ var_columns : var_columns ',' var
                        | var """
        p[0] = p[1]
        p[0].append(p[3])

    def p_create(self, p):
        """ q_create: CREATE TABLE var FROM create_source """
        p[0] = {"op": p[1], "args": {"result_table": p[3], 'source': p[5]}}

    def p_createSource(self, p):
        """ create_source : table_join
                          | q_select """
        p[0] = p[1]

    def p_join(self, p):
        """ table_join: var JOIN var USING'(' var ')' """
        p[0] = {"op": p[2], "args": {"tables": [p[1], p[3]], "column": p[6]}}
