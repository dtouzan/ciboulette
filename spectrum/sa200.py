"""
sa200 class

use specutils

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
    # Class for sa200 spectrum.
    def __init__(self, filename):
        self.s1d = Spectrum1D.read(filename)
        self.resolution = 200
        f = fits.open(filename)  
        self.header = f[0].header
        f.close() 
  
    @property
    def name(self):
        """
        @return:  A sting representing name
        """     
        return self.header['OBJNAME']

    @property
    def R(self):
        """
        @return:  A string representing resolution
        """     
        if 'SPE_RPOW' in self.header:
            c = self.header['SPE_RPOW']
        else:
            c = ''           
        return c   
    
    @property
    def observer(self):
        """
        @return:  A sting representing observer
        """     
        return self.header['OBSERVER']
    
    @property
    def date(self):
        """
        @return:  A sting representing date
        """     
        return self.header['DATE-OBS']    

    @property
    def instrument(self):
        """
        @return:  A sting representing instrument
        """     
        return self.header['BSS_INST']    

    @property
    def site(self):
        """
        @return:  A sting representing site
        """     
        return self.header['BSS_SITE']    

    @property
    def exposure(self):
        """
        @return:  A sting representing exposure time
        """     
        return self.header['EXPTIME']    

    @property
    def calibration_reference(self):
        """
        @return:  A sting representing calibration reference
        """     
        if 'O_CAL' in self.header:
            c = self.header['O_CAL']
        else:
            c = str(self.resolution)           
        return c   

    @property
    def longitude(self):
        """
        @return:  A sting representing longitude
        """     
        return self.header['GEO_LONG']    

    @property
    def latitude(self):
        """
        @return:  A sting representing latitude
        """     
        return self.header['GEO_LAT']    

    @property
    def elevation(self):
        """
        @return:  A sting representing elevation
        """     
        return self.header['GEO_ELEV']    
    
    @property
    def version(self):
        """
        @return:  A sting representing version
        """     
        return self.header['VERSION']    

    @property
    def JD(self):
        """
        @return:  A sting representing Julian Day
        """     
        time = Time(self.header['DATE-OBS'])
        return time.jd
    
    @property
    def title(self):
        """
        @return:  A sting representing title
        """     
        title_name = self.name + ' - ' + self.date + ' - R: ' + str(self.R) + ' / ' + self.calibration_reference
        return title_name
     
    @property
    def unit(self):
        """
        @return:  A sting representing unit
        """     
        return self.header['CDELT1']    

    def flux_value(self, atomic_line = 6562.8):
        """
        @return:  A string representing flux values
        """     
        return self.s1d.flux.value[int( (atomic_line - self.header['CRVAL1']) / self.unit)]

    @property
    def xlabel(self):
        """
        @return:  A sting representing x plot label
        """     
        label = r'$\lambda$[Ångström]'.format(self.s1d.spectral_axis.unit)
        return label
    
    @property
    def ylabel(self):
        """
        @return:  A sting representing y plot label
        """     
        label = 'Relative intensity'.format(self.s1d.flux.unit)
        return label
    
    @property
    def spectral_axis(self):
        """
        @return:  A table representing spectral axis
        """     
        return self.s1d.spectral_axis
    
    @property
    def flux(self):
        """
        @return:  A table representing flux values
        """     
        return self.s1d.flux
    
    def plotBD(self, axes):
        """
        @set:  Plot spectrum comic format
        """     
        axes.plot(self.s1d.spectral_axis, self.s1d.flux , linewidth=3, color = 'black',alpha=0.7)
        axes.plot(self.s1d.spectral_axis, self.s1d.flux , linewidth=1, color = 'cornflowerblue')

    def plot(self, axes):
        """
        @set:  Plot spectrum line width 2
        """     
        axes.plot(self.s1d.spectral_axis, self.s1d.flux , linewidth=2, color = 'black')
