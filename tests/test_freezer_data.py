# Standard library imports
from collections import OrderedDict
import csv
import pathlib
import unittest
from unittest import mock
from unittest.mock import Mock
from unittest.mock import patch, call

# Local application imports
from app.FreezerData import FreezerData

class TestEmail(unittest.TestCase):
    """Test methods from FreezerData Class"""

    def test_parse_csv(self):
        """Tests FreezerData parse of CSV test file"""

        # Test data
        csv_file = pathlib.Path.cwd().joinpath("tests", "freezer_test.csv")
        ip = "92.168.1.100"

        # Create FreezerData object
        freezer_data = FreezerData(csv_file)

        # Parse freezer data
        freezer_data.parse_csv(ip)

        # Test result of parse
        od = OrderedDict([('Freezer Number', '3'), 
            ('Department', 'Chemistry'), ('PI', 'Person3'), 
            ('Email', 'minus80-Person3@chem.umass.edu'), 
            ('MFG', 'Thermo Fisher'), ('Model Number', 'TSU 500D'), 
            ('Location', 'LGRT 3'), ('Jack Number', ''), 
            ('IP', '92.168.1.100'), ('Hostname', 'minus80-Person3-1'), 
            ('MAC', 'aa:bb:cc:dd:ee:ff'), ('Comments', ''), (None, [''])])
        self.assertEqual(freezer_data.get_data(), od)

    def test_parse_csv_falls_back_to_hostname(self):
        """Tests FreezerData parse of CSV using hostname fallback."""

        csv_file = pathlib.Path.cwd().joinpath("tests", "freezer_test.csv")
        hostname = "minus80-Person3-1"

        freezer_data = FreezerData(csv_file)
        freezer_data.parse_csv("", hostname)

        self.assertEqual(freezer_data.get_data()["IP"], "92.168.1.100")
        self.assertEqual(freezer_data.get_data()["Hostname"], hostname)

    def test_parse_csv_raises_for_unknown_ip(self):
        """Tests FreezerData parse raises a ValueError for unknown IP."""

        csv_file = pathlib.Path.cwd().joinpath("tests", "freezer_test.csv")
        freezer_data = FreezerData(csv_file)

        with self.assertRaises(ValueError):
            freezer_data.parse_csv("192.0.2.1")

if __name__ == "__main__":
    unittest.main()