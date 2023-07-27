# Import package to enable defining abstract classes in Python.
# Do not worry about understanding abstract base classes. This is just a class that defines
# some methods that subclasses must implement.
from abc import ABC, abstractmethod

import logging

class BaseDataTable(ABC):
    """
    The implementation classes (XXXDataTable) for CSV database, relational, etc. will extend the
    base class and implement the abstract methods.
    """

    def __init__(self, table_name, connect_info, key_columns=None, debug=True):
        """

        :param table_name: Name of the table. Subclasses interpret the exact meaning of table_name.
        :param connect_info: Dictionary of parameters necessary to connect to the data. See examples in subclasses.
        :param key_columns: List, in order, of the columns (fields) that comprise the primary key.
            A primary key is a set of columns whose values are unique and uniquely identify a row. For Appearances,
            the columns are ['playerID', 'teamID', 'yearID']
        :param debug: If true, print debug messages.
        """
        self._table_name = table_name
        self._connect_info = connect_info
        self._key_columns = key_columns
        self._debug = debug

    @abstractmethod
    def find_by_template(self, template, field_list=None, limit=None, offset=None, order_by=None):
        """

        :param template: A dictionary of the form { "field1" : value1, "field2": value2, ...}. The function will return
            a derived table containing the rows that match the template.
        :param field_list: A list of requested fields of the form, ['fielda', 'fieldb', ...]
        :param limit: Do not worry about this for now.
        :param offset: Do not worry about this for now.
        :param order_by: Do not worry about this for now.
        :return: A derived table containing the computed rows.
        """
        pass
