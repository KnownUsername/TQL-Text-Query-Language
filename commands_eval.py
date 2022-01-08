import pandas as pd
import os.path

class CommandsEval:

    loaded_tables = {}

    @staticmethod
    def load(table_name, filename):
        """ Loads a table - Loads csv file to memory """

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
    def discard(table_name):
        """ Discards a table - removes from memory """

        # Table must be loaded - on tables' dictionary
        if table_name in CommandsEval.loaded_tables:
            # Removal of desired table
            del CommandsEval.loaded_tables[table_name]

        else:
            raise Exception('Table is not loaded')

    @staticmethod
    def show(table_name):
        """ Presents table on console"""

        # Table must be loaded - on tables' dictionary
        if table_name in CommandsEval.loaded_tables:
            print(CommandsEval.loaded_tables[table_name])
        return True

    @staticmethod
    def save(table_name, filename):
        """ Saves table on a csv file"""

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
        except:
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
