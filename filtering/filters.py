"""
Filters class

Baader SDSS/SLOAN u' photometric https://www.baader-planetarium.com/en/sloansdss-u%27-filter-%E2%80%93-photometrisch.html
Baader SDSS/SLOAN g' photometric https://www.baader-planetarium.com/en/sloansdss-g%27-filter-%E2%80%93-photometrisch.html
Baader SDSS/SLOAN r' photometric https://www.baader-planetarium.com/en/sloansdss-r%27-filter-%E2%80%93-photometrisch.html
Baader SDSS/SLOAN i' photometric https://www.baader-planetarium.com/en/sloansdss-i%27-filter-%E2%80%93-photometrisch.html
Baader SDSS/SLOAN z-s' photometric https://www.baader-planetarium.com/en/sloansdss-z-s%27-filter-%E2%80%93-photometrisch.html
Baader SDSS/SLOAN y' photometric https://www.baader-planetarium.com/en/sloansdss-y%27-filter-%E2%80%93-photometrisch.html

Baader Bessel U photometric https://www.baader-planetarium.com/en/filters/photometric-filters/ubvri-bessel-u-filter-%E2%80%93-photometrisch.html
Baader Bessel B photometric https://www.baader-planetarium.com/en/filters/photometric-filters/ubvri-bessel-b-filter-%E2%80%93-photometrisch.html
Baader Bessel V photometric https://www.baader-planetarium.com/en/filters/photometric-filters/ubvri-bessel-v-filter-%E2%80%93-photometrisch.html
Baader Bessel R photometric https://www.baader-planetarium.com/en/filters/photometric-filters/ubvri-bessel-r-filter-%E2%80%93-photometrisch.html
Baader Bessel I photometric https://www.baader-planetarium.com/en/filters/photometric-filters/ubvri-bessel-i-filter-%E2%80%93-photometrisch.html
Baader Bessel I photometric https://www.baader-planetarium.com/en/baader-h-alpha-35nm-ccd-filter.html
Baader RGB B  filter https://www.baader-planetarium.com/en/baader-rgb-b-filter-%E2%80%93-cmos-optimized.html
Baader RGB G  filter https://www.baader-planetarium.com/en/baader-rgb-g-filter-%E2%80%93-cmos-optimized.html
Baader RGB R  filter https://www.baader-planetarium.com/en/baader-rgb-r-filter-%E2%80%93-cmos-optimized.html

spectral_axis: Angstrom
flux: percent

"""

from astropy import units as u
import numpy as np
from scipy.interpolate import make_interp_spline, interp1d

class Filters(object):
    # Class for Element filters.
    def __init__(self):
        self.spectral_axis = []
        self.flux = []
        self.name = ''
        self.label = ''
        self.color = 'black'
        self.x = []
        self.y = []
    
    def plotBD(self, axes):
        axes.fill_between(self.x,self.y, color = self.color, alpha=0.1)
        axes.plot(self.x,self.y, linewidth=3, color = self.color,alpha=0.9)
        axes.plot(self.x,self.y, linewidth=5, color = 'white',alpha=0.5)
        x_annotate = self.x[0] + ((self.x[len(self.x)-1] - self.x[0]) / 2)
        axes.annotate(f'{self.label}', xy=(x_annotate, 0), xytext=(0,5), textcoords='offset points', rotation=0, va='bottom', ha='left', annotation_clip=False, fontsize=8, color=self.color, weight='bold', alpha=0.9)

    def make_XY(self,name = ''):
        if name == 'make_interp_spline':
            X_Y_Spline = make_interp_spline(self.spectral_axis, self.flux)
            self.x = np.linspace(min(self.spectral_axis), max(self.spectral_axis), 500)
            self.y = X_Y_Spline(self.x)
        if name == 'interp1d':
            X_Y_Spline = interp1d(self.spectral_axis, self.flux)
            self.x = np.linspace(min(self.spectral_axis), max(self.spectral_axis), 500)
            self.y = X_Y_Spline(self.x)            
        if name == '':
            self.x = self.spectral_axis
            self.y = self.flux
        
class SDSS_Sloan_g(Filters):
    # Class SDSS/Sloan g' filter 
    def __init__(self):
        self.set_filter()
    
    def set_filter(self):
        self.spectral_axis = [3950, 4010, 4100, 4200, 4310, 4400, 4500, 4600, 4800, 5000, 5100, 5200, 5300, 5400, 5500, 5595, 5600, 5700]        
        self.flux = [0, 0.9, 0.94, 0.96, 0.98, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0.98, 0.20, 0.04, 0]       
        self.name = "Baader SLOAN/SDSS g' photometric"
        self.label = "g'"
        self.color = 'cornflowerblue' 
        self.make_XY('interp1d')

class SDSS_Sloan_r(Filters):
    # Class SDSS/Sloan r' filter 
    def __init__(self):
        self.set_filter()
    
    def set_filter(self):
        self.spectral_axis = [5595, 5610, 6995, 7020]
        self.flux = [0, 1, 1, 0]
        self.name = "Baader SLOAN/SDSS r' photometric"
        self.label = "r'"
        self.color = 'darkorange'
        self.make_XY('interp1d')

class SDSS_Sloan_u(Filters):
    # Class SDSS/Sloan u' filter 
    def __init__(self):
        self.set_filter()
    
    def set_filter(self):
        self.spectral_axis = [  3013.5134,
                                3112.6125,
                                3175.6758,
                                3198.1982,
                                3202.7026,
                                3211.7117,
                                3220.7207,
                                3274.7747,
                                3351.3513,
                                3450.4504,
                                3549.5496,
                                3644.144,
                                3690.2073,
                                3750.2703,
                                3792.7927,
                                3824.3242,
                                3851.3513,
                                3882.8828,
                                3896.3965,
                                3909.91,
                                3909.91,
                                3972.973 ]

        self.flux = [   0,
                        0.01,
                        0.01,
                        0.02,
                        0.50,
                        0.80,
                        0.83,
                        0.84,
                        0.84,
                        0.83,
                        0.81,
                        0.75,
                        0.70,
                        0.60,
                        0.50,
                        0.40,
                        0.30,
                        0.20,
                        0.10,
                        0.02,
                        0.01,
                        0 ]
        
        self.name = "Baader SLOAN/SDSS u' photometric"
        self.label = "u'"
        self.color = 'darkmagenta'
        self.make_XY('interp1d')

class SDSS_Sloan_i(Filters):
    # Class SDSS/Sloan i' filter 
    def __init__(self):
        self.set_filter()
    
    def set_filter(self):
        self.spectral_axis = [6995, 7010, 8400, 8500]
        self.flux = [0, 1, 1, 0]
        self.name = "Baader SLOAN/SDSS i' photometric"
        self.label = "i'"
        self.color = 'indianred'
        self.make_XY('interp1d')

class SDSS_Sloan_z_s(Filters):
    # Class SDSS/Sloan z-s' filter 
    def __init__(self):
        self.set_filter()
    
    def set_filter(self):
        self.spectral_axis = [8100, 8300, 9100, 9300]
        self.flux = [0, 1, 1, 0]
        self.name = "Baader SLOAN/SDSS z- s' photometric"
        self.label = "z- s'"
        self.color = 'red'
        self.make_XY('interp1d')

class SDSS_Sloan_y(Filters):
    # Class SDSS/Sloan y' filter 
    def __init__(self):
        self.set_filter()
    
    def set_filter(self):
        self.spectral_axis = [9300, 9450, 10450, 10600]
        self.flux = [0, 1, 1, 0]
        self.name = "Baader SLOAN/SDSS y' photometric"
        self.label = "y'"
        self.color = 'darkred'
        self.make_XY('interp1d')

class Bessel_V(Filters):
    # Class UBVRI Bessel V filter 
    def __init__(self):
        self.set_filter()
    
    def set_filter(self):
        self.spectral_axis = [4800, 4900, 5000, 5100, 5200, 5400, 5600, 5800, 6000, 6200, 6400, 6600, 6800]
        self.flux = [0, 0.35, 0.70, 0.85, 0.93, 0.905, 0.815, 0.66, 0.45, 0.30, 0.15, 0.04, 0]
        self.name = "Baader UBVRI Bessel V photometric"
        self.label = "V"
        self.color = 'green'
        self.make_XY('make_interp_spline')
        
class Bessel_B(Filters):
    # Class UBVRI Bessel B filter 
    def __init__(self):
        self.set_filter()
    
    def set_filter(self):
        self.spectral_axis = [3800, 4000, 4200, 4400, 4600, 4800, 5000, 5100, 5200]
        self.flux = [0, 0.75, 0.80, 0.77, 0.70, 0.45, 0.20, 0.05, 0]
        self.name = "Baader UBVRI Bessel B photometric"
        self.label = "B"
        self.color = 'blue'
        self.make_XY('make_interp_spline')

class Bessel_R(Filters):
    # Class UBVRI Bessel R filter 
    def __init__(self):
        self.set_filter()
    
    def set_filter(self):
        self.spectral_axis = [5550, 5600, 5800, 6000, 6200, 6400, 6600, 6800, 7000, 7200, 7400, 7600, 7800, 8000, 8200, 8400, 8600]
        self.flux = [0, 0.20, 0.72, 0.80, 0.75, 0.66, 0.58, 0.45, 0.35, 0.25, 0.18, 0.12, 0.06, 0.04, 0.02, 0.01, 0]
        self.name = "Baader UBVRI Bessel R photometric"
        self.label = "R"
        self.color = 'orange'
        self.make_XY('make_interp_spline')
        
class Bessel_U(Filters):
    # Class UBVRI Bessel U filter 
    def __init__(self):
        self.set_filter()
    
    def set_filter(self):
        self.spectral_axis = [3200, 3400, 3600, 3800, 4000, 4100]
        self.flux = [0, 0.30, 0.60, 0.60, 0.20, 0]
        self.name = "Baader UBVRI Bessel U photometric"
        self.label = "U"
        self.color = 'violet'
        self.make_XY('make_interp_spline')

class Bessel_I(Filters):
    # Class UBVRI Bessel I filter 
    def __init__(self):
        self.set_filter()
    
    def set_filter(self):
        self.spectral_axis = [7000, 7200, 7400, 7600, 7800, 8000, 8200, 8400, 8600, 8800, 9000, 9200, 9400, 9600, 9800, 10000, 10200, 10400, 10600, 10800, 11000, 11200, 11400, 11500]
        self.flux = [0, 0.30, 0.80, 0.93, 0.95, 0.94, 0.93, 0.92, 0.91, 0.90, 0.89, 0.86, 0.84, 0.80, 0.75, 0.67, 0.60, 0.50, 0.40, 0.28, 0.20, 0.10, 0.04, 0]
        self.name = "Baader UBVRI Bessel I photometric"
        self.label = "I"
        self.color = 'darkred'
        self.make_XY('make_interp_spline')

class Ha35nm(Filters):
    # Class Baader H-alpha 35nm filter 
    def __init__(self):
        self.set_filter()
    
    def set_filter(self):
        self.spectral_axis = [6200, 6300, 6500, 6600, 6700]
        self.flux = [0, 0.70, 0.95, 0.85, 0]
        self.name = "Baader H-alpha 35nm"
        self.label = r'H$\alpha$'
        self.color = 'red'
        self.make_XY('make_interp_spline')

class RGB_B(Filters):
    # Class Baader RGB B filter optimised CMOS
    def __init__(self):
        self.set_filter()
    
    def set_filter(self):
        self.spectral_axis = [3895, 4000, 4100, 4200, 4300, 4400, 4600, 4800, 5000, 5100]
        self.flux = [0, 0.90, 0.93, 0.96, 0.99, 0.99, 0.99, 0.99, 0.99, 0]
        self.name = "Baader RGB-B filter optimised CMOS"
        self.label = 'B'
        self.color = 'blue'
        self.make_XY('interp1d')

class RGB_G(Filters):
    # Class Baader RGB G filter optimised CMOS
    def __init__(self):
        self.set_filter()
    
    def set_filter(self):
        self.spectral_axis = [4850, 4900, 5000, 5200, 5400, 5600, 5790, 5800, 5805]
        self.flux = [0, 0.98, 0.99, 0.99, 0.99, 0.99, 0.99, 0.20, 0]
        self.name = "Baader RGB-G filter optimised CMOS"
        self.label = 'G'
        self.color = 'green'
        self.make_XY('interp1d')

class RGB_R(Filters):
    # Class Baader RGB R filter optimised CMOS
    def __init__(self):
        self.set_filter()
    
    def set_filter(self):
        self.spectral_axis = [5850, 5950, 6000, 6200, 6400, 6600, 6800, 6850, 7000]
        self.flux = [0, 0.99, 0.99, 0.99, 0.99, 0.99, 0.99, 0.98,0]
        self.name = "Baader RGB-R filter optimised CMOS"
        self.label = 'R'
        self.color = 'red'
        self.make_XY('interp1d')
    
class cls_ccd(Filters):
    # Class Astronomik CLS CCD filter 
    def __init__(self):
        self.set_filter()
    
    def set_filter(self):
        self.spectral_axis = [4400, 4600, 4800, 5000, 5200, 5400, 5600, 5800, 6000, 6200, 6400, 6600, 6800, 7000]
        self.flux = [0, 0.90, 0.95, 0.95, 0.90, 0.15, 0.01, 0.01, 0.01, 0.15, 0.85, 0.93, 0.95, 0 ]
        self.name = "Astronomik CLS CCD"
        self.label = 'CLS'
        self.color = 'grey'
        self.make_XY('make_interp_spline')

class OIII12nm(Filters):
    # Class Astronomik OIII CCD 12 nm filter 
    def __init__(self):
        self.set_filter()
    
    def set_filter(self):
        self.spectral_axis = [4850, 4900, 4950, 5000, 5050, 5100, 5150]
        self.flux = [0, 0.10, 0.85, 0.96, 0.60, 0.05, 0]
        self.name = "Astronomik OIII CCD 12nm"
        self.label = 'OIII'
        self.color = 'teal'
        self.make_XY('make_interp_spline')
