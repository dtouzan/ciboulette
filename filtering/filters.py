"""
Filters class

Baader SDSS/SLOAN u' photometric https://www.baader-planetarium.com/en/sloansdss-u%27-filter-%E2%80%93-photometrisch.html
Baader SDSS/SLOAN g' photometric https://www.baader-planetarium.com/en/sloansdss-g%27-filter-%E2%80%93-photometrisch.html
Baader SDSS/SLOAN r' photometric https://www.baader-planetarium.com/en/sloansdss-r%27-filter-%E2%80%93-photometrisch.html
Baader Bessel V photometric https://www.baader-planetarium.com/en/filters/photometric-filters/ubvri-bessel-v-filter-%E2%80%93-photometrisch.html


"""

from astropy import units as u
import numpy as np
from scipy.interpolate import make_interp_spline

class Filters(object):
    # Class for Element filters.
    def __init__(self):
        self.spectral_axis = []
        self.flux = []
        self.name = ''
        self.label = ''
        self.color = 'black'
    
    def plotBD(self, axes):
        axes.fill_between(self.spectral_axis,self.flux, color = self.color, alpha=0.1)
        axes.plot(self.spectral_axis, self.flux, linewidth=3, color = self.color,alpha=1)
        axes.plot(self.spectral_axis, self.flux, linewidth=5, color = 'white',alpha=0.7)
        axes.annotate(f'{self.label}', xy=(self.spectral_axis[1], 0), xytext=(0,5), textcoords='offset points', rotation=0, va='bottom', ha='left', annotation_clip=False, fontsize=6, color=self.color, weight='bold')

        
class SDSS_Sloan_g(Filters):
    # Class SDSS/Sloan g' filter 
    def __init__(self):
        self.set_filter()
    
    def set_filter(self):
        self.spectral_axis = [3950, 4010, 4100, 4200, 4310, 4400, 4500, 4600, 4800, 5000, 5100, 5200, 5300, 5400, 5500, 5595, 5600]
        self.flux = [0, 0.9, 0.92, 0.96, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0.98, 0]
        self.name = "Baader SLOAN/SDSS g' photometric"
        self.label = "SLOAN/SDSS g'"
        self.color = 'cornflowerblue'       

class SDSS_Sloan_r(Filters):
    # Class SDSS/Sloan r' filter 
    def __init__(self):
        self.set_filter()
    
    def set_filter(self):
        self.spectral_axis = [5595, 5610, 6995, 7020]
        self.flux = [0, 1, 1, 0]
        self.name = "Baader SLOAN/SDSS r' photometric"
        self.label = "SLOAN/SDSS r'"
        self.color = 'indianred'

class SDSS_Sloan_u(Filters):
    # Class SDSS/Sloan u' filter 
    def __init__(self):
        self.set_filter()
    
    def set_filter(self):
        self.spectral_axis = [3195, 3200, 3300, 3400, 3500, 3600, 3800, 3900]
        self.flux = [0, 0.84, 0.86, 0.83, 0.82, 0.78, 0.45, 0]
        self.name = "Baader SLOAN/SDSS u' photometric"
        self.label = "SLOAN/SDSS u'"
        self.color = 'violet'

class Bessel_V(Filters):
    # Class UBVRI Bessel V filter 
    def __init__(self):
        self.set_filter()
    
    def set_filter(self):
        self.spectral_axis = [4800, 4900, 5000, 5100, 5200, 5400, 5600, 5800, 6000, 6200, 6400, 6600, 6800]
        self.flux = [0, 0.35, 0.70, 0.85, 0.93, 0.905, 0.815, 0.66, 0.45, 0.25, 0.15, 0.04, 0]
        self.name = "Baader Bessel V photometric"
        self.label = "Bessel V"
        self.color = 'green'

    def plotBD(self, axes):
        X_Y_Spline = make_interp_spline(self.spectral_axis, self.flux)
        X_ = np.linspace(min(self.spectral_axis), max(self.spectral_axis), 100)
        Y_ = X_Y_Spline(X_)
        axes.fill_between(self.spectral_axis,self.flux, color = self.color, alpha=0.1)
        axes.plot(X_, Y_, linewidth=3, color = self.color,alpha=1)
        axes.plot(X_, Y_, linewidth=5, color = 'white',alpha=0.7)
        axes.annotate(f'{self.label}', xy=(self.spectral_axis[1], 0), xytext=(0,5), textcoords='offset points', rotation=0, va='bottom', ha='left', annotation_clip=False, fontsize=6, color=self.color, weight='bold')
