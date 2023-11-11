"""
AAVSO vsx class
https://www.aavso.org/
"""

__authors__ = ("Dominique Touzan","ciboulette module")
__contact__ = ("dtouzan@gmail.com","https://github.com/dtouzan/ciboulette")
__copyright__ = "MIT"
__date__ = "2023-10-24"
__version__ = "1.0.0"
__citation__ = "The International Variable Star Index. Available: https://www.aavso.org/vsx/index.php?view=about.top\n"\
                "VSX - usage and policies. Available : https://www.aavso.org/vsx/index.php?view=about.top\n"\
                "AAVSO Data Usage Guidelines. Available: https://www.aavso.org/data-usage-guidelines.\n"\
                "We acknowledge with thanks the variable star observations from the AAVSO International Database contributed by observers worldwide and used in this research.\n"

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
        self._read

    @property
    def _read(self):
        """
        @return: TABLE of Variable
        """
        self._table

    @property
    def _data(self):
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
    def _table(self):
        """
        @return: data table
        """
        result = self._data['VSXObject']
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
            return self._header_query('Name')
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
            return False, False

    @property
    def magnitude(self):
        """
        @return: vsx magnitude maximum minimum
        """
        if self.available:
            min = float(self._header_query('MinMag').split(' ')[0])
            max = float(self._header_query('MaxMag').split(' ')[0])
            return max, min
        else:
            return False, False

    @property
    def AUID(self):
        """
        @return: vsx AUID
        """
        if self.available:
            return self._header_query('AUID')
        else:
            return False

    @property
    def variability_type(self):
        """
        @return: vsx VariabilityType
        """
        if self.available:
            return self._header_query('VariabilityType')
        else:
            return False

    @property
    def category(self):
        """
        @return: vsx Category
        """
        if self.available:
            return self._header_query('Category')
        else:
            return False

    @property
    def OID(self):
        """
        @return: vsx OID
        """
        if self.available:
            return self._header_query('OID')
        else:
            return False

    @property
    def constellation(self):
        """
        @return: vsx Constellation
        """
        if self.available:
            return self._header_query('Constellation')
        else:
            return False

    def header_value(self, header_name=''):
        """
        @return: vsx string representing dataset query header
        """
        return self._header_query(header_name)
    
    
    def _header_query(self, header_name=''):
        """
        @return:  A string representing dataset headers query
        """
        if header_name != '':
            if self.available:
                return self.dataset[header_name][0]
            else:
                return False
        else:
            return False

