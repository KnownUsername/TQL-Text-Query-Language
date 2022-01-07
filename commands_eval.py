from csv_record_lexer import CSVRecordLexer
from csv_record import CSV_Record


class CommandsEval:

    loaded_tables = {}

    @staticmethod
    def load(table_name, filename):

        # Read file and apply lex
        csvr = CSVRecordLexer(filename)
        csvr.process()

        # Store table on tables' dictionary
        CommandsEval.loaded_tables[table_name] = csvr.records

        return True
