""" Defines a country structure, from the csv file.
    Each field represents a column. """
class Country:

    # Contains all fields' name (each column name)
    columns = []


    def clean(self):
        """  Changes the value of every field into None.
        This can be used, in order to reuse a variable"""
        for column in self.columns:
            setattr(self, column, None)

    def present(self):
        """ Prints object's corresponding columns to values, separated by tabs """
        for column in self.columns:
            print(f'{column}: {getattr(self, column)}\t')

    def is_empty(self):
        """ Checks if an object has all values at None"""
        for column in self.columns:

            # 1 existent value is enough to say it's not empty
            # Therefore, it's returned False
            if getattr(self, column):
                return False
        # If all values are empty, than it's considered empty
        # So true it's returned.
        return True
