"""
utility functions for astroquery
"""

from astropy import units as u
from astroquery.simbad import Simbad
from astropy.coordinates import SkyCoord  

class astroQ:
    
    def __init__(self) :
        
        self.data = []

    def positionsbyname(self,string):
        """
        Return RA and DEC with astroquery name object
        """
        ra = 0
        dec = 0
        result_table = Simbad.query_object(string)
        c = SkyCoord(ra=result_table['RA'], dec=result_table['DEC'], unit=(u.deg, u.deg))
        ra = c.ra.deg[0]    # Hours
        dec = c.dec.deg[0]  # degrees
        return ra,dec
        
    def positionsbyname_deg(self,string):
        """
        Return RA(degrees) and DEC with astroquery name object
        """
        ra = 0
        dec = 0
        result_table = Simbad.query_object(string)
        c = SkyCoord(ra=result_table['RA'], dec=result_table['DEC'], unit=(u.deg, u.deg))
        ra = c.ra.deg[0] * 15    # degrees
        dec = c.dec.deg[0]       # degrees
        return ra,dec 