import csv
import os.path


class CSVHandler:
    """This class is used to manage csv files"""
    def __init__(self, path: str):
        """The constructor needs a parameter: path, which is the path where the program will save the csv file"""
        if type(path) != str:
            raise ValueError("The path parameter must be a string")
        self.field = ["Data", "Ora", "Totale_Pucce_Rilevate", "Totale_Pucce_Buone", "Totale_Pucce_Bruciate",
                      "Percentuale_Buone", "Percentuale_Bruciate"]
        self.path = path
        if not os.path.exists(self.path):
            try:
                with open(self.path, "w") as csv_file:
                    csv_writer = csv.DictWriter(csv_file, fieldnames=self.field)
                    csv_writer.writeheader()
            except Exception as e:
                print("")
                print(e)
                print("Exception Name: ", e.__class__.__name__)

    def write_data(self, dict_data: dict):
        """This method is used to write a line in the csv file, it accepts a parameter:
        dict_data, which is a dictionary with the data to be written to it"""
        if type(dict_data) != dict:
            raise ValueError("The dict_data argument must be a dictionary")
        if list(dict_data.keys()) != self.field:
            raise ValueError(
                'The given values do not match the fields of the class: '
                '["Data", "Ora", "Totale_Pucce_Rilevate", "Totale_Pucce_Buone", "Totale_Pucce_Bruciate", '
                '"Percentuale_Buone", "Percentuale_Bruciate"]')
        with open(self.path, "a") as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=self.field)
            csv_writer.writerow(dict_data)
