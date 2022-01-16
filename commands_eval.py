"""
    Project: TQL-TEXT-QUERY-LANGUAGE
    Purpose: Academical
    Description: Attributes function to expression received

    Author: João Rodrigues
    Student No.: 16928

    Course: LESI
    Subject: Languages Processing
    College: IPCA
    Academic year: 2021/2022
"""

import pandas as pd
import os.path
from IPython.display import display


class CommandsEval:

    loaded_tables = {}
    procedures = {}

    operators = {
        "LOAD": lambda args: CommandsEval._load(args),
        "DISCARD": lambda args: CommandsEval._discard(args),
        "SAVE": lambda args: CommandsEval._save(args),
        "SHOW": lambda args: CommandsEval._show(args),
        "CREATE": lambda args: CommandsEval._create(args),
        "SELECT": lambda args: CommandsEval._select(args),

        "PROCEDURE": lambda args: CommandsEval._procedure(args),
        "CALL": lambda args: CommandsEval._call(args)
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
        print(f"Table '{table_name}' was successfully loaded")

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
            print("Table removed with success!")
            print(f"Current active tables: {CommandsEval.loaded_tables.keys()}")
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

    @staticmethod
    def _save(args):
        """ Saves table on a csv file"""

        # Check if fields exists
        try:
            table_name = args['table']
            filename = args['file']
        except KeyError as e:
            raise KeyError(f'{e.args[0].capitalize()} value was not found on input')




        table_name = 2
        # Check if there is only 1 value, that is a string
        if type(table_name) is not str:
            raise TypeError(f"f{TypeError.args[0]} has invalid type")
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
    def _select(args):
        """ Shows given table with parameters given.

        These parameters could be:
           - Slice of columns
           - Filter of values
           - Limited quantity of values presented
        """

        # Check if field exists
        try:
            columns = args['columns']
            table = args['table']
            where_parameter = args['params']['where']
            limit_parameter = args['params']['limit']
        except KeyError as e:
            raise KeyError(f'{e.args[0].capitalize()} value was not found on input')

        # Check if name of table, is already being used
        if table not in CommandsEval.loaded_tables.keys():
            raise Exception(f'Table "{table}" is not loaded')

        # Check type of each variable

        # Check if table exists  // Maybe add to try/except that's before it
        original_table = CommandsEval.loaded_tables[table]
        parameterized_table = original_table

        # Check if there is any parameter for WHERE
        if where_parameter:

            # Variables assignment, for more readable code
            operator = where_parameter['op']
            column = where_parameter['column']
            value = where_parameter['value']

            # Apply condition, based on given operator
            parameterized_table = CommandsEval._alternate_operator(parameterized_table, column, operator, value)

        # Check if there is any parameter for LIMIT
        if limit_parameter:
            parameterized_table = parameterized_table[:limit_parameter]

        # Filter columns
        if columns != '*':
            parameterized_table = parameterized_table.loc[:, columns]

        display(parameterized_table)

        return parameterized_table

    @staticmethod
    def _create(args):
        """ Creates a new table from other tables """

        # Retrieve primary data
        table_name = args['result_table']
        source_op = args['source']

        # For JOIN clauses
        if source_op['op'] == 'JOIN':

            # Decompose JOIN variables
            left_table, right_table = source_op['args']['tables']
            join_column = source_op['args']['column']

            # Join of two tables
            new_table = CommandsEval._join(left_table, right_table, join_column)

            # Storage of new table
            CommandsEval.loaded_tables[table_name] = new_table

        elif source_op['op'] == 'SELECT':

            # Take SELECT procedure on its method
            new_table = CommandsEval._select(source_op['args'])

            # Storage of new table
            CommandsEval.loaded_tables[table_name] = new_table

    @staticmethod
    def _procedure(args):
        """ Creates a procedure -> a set of commands """

        # Store queries into dictionary of procedures, with given procedure name
        CommandsEval.procedures[args['procedure_name']] = args['queries']

    @staticmethod
    def _call(procedure_name):
        """ Executes a stored procedure """

        for query in CommandsEval.procedures[procedure_name]:
            CommandsEval.evaluate(query)

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

            args = ast['args']
            if op in CommandsEval.operators:
                func = CommandsEval.operators[op]
                return func(args)
            else:
                raise Exception(f"Unknown operator {op}")

        raise Exception('Undefined AST')

    @staticmethod
    def _alternate_operator(table, column, operator, value):
        """ Apply condition, based on given operator """

        if operator == '>':
            parameterized_table = table[table[column] > value]

        elif operator == '<':
            parameterized_table = table[table[column] < value]

        elif operator == '>=':
            parameterized_table = table[table[column] >= value]

        elif operator == '<=':
            parameterized_table = table[table[column] <= value]

        elif operator == '=':
            parameterized_table = table[table[column] == value]

        else:
            parameterized_table = table[table[column] != value]

        return parameterized_table

    @staticmethod
    def _join(left_table, right_table, join_column):
        """ Joins 2 tables """

        if isinstance(left_table, str) and isinstance(right_table, str):
            return CommandsEval.loaded_tables[left_table].join(CommandsEval.loaded_tables[right_table], on = join_column, lsuffix = 'left_'+join_column, rsuffix = 'right_'+join_column)