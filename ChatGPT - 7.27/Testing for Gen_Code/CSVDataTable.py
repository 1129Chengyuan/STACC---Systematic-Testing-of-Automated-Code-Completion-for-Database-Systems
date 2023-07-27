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
        # Check input: raise ValueError for invalid template or field_list
        if not isinstance(template, dict):
            raise TypeError("Template must be a proper dictionary")
        if field_list is not None and not all(isinstance(field, str) for field in field_list):
            raise TypeError("field_list must be a list with strings as elements")

        results = []

        # Open the CSV file
        with open(self.connect_info['directory'] + '/' + self.table_name, 'r') as csv_file:
            reader = csv.DictReader(csv_file)

            # Iterate through the rows in the CSV file
            for row in reader:
                # Check if the row matches the template
                is_match = True
                for key, value in template.items():
                    if row[key] != value:
                        is_match = False
                        break

                # If the row matches the template, process its fields
                if is_match:
                    fields_result = {}
                    if isinstance(field_list, list):  # if any fields specified in the field_list
                        for field in field_list:
                            if field in row:
                                fields_result[field] = row[field]
                        results.append(fields_result)
                    elif field_list == "*" or field_list is None:  # "*" retrieves all fields, None retrieves no fields
                        if field_list == "*": results.append(row)
                        elif field_list is None: results.append(None)

            return results if results else None  # return the matching records, or None if no matching records found
