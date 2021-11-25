"""
sa200 class

Header ISIS V6.1.1
SIMPLE  =                    T / File does conform to FITS standard   
CRVAL1  =                  -32 / Coordinate at reference pixel                  
CDELT1  =                    1 / Coordinate increment                           
VERSION = '           '        / Software version                               
OBJNAME = '         '          / Current name of the object                     
DATE-OBS= '                  ' / Date of observation start                     
EXPTIME =                      / [s] Total time of exposure                     
EXPTIME2= '        '           / Exposure decomposition                         
BSS_INST= '        '           / Instrument                                 
BSS_SITE= '        '           / Observation site                               
OBSERVER= '        '                                                   
CUNIT1  = 'Angstrom'           / Wavelength unit                                
CTYPE1  = 'Wavelength'         / Axis type                                      
O_CAL   = '        '           / Calibration object                             
Q_CAL   = '0       '           / Quality flag 4-excellent                       
CRPIX1  =                    1 / Reference pixel                                
BSS_VHEL=                    0 / [km/s] Heliocentric speed                      
BSS_COSM= '        '                                                            
BSS_TELL= '        '                                                            
BSS_NORM= '        '                                                            
SPE_RPOW=                      / Spectral resolution power                      
JD-OBS  =                    0 / JD start observation                           
JD-MID  =                    0 / JD mid observation                             
JD-HEL  =                    0 / JD heliocentric mid-obs                        
GEO_LONG=                      / Obs. geographic longitude                      
GEO_LAT =                      / Obs. geographic latitude                       
GEO_ELEV=                      / Obs. geographic elevation        
"""

from astropy.io import fits
from astropy.table import Table
from astropy import units as u
from astropy.coordinates import SkyCoord
import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import quantity_support
from specutils import Spectrum1D
from astropy.time import Time


class SA200(object):
    """
    Class for sa200 spectrum.
    """
    def __init__(self, filename):
        self.s1d = Spectrum1D.read(filename)
        self.resolution = 200
        f = fits.open(filename)  
        self.data = f[0].data 
        self.header = f[0].header
        f.close() 
        #Serie de balmer
        self.Ha = 6562.10
        self.Hb = 4861.32
        self.Hg = 4340.46
        self.Hd = 4101.73
        #
        self.Mg = 5714
        # Doublet du sodium
        self.NaI = 5889.950
        self.NaII = 5895.924 
        #
        self.SiIIa = 6347.1
        self.SiIIb = 6371.4
  
    @property
    def name(self):
        """
        Return resolution
        """
        return self.header['OBJNAME']

    @property
    def R(self):
        """
        Return resolution
        """
        return self.header['SPE_RPOW']
    
    @property
    def observer(self):
        """
        Return observer
        """
        return self.header['OBSERVER']
    
    @property
    def date(self):
        """
        Return date observation
        """
        return self.header['DATE-OBS']    

    @property
    def instrument(self):
        """
        Return instrum                      
        """
        return self.header['BSS_INST']    

    @property
    def site(self):
        """
        Return site                      
        """
        return self.header['BSS_SITE']    

    @property
    def exposure(self):
        """
        Return exposure
        """
        return self.header['EXPTIME']    

    @property
    def calibration_reference(self):
        """
        Return start calibration reference 
        """
        if 'O_CAL' in self.header:
            c = self.header['O_CAL']
        else:
            c = str(self.resolution)           
        return c   

    @property
    def longitude(self):
        """
        Return site longitude
        """
        return self.header['GEO_LONG']    

    @property
    def latitude(self):
        """
        Return site latitude 
        """
        return self.header['GEO_LAT']    

    @property
    def elevation(self):
        """
        Return site latitude 
        """
        return self.header['GEO_ELEV']    
    
    @property
    def version(self):
        """
        Return software version
        """
        return self.header['VERSION']    

    @property
    def JD(self):
        """
        Return Julian Day
        """
        time = Time(self.header['DATE-OBS'])
        return time.jd
    
    @property
    def title(self):
        """
        Return title of spectrum plot
        """
        title_name = self.name + ' - ' + self.date + ' - R: ' + str(self.R) + ' / ' + self.calibration_reference
        return title_name
     
    @property
    def unit(self):
        """
        Return resolution of spectrum plot
        """
        return self.header['CDELT1']    
