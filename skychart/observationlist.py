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
        self.observations = Table()
        self.title = ''               # 32 digits
        self.ra = ''                  # 9 digits
        self.dec = ''                 # 8 digits
        self.label = ''               # 32 digits
        self.observation = ''         # 50 digits
        

    @property
    def create(self):
        """
        Return list for skymap
        """