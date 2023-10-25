"""
AAVSO compoment class
"""

__authors__ = ("Dominique Touzan","ciboulette module")
__contact__ = ("dtouzan@gmail.com","https://github.com/dtouzan/ciboulette")
__copyright__ = "MIT"
__date__ = "2023-10-24"
__version__= "1.0.0"

# Globals mods

# Astropy mods
from astropy.table import Table

class compoment():

    """
    Class AAVSO compoment
    @NameID: name of AAVSO ID
    """

    def __init__(self):
        self.dataset = Table()

    @property
    def available(self):
        if len(self.dataset) > 0:
            return True
        else:
            return False

    @property
    def observations(self):
        """
        @return: table data
        """
        if self.available:
            return self.dataset
        else:
            return False

    @property
    def header_names(self):
        """
        @return:  A list representing dataset headers
        """
        return self.dataset.colnames
