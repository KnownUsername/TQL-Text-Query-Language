import pandas as pd
import os.path

class CommandsEval:

    loaded_tables = {}

    operators = {
        "LOAD": lambda args, filename: CommandsEval._load(args),
        "DISCARD": lambda args: CommandsEval._discard(args),
        "SAVE": lambda args, filename: CommandsEval._save(args),
        "SHOW": lambda args: CommandsEval._show(args),
        "CREATE": lambda args: args,
        "SELECT": lambda args: args
    }


    @staticmethod
    def _load(args):
        """ Loads a table - Loads csv file to memory """

        # Check if values' fields exists
        try:
            table_name = args['table']
        except KeyError:
            raise KeyError('Table value was not found')

        try:
            filename = args['file']
        except KeyError:
            raise KeyError(f' Filename was not found')


        # Check if there is only 1 value that is a string
        if type(table_name) is not str:
            raise TypeError("Table has invalid type")
        if type(filename) is not str:
            raise TypeError("Filename has invalid type")



        # Check if file's extension is csv
        if not CommandsEval.is_csv(filename):
            raise Exception('File extension is not csv')

        try:
            # Read csv file and store it as Data Frame
            table = pd.read_csv(filename)

        # Check if file exists
        except FileNotFoundError:
            raise FileNotFoundError

        # Check if name of table, is already being used
        if table_name in CommandsEval.loaded_tables.keys():
            raise Exception(f'There is already loaded, a table with the name: {table_name}')

        # Store table on tables' dictionary
        CommandsEval.loaded_tables[table_name] = table

        return True

    @staticmethod
    def _discard(args):
        """ Discards a table - removes from memory """

        # Check if field exists
        try:
            table_name = args['table']
        except KeyError:
            raise KeyError('Table value was not found')

        # Check if there is only 1 value that is a string
        if type(table_name) is not str:
            raise TypeError("Table has invalid type")

        # Table must be loaded - on tables' dictionary
        if table_name in CommandsEval.loaded_tables:
            # Removal of desired table
            del CommandsEval.loaded_tables[table_name]

        else:
            raise Exception('Table is not loaded')

    @staticmethod
    def _show(args):
        """ Presents table on console"""

        # Check if field exists
        try:
            table_name = args['table']
        except KeyError:
            raise KeyError('Table value was not found')

        # Check if there is only 1 value that is a string
        if type(table_name) is not str:
            raise TypeError("Table has invalid type")

        # Table must be loaded - on tables' dictionary
        if table_name in CommandsEval.loaded_tables:
            print(CommandsEval.loaded_tables[table_name])
        return True

    @staticmethod
    def _save(args):
        """ Saves table on a csv file"""

        # Check if fields exists
        try:
            table_name = args['table']
        except KeyError:
            raise KeyError(f'Table value was not found')

        try:
            filename = args['file']
        except KeyError:
            raise KeyError(f' Filename was not found')


        # Check if there is only 1 value, that is a string
        if type(table_name) is not str:
            raise TypeError("Table has invalid type")
        if type(filename) is not str:
            raise TypeError("Filename has invalid type")




        # Check if file is loaded
        if table_name not in CommandsEval.loaded_tables:
            raise Exception('Table is not loaded')

        # Check if file's extension is csv
        if not CommandsEval.is_csv(filename):
            raise Exception('File extension is not csv')

        # Check if file already exists
        if os.path.isfile(filename):
            raise FileExistsError

        try:
            # Store table into a csv file
            CommandsEval.loaded_tables[table_name].to_csv(filename)
        except Exception:
            raise Exception
        finally:
            print(f"Table {table_name} was successfully saved as {filename}")


    @staticmethod
    def present_table(table):
        """ Presents table on console"""

    @staticmethod
    def is_csv(filename):
        """ Checks if file extension is csv """
        return True if filename[-4:] == '.csv' else False

    @staticmethod
    def evaluate(ast):
        if type(ast) in (bool, float, str):
            return ast
        if type(ast) is dict:
            return CommandsEval._eval_operator(ast)
        if type(ast) is list:
            ans = None
            for a in ast:
                ans = CommandsEval.evaluate(a)
            return ans

        raise Exception("Unknown AST type")

    @staticmethod
    def _eval_operator(ast):

        if 'op' in ast:
            op = ast["op"]

            args = [arg for arg in ast['args']]

            if op in CommandsEval.operators:
                func = CommandsEval.operators[op]
                return func(args)
            else:
                raise Exception(f"Unknown operator {op}")

        raise Exception('Undefined AST')