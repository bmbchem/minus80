"""Class module that represents freezer data obtained from CSV file."""

# Standard library imports
import csv
import os
import pathlib

class FreezerData:
    """
    Class that represents freezer data obtained from CSV file.

    Attributes
    ----------
        csv_file : Path
            File path location of file that contains freezer data
        data : dictionary
            Dictionary of freezer data
    Methods
    -------
        parse_csv(ip, hostname=None): Parse CSV file and determines appropriate freezer data
    """

    def __init__(self, csv_file=None):

        if csv_file is None:
            csv_file = os.environ.get("FREEZER_CSV", pathlib.Path(__file__).resolve().parent.joinpath("freezer_info.csv"))
        self.__csv_file = csv_file
        self.__data = {}
    
    def get_data(self):
        """ Returns Freezer Data data attribute"""
        
        return self.__data
    
    def set_data(self, ordered_dict):
        """ Sets Freezer Data dat attribute"""
        
        self.__data = ordered_dict
    
    def parse_csv(self, ip, hostname=None):
        """Parses CSV file and populates data attribute with appropriate freezer 
        data based on ip and hostname parameters.

        Parameters:
            ip : str
                IP of the Raspberry Pi
            hostname : str, optional
                Hostname of the Raspberry Pi
        """

        ip = str(ip).strip()
        hostname = str(hostname).strip() if hostname is not None else ""

        try:
            with open(self.__csv_file, newline='', encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)
                if reader.fieldnames is None:
                    raise ValueError("CSV file is missing headers.")

                for row in reader:
                    if row.get("IP", "").strip() == ip:
                        self.__data = row
                        break
                    if hostname and row.get("Hostname", "").strip().lower() == hostname.lower():
                        self.__data = row
                        break
        except FileNotFoundError:
            raise FileNotFoundError(f"CSV file not found at {self.__csv_file}")

        if self.__data == {}:
            if hostname:
                raise ValueError(
                    f"No matching CSV record found for IP '{ip}' or hostname '{hostname}'."
                )
            raise ValueError(f"No matching CSV record found for IP '{ip}'.")
