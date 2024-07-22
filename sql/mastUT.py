"""
class mast UT for SQL interface

IN PROGRESS, DO NOT USED
"""

__authors__ = ("Dominique Touzan","ciboulette module")
__contact__ = ("dtouzan@gmail.com","https://github.com/dtouzan/ciboulette")
__copyright__ = "MIT"
__date__ = "2024-03-12"
__version__= "1.0.0"

# User mods
from ciboulette.sql import compoments, interface

class mast_UT1(interface.interfaces):

    def default(slef, observation_id: int):
        self.mast_default(observation_id, 'UT1', 'nefertiti3199-imx477', 1, 1, 0.030)

class mast_UT2(interface.interfaces):

    def defualt(slef, observation_id: int):
        self.mast_default(observation_id, 'UT2', 'taranis5370-imx477', 1, 1, 0.050)
