import unittest
from tracemalloc_utils import clear_traces

class CombinedTests(unittest.TestCase):

    def setUp(self):
        try:
            with open("CSVDataTable.py") as f:
                code = compile(f.read(), "file.py", "exec")
        except SyntaxError:
            self.fail("Syntax error in file.py")
        clear_traces()
        blank = []
        import CSVDataTable
        self.managers_table = CSVDataTable.CSVDataTable('managers.csv', blank, ['playerID'])
        self.parks_table = CSVDataTable.CSVDataTable('Parks.csv', blank, ['park.key'])
        self.teams_table = CSVDataTable.CSVDataTable('TeamsFranchises.csv', blank, ['franchID'])

    def test_invalid_template_field(self):
        template = {'invalid': 'value'}
        with self.assertRaises(KeyError):
            results = self.managers_table.find_by_template(template)

    def test_multiple_matches(self):
        template = {'yearID': '2000'}
        results = self.managers_table.find_by_template(template)
        self.assertGreater(len(results), 1)
        for result in results:
            self.assertEqual(result['yearID'], '2000')

    def test_empty_field_list(self):
        template = {'playerID': 'aaronha01'}
        field_list = []
        results = self.managers_table.find_by_template(template, field_list)
        self.assertEqual(len(results), 0)
        self.assertEqual(results, [])

    def test_empty_field_list_multiple(self):
        template = {'yearID': '2000'}
        field_list = []
        results = self.managers_table.find_by_template(template, field_list)
        self.assertGreater(len(results), 0)
        for result in results:
            self.assertEqual(result, {})

    def test_extra_template_fields(self):
        template = {'playerID': 'aaronha01', 'extra': 'ignore'}
        results = self.managers_table.find_by_template(template)
        expected = []
        self.assertEqual(results, expected)

    def test_park_test_find_by_template_one_match(self):
        template = {'park.key': 'ATL03'}
        results = self.parks_table.find_by_template(template)
        expected = [
            {'park.key': 'ATL03', 'park.name': 'Suntrust Park', 'park.alias': '', 'city': 'Atlanta', 'state': 'GA',
             'country': 'US'}]
        self.assertEqual(results, expected)

    def test_find_by_template_no_matches(self):
        template = {'park.key': 'XXX'}
        results = self.parks_table.find_by_template(template)
        expected = []
        self.assertEqual(results, expected)

    def test_find_by_template_multiple_matches(self):
        template = {'state': 'OH'}
        results = self.parks_table.find_by_template(template)
        expected = [{'city': 'Canton',
                     'country': 'US',
                     'park.alias': 'Pastime Park',
                     'park.key': 'CAN01',
                     'park.name': 'Mahaffey Park',
                     'state': 'OH'},
                    {'city': 'Canton',
                     'country': 'US',
                     'park.alias': '',
                     'park.key': 'CAN02',
                     'park.name': 'Pastime Park',
                     'state': 'OH'},
                    {'city': 'Cincinnati',
                     'country': 'US',
                     'park.alias': 'Union Cricket Club Grounds',
                     'park.key': 'CIN01',
                     'park.name': 'Lincoln Park Grounds',
                     'state': 'OH'},
                    {'city': 'Cincinnati',
                     'country': 'US',
                     'park.alias': '',
                     'park.key': 'CIN02',
                     'park.name': 'Avenue Grounds',
                     'state': 'OH'},
                    {'city': 'Cincinnati',
                     'country': 'US',
                     'park.alias': '',
                     'park.key': 'CIN03',
                     'park.name': 'Bank Street Grounds',
                     'state': 'OH'},
                    {'city': 'Cincinnati',
                     'country': 'US',
                     'park.alias': '',
                     'park.key': 'CIN04',
                     'park.name': 'League Park I',
                     'state': 'OH'},
                    {'city': 'Cincinnati',
                     'country': 'US',
                     'park.alias': '',
                     'park.key': 'CIN05',
                     'park.name': 'League Park II',
                     'state': 'OH'},
                    {'city': 'Cincinnati',
                     'country': 'US',
                     'park.alias': 'League Park III',
                     'park.key': 'CIN06',
                     'park.name': 'Palace of the Fans',
                     'state': 'OH'},
                    {'city': 'Cincinnati',
                     'country': 'US',
                     'park.alias': 'Redland Field',
                     'park.key': 'CIN07',
                     'park.name': 'Crosley Field',
                     'state': 'OH'},
                    {'city': 'Cincinnati',
                     'country': 'US',
                     'park.alias': 'Riverfront Stadium',
                     'park.key': 'CIN08',
                     'park.name': 'Cinergy Field',
                     'state': 'OH'},
                    {'city': 'Cincinnati',
                     'country': 'US',
                     'park.alias': '',
                     'park.key': 'CIN09',
                     'park.name': 'Great American Ballpark',
                     'state': 'OH'},
                    {'city': 'Cleveland',
                     'country': 'US',
                     'park.alias': '',
                     'park.key': 'CLE01',
                     'park.name': 'National Association Grounds',
                     'state': 'OH'},
                    {'city': 'Cleveland',
                     'country': 'US',
                     'park.alias': 'Kennard Street Park',
                     'park.key': 'CLE02',
                     'park.name': 'League Park I',
                     'state': 'OH'},
                    {'city': 'Cleveland',
                     'country': 'US',
                     'park.alias': 'American Association Park',
                     'park.key': 'CLE03',
                     'park.name': 'League Park II',
                     'state': 'OH'},
                    {'city': 'Cleveland',
                     'country': 'US',
                     'park.alias': 'Players League Park',
                     'park.key': 'CLE04',
                     'park.name': 'Brotherhood Park',
                     'state': 'OH'},
                    {'city': 'Cleveland',
                     'country': 'US',
                     'park.alias': 'National League Park III',
                     'park.key': 'CLE05',
                     'park.name': 'League Park III',
                     'state': 'OH'},
                    {'city': 'Cleveland',
                     'country': 'US',
                     'park.alias': 'Dunn Field',
                     'park.key': 'CLE06',
                     'park.name': 'League Park IV',
                     'state': 'OH'},
                    {'city': 'Cleveland',
                     'country': 'US',
                     'park.alias': 'Municipal Stadium',
                     'park.key': 'CLE07',
                     'park.name': 'Cleveland Stadium',
                     'state': 'OH'},
                    {'city': 'Cleveland',
                     'country': 'US',
                     'park.alias': 'Jacobs Field',
                     'park.key': 'CLE08',
                     'park.name': 'Progressive Field',
                     'state': 'OH'},
                    {'city': 'Cleveland',
                     'country': 'US',
                     'park.alias': '',
                     'park.key': 'CLE09',
                     'park.name': 'Cedar Avenue Driving Park',
                     'state': 'OH'},
                    {'city': 'Collinwood',
                     'country': 'US',
                     'park.alias': '',
                     'park.key': 'CLL01',
                     'park.name': 'Euclid Beach Park',
                     'state': 'OH'},
                    {'city': 'Columbus',
                     'country': 'US',
                     'park.alias': '',
                     'park.key': 'COL01',
                     'park.name': 'Recreation Park I',
                     'state': 'OH'},
                    {'city': 'Columbus',
                     'country': 'US',
                     'park.alias': '',
                     'park.key': 'COL02',
                     'park.name': 'Recreation Park II',
                     'state': 'OH'},
                    {'city': 'Columbus',
                     'country': 'US',
                     'park.alias': '',
                     'park.key': 'COL03',
                     'park.name': 'Neil Park I',
                     'state': 'OH'},
                    {'city': 'Columbus',
                     'country': 'US',
                     'park.alias': '',
                     'park.key': 'COL04',
                     'park.name': 'Neil Park II',
                     'state': 'OH'},
                    {'city': 'Dayton',
                     'country': 'US',
                     'park.alias': '',
                     'park.key': 'DAY01',
                     'park.name': 'Fairview Park',
                     'state': 'OH'},
                    {'city': 'Geauga Lake',
                     'country': 'US',
                     'park.alias': "Beyerle's Park",
                     'park.key': 'GEA01',
                     'park.name': 'Geauga Lake Grounds',
                     'state': 'OH'},
                    {'city': 'Geauga Lake',
                     'country': 'US',
                     'park.alias': "Beyerle's Park",
                     'park.key': 'NEW03',
                     'park.name': 'Geauga Lake Grounds',
                     'state': 'OH'},
                    {'city': 'Cincinnati',
                     'country': 'US',
                     'park.alias': 'Pendleton Park',
                     'park.key': 'PEN01',
                     'park.name': 'East End Park',
                     'state': 'OH'},
                    {'city': 'Toledo',
                     'country': 'US',
                     'park.alias': '',
                     'park.key': 'TOL01',
                     'park.name': 'League Park',
                     'state': 'OH'},
                    {'city': 'Toledo',
                     'country': 'US',
                     'park.alias': '',
                     'park.key': 'TOL02',
                     'park.name': 'Tri-State Fair Grounds',
                     'state': 'OH'},
                    {'city': 'Toledo',
                     'country': 'US',
                     'park.alias': '',
                     'park.key': 'TOL03',
                     'park.name': 'Speranza Park',
                     'state': 'OH'},
                    {'city': 'Toledo',
                     'country': 'US',
                     'park.alias': '',
                     'park.key': 'TOL04',
                     'park.name': 'Armory Park',
                     'state': 'OH'}]
        self.assertEqual(results, expected)

    def test_find_by_template_with_field_list(self):
        template = {'state': 'OH'}
        field_list = ['park.key', 'park.name']
        results = self.parks_table.find_by_template(template, field_list)
        expected = [{'park.key': 'CAN01', 'park.name': 'Mahaffey Park'},
                    {'park.key': 'CAN02', 'park.name': 'Pastime Park'},
                    {'park.key': 'CIN01', 'park.name': 'Lincoln Park Grounds'},
                    {'park.key': 'CIN02', 'park.name': 'Avenue Grounds'},
                    {'park.key': 'CIN03', 'park.name': 'Bank Street Grounds'},
                    {'park.key': 'CIN04', 'park.name': 'League Park I'},
                    {'park.key': 'CIN05', 'park.name': 'League Park II'},
                    {'park.key': 'CIN06', 'park.name': 'Palace of the Fans'},
                    {'park.key': 'CIN07', 'park.name': 'Crosley Field'},
                    {'park.key': 'CIN08', 'park.name': 'Cinergy Field'},
                    {'park.key': 'CIN09', 'park.name': 'Great American Ballpark'},
                    {'park.key': 'CLE01', 'park.name': 'National Association Grounds'},
                    {'park.key': 'CLE02', 'park.name': 'League Park I'},
                    {'park.key': 'CLE03', 'park.name': 'League Park II'},
                    {'park.key': 'CLE04', 'park.name': 'Brotherhood Park'},
                    {'park.key': 'CLE05', 'park.name': 'League Park III'},
                    {'park.key': 'CLE06', 'park.name': 'League Park IV'},
                    {'park.key': 'CLE07', 'park.name': 'Cleveland Stadium'},
                    {'park.key': 'CLE08', 'park.name': 'Progressive Field'},
                    {'park.key': 'CLE09', 'park.name': 'Cedar Avenue Driving Park'},
                    {'park.key': 'CLL01', 'park.name': 'Euclid Beach Park'},
                    {'park.key': 'COL01', 'park.name': 'Recreation Park I'},
                    {'park.key': 'COL02', 'park.name': 'Recreation Park II'},
                    {'park.key': 'COL03', 'park.name': 'Neil Park I'},
                    {'park.key': 'COL04', 'park.name': 'Neil Park II'},
                    {'park.key': 'DAY01', 'park.name': 'Fairview Park'},
                    {'park.key': 'GEA01', 'park.name': 'Geauga Lake Grounds'},
                    {'park.key': 'NEW03', 'park.name': 'Geauga Lake Grounds'},
                    {'park.key': 'PEN01', 'park.name': 'East End Park'},
                    {'park.key': 'TOL01', 'park.name': 'League Park'},
                    {'park.key': 'TOL02', 'park.name': 'Tri-State Fair Grounds'},
                    {'park.key': 'TOL03', 'park.name': 'Speranza Park'},
                    {'park.key': 'TOL04', 'park.name': 'Armory Park'}]
        self.assertEqual(results, expected)

    def test_find_by_template_one_match(self):
        template = {"franchID": "BOS"}
        expected = [{'franchID': 'BOS', 'franchName': 'Boston Red Sox', 'active': 'Y', 'NAassoc': ''}]
        actual = self.teams_table.find_by_template(template)
        self.assertEqual(actual, expected)

    def test_franch_find_by_template_multiple_matches(self):
        template = {"active": "Y"}
        field_list = ["franchID", "franchName"]
        expected = [{'franchID': 'ANA', 'franchName': 'Los Angeles Angels of Anaheim'},
                    {'franchID': 'ARI', 'franchName': 'Arizona Diamondbacks'},
                    {'franchID': 'ATL', 'franchName': 'Atlanta Braves'},
                    {'franchID': 'BAL', 'franchName': 'Baltimore Orioles'},
                    {'franchID': 'BOS', 'franchName': 'Boston Red Sox'},
                    {'franchID': 'CHC', 'franchName': 'Chicago Cubs'},
                    {'franchID': 'CHW', 'franchName': 'Chicago White Sox'},
                    {'franchID': 'CIN', 'franchName': 'Cincinnati Reds'},
                    {'franchID': 'CLE', 'franchName': 'Cleveland Indians'},
                    {'franchID': 'COL', 'franchName': 'Colorado Rockies'},
                    {'franchID': 'DET', 'franchName': 'Detroit Tigers'},
                    {'franchID': 'FLA', 'franchName': 'Florida Marlins'},
                    {'franchID': 'HOU', 'franchName': 'Houston Astros'},
                    {'franchID': 'KCR', 'franchName': 'Kansas City Royals'},
                    {'franchID': 'LAD', 'franchName': 'Los Angeles Dodgers'},
                    {'franchID': 'MIL', 'franchName': 'Milwaukee Brewers'},
                    {'franchID': 'MIN', 'franchName': 'Minnesota Twins'},
                    {'franchID': 'NYM', 'franchName': 'New York Mets'},
                    {'franchID': 'NYY', 'franchName': 'New York Yankees'},
                    {'franchID': 'OAK', 'franchName': 'Oakland Athletics'},
                    {'franchID': 'PHI', 'franchName': 'Philadelphia Phillies'},
                    {'franchID': 'PIT', 'franchName': 'Pittsburgh Pirates'},
                    {'franchID': 'SDP', 'franchName': 'San Diego Padres'},
                    {'franchID': 'SEA', 'franchName': 'Seattle Mariners'},
                    {'franchID': 'SFG', 'franchName': 'San Francisco Giants'},
                    {'franchID': 'STL', 'franchName': 'St. Louis Cardinals'},
                    {'franchID': 'TBD', 'franchName': 'Tampa Bay Rays'},
                    {'franchID': 'TEX', 'franchName': 'Texas Rangers'},
                    {'franchID': 'TOR', 'franchName': 'Toronto Blue Jays'},
                    {'franchID': 'WSN', 'franchName': 'Washington Nationals'}]
        actual = self.teams_table.find_by_template(template, field_list)
        self.assertEqual(actual, expected)

    def test_franch_template_no_matches(self):
        template = {"franchID": "AAA"}
        expected = []
        actual = self.teams_table.find_by_template(template)
        self.assertEqual(actual, expected)

    def test_find_by_template_missing_field(self):
        template = {"notAField": "value"}
        expected = []
        actual = self.teams_table.find_by_template(template)
        print(actual)
        self.assertEqual(actual, expected)

# if __name__ == '__main__':
#     unittest.main()

