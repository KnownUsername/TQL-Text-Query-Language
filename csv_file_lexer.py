"""
    Project: Countries_CSV-to-HTML-and-LaTeX-formats
    Purpose: Academical
    Description: Contains a class using lexer, to find fields on a csv file.

    Author: João Rodrigues
    Student No.: 16928

    Course: LESI
    Subject: Languages Processing
    College: IPCA
    Academic year: 2021/2022
"""

# Imports
from country import Country
from my_utils import slurp
import ply.lex as plex
import copy


class CountryLexer:
    """ Uses lexer, to find fields on a csv file. """

    # Tokens - defines different rules for regular expressions
    tokens = ("NEWLINE", "NFIELD", "QMFIELD", "COMMA", "EOF", "DUMMY")

    # States - Environment where tokens will be applied
    states = (
        ("header", "exclusive"),
        ("body", "exclusive"),
        ("comment", "exclusive")
    )


    def __init__(self, filename):
        """ Class constructor.

            It's assigned it filename and initialized lexer variable with None value.

            It's also initialized lists and auxiliar variables.
            Info for each variable, available on comment.
        """

        self.lexer = None
        self.filename = filename

        # Stores the state that precedes 'comment' state
        self.previous_state = None

        # Index of current column/field
        self.column_index = 0

        # Current country being read
        self.current_country = Country()

            # -  Data Structures - #

        # All countries read
        self.countries = []

    def process(self):
        """ Processes a csv file.
                - Reads it
                - Applies tokens' rules
                - Saves elements on a list (each line is an element)
        """

        # Reads a file content and saves it as string
        file = slurp(self.filename)

        # Initializes lexer variable
        self.lexer = plex.lex(module=self)

        # Introduces file's content on lexer
        self.lexer.input(file)
        # Start lexer on header state
        self.lexer.begin('header')

        # Tokens' processing
        for token in iter(self.lexer.token, None):
            pass


    #   --- Token Rules ---   #

    # Error manager
    def t_ANY_error(self, t):
        print(f"Unexpected tokens: {t.value[0:10]}")
        exit(1)


    #     ==> INITIAL <==
    def t_DUMMY(self, t):
        """ It's only defined, so that state INITIAL has a method associated to it.

            If this method is removed, the program won't run, because INITIAL needs to be defined.
            Being defined, means having any rule to work it, in this case, it's being used a method,
            where the regular expression doesn't matter, as this state is never used.

        """
        r'[-\w \']+'
        pass

    #   ###################   #

    #     ==>    HEADER    <==

    # Tokens starting with #
    def t_header_HASHTAG(self, t):
        r"\#[^,^\n]+"

        # Check if '#' is the 1st character on line
        # This occurs when column_index is 0, as it would be 1st field
        if self.column_index == 0:

            # Assign previous_state, so comment knows for where to return
            self.previous_state = 'header'

            # Change to comment state, to catch missing string on comment
            self.lexer.begin('comment')

        else:
            # Add value to list of columns
            self.current_country.columns.append(t.value)

    # Normal fields - No quotation marks
    def t_header_NFIELD(self, t):
        r'[-\w ()\'#]+'

        # Add value to list of columns
        self.current_country.columns.append(t.value)


    # Fields containing quotation marks
    def t_header_QMFIELD(self, t):
        r'"[^"]+"'

        # Add value to list of columns
        self.current_country.columns.append(t.value)

    # Commas
    def t_header_COMMA(self, t):
        r','

        # Index increment, to change column/field
        self.column_index += 1

    # New lines
    def t_header_NEWLINE(self, t):
        r'\n'

        # Reinitialize variable
        self.column_index = 0

        # Change to body state
        self.lexer.begin('body')

    #   ###################   #

    #    ==>    BODY    <==

    # Tokens starting with #
    def t_body_HASHTAG(self, t):
        r"\#[^,^\n]+"

        # Check if '#' is the 1st character on line
        # This occurs when column_index is 0, as it would be 1st field
        if self.column_index == 0:

            # Assign previous_state, so comment knows for where to return
            self.previous_state = 'body'

            # Change to comment state, to catch missing string on comment
            self.lexer.begin('comment')

        else:
            # Set value of a class attribute
            # ( Something close to this -> current_country.columns[column_index] = t.value )
            setattr(self.current_country, Country.columns[self.column_index], t.value)

    # Normal fields - No quotation marks
    def t_body_NFIELD(self, t):
        r'[-\w &()\'\.#]+'

        # Set value of a class attribute
        # ( Something close to this -> current_country.columns[column_index] = t.value )
        setattr(self.current_country, Country.columns[self.column_index], t.value)

    # Fields containing quotation marks
    def t_body_QMFIELD(self, t):
        r'"[^"]+"'

        # Remove " " on start and end of string
        modified_token = t.value[1:-1]
        # Set value of a class attribute
        # ( Something close to this -> current_country.columns[column_index] = t.value )
        setattr(self.current_country, Country.columns[self.column_index], modified_token)

    # Commas
    def t_body_COMMA(self, t):
        r','
        # Index increment, to change column/field
        self.column_index += 1

    # New lines
    def t_body_NEWLINE(self, t):
        r'\n'

        # Restart index value
        self.column_index = 0

        # Store read country
        self.countries.append(copy.deepcopy(self.current_country))

        # Set all class's variables to None
        self.current_country.clean()

    # End Of File
    def t_body_eof(self, t):
        """ Reaching EOF, it must be able to identify if last line is empty or a record.
            The process is done by checking if current object has values.

            An object with values is saved and gets its values to None after it.
            An object with no values is ignored.
        """

        # If current object is not empty, than it must be included on list
        if not self.current_country.is_empty():

            # Store read country
            self.countries.append(copy.deepcopy(self.current_country))

            # Set all class's variables to None
            self.current_country.clean()


    #    ==>    COMMENT    <==

    # Matches text on same line as found '#' character on a line comment.
    # Content is ignored.
    t_comment_ignore_comment = r"[^\n]+"

    # New lines
    def t_comment_NEWLINE(self, t):
        r"\n"

        # Returns to previous state
        self.lexer.begin(self.previous_state)
