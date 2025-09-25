"""
class for skychart application
"""


__authors__ = ("Dominique Touzan","ciboulette module")
__contact__ = ("dtouzan@gmail.com","https://github.com/dtouzan/ciboulette")
__copyright__ = "MIT"
__date__ = "2025-08-30"
__version__= "1.0.0"

from ciboulette.sql import interface

class Observationlist():

    def __init__(self, fileoutput='NewObsList.txt'):
        self.fileoutput = fileoutput     

    @property
    def get(self):
        """
        @Return: list for skymap
        """
        interfaces = interface.interfaces()
        return interfaces.skychart_values

    @property
    def file(self):
        """
        @Return: create file for skymap
        """
        interfaces = interface.interfaces()
        filename = interfaces.skychart_filename
        with open(filename, 'w') as file_skychart:
            for value in interfaces.skychart_values:
                print(f'{value}', file=file_skychart)
