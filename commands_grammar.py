
class CommandsGrammar:
    """ Grammar processor for TQL queries"""

    def p_query(self, p):
        """ query : q_load
                  | q_discard
                  | q_save
                  | q_show
                  | q_create
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