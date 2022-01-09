
class CommandsGrammar:
    """ Grammar processor for TQL queries"""

    def p_load(self, p):
        """ q_load : LOAD TABLE var FROM file """
        p[0] = {"op": p[1], "args": {"table": p[3], "file": p[5]}}

    def p_discard(self, p):
        """ q_discard: DISCARD TABLE var """
        p[0] = {"op": p[1], "args": {"table": p[3]}}
