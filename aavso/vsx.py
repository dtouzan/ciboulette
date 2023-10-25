"""
AAVSO vsx class
https://www.aavso.org/
"""

__authors__ = ("Dominique Touzan","ciboulette module")
__contact__ = ("dtouzan@gmail.com","https://github.com/dtouzan/ciboulette")
__copyright__ = "MIT"
__date__ = "2023-10-24"
__version__= "1.0.0"

# Globals mods
import requests

# Astropy mods
from astropy.table import Table
from astropy import units as u
from astropy.coordinates import SkyCoord

# Users mods
from ciboulette.aavso.compoments import compoment

class vsx(compoment):
    """
    Class AAVSO VSX, create VSX table
    @NameID: name of AAVSO ID
    """

    def __init__(self, nameID):
        self.nameID = nameID
        self.read

    @property
    def read(self):
        """
        @return: TABLE of Variable
        """
        self.table

    @property
    def data(self):
        """
        @return: JSON data
        Source : https://www.aavso.org/direct-web-query-vsxvsp
        """
        if ' ' in self.nameID:
            nameID = self.nameID.replace(' ','%20')
        else:
            nameID = self.nameID

        url = "http://www.aavso.org/vsx/index.php"
        params = {}
        params['view']='api.object'
        params['format']='json'
        params['ident']=self.nameID
        response = requests.get(url,params=params)
        if (response.status_code > 400):
            return False
        else:
            return response.json()

    @property
    def table(self):
        """
        @return: data table
        """
        result = self.data['VSXObject']
        header = []
        value = []
        types = []
        for item in result:
            value.append(result[item])
            header.append(item)
            types.append('str')

        self.dataset = Table(names = header, dtype = types)
        self.dataset.add_row(value)

    @property
    def name(self):
        """
        @return: vsx name
        """
        if self.available:
            return self.dataset['Name'][0]
        else:
            return False
 
    @property
    def coordinates(self):
        """
        @return: vsx RA,DEC (degree,degree)
        """
        if self.available:
            return float(self.dataset['RA2000']), float(self.dataset['Declination2000'])
        else:
            return False
            
    @property
    def hourdegree(self):
        """
        @return: vsx RA,DEC (Hour,Degree)
        """
        if self.available:
            c = SkyCoord(ra=float(self.dataset['RA2000'])*u.degree, dec=float(self.dataset['Declination2000'])*u.degree)
            return c.ra.hour, c.dec.degree
        else:
            return False

    @property
    def epoch(self):
        """
        @return: vsx epoch
        """
        if self.available:
            return float(self.dataset['Epoch'][0])
        else:
            return False

    @property
    def magnitude(self):
        """
        @return: vsx magnitude maximum minimum
        """
        if self.available:
            min = float(self.dataset['MinMag'][0].split(' ')[0])
            max = float(self.dataset['MaxMag'][0].split(' ')[0])
            return max, min
        else:
            return False

    @property
    def AUID(self):
        """
        @return: vsx AUID
        """
        if self.available:
            return self.dataset['AUID'][0]
        else:
            return False

