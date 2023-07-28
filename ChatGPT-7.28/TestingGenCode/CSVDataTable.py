from BaseDataTable import BaseDataTable
import copy
import csv


class CSVDataTable(BaseDataTable):
    """
    The implementation classes (XXXDataTable) for CSV database, relational, etc. with extend the
    base class and implement the abstract methods.
    """

    def __init__(self, table_name, connect_info, key_columns):
        """

        :param table_name: Logical name of the table.
        :param connect_info: Dictionary of parameters necessary to connect to the data.
        :param key_columns: List, in order, of the columns (fields) that comprise the primary key.
        """
        self.table_name = table_name
        self.connect_info = connect_info
        self.key_columns = key_columns
        # pass

#CODE BELOW!

    def find_by_template(self, template, field_list=None):
        globalVar = {}
        local = {'template':template,'field_list':field_list}
        return exec(self.connect_info, globalVar, local)
        # pass