"""
AtomicLine class

Use astroquery / Atomic Line List (astroquery.atomic)

"""

from astropy import units as u
from astroquery.atomic import AtomicLineList


class AtomicLine(object):
    # Class for Element spectrum.
    
    def __init__(self):
        self.atomic_line = []
        self.name = ''
        self.label = ''
        
    def atomic_line_request(self, lambda_min = 380, lambda_max = 700, spectrum = 'H I'):
        wavelength_range = (lambda_min * u.nm, lambda_max * u.nm)
        self.atomic_line = AtomicLineList.query_object(wavelength_range = wavelength_range, wavelength_type = 'air',wavelength_accuracy = 20, element_spectrum = spectrum)

    @property
    def get(self):
        """
        @return:  A table of atomic line
        """     
        return self.atomic_line
     
    @property
    def spectrum(self): 
        """
        @return:  A float is label is 'SPRCTRUM' in atomic line class
        """     
        return self.atomic_line['SPECTRUM'].value[0]

    @property
    def value(self): 
        """
        @return:  A float is label is 'LAMBDA AIR ANG' in atomic line class
        """     
        return self.atomic_line['LAMBDA AIR ANG'].value[0]

    @property
    def get_label(self):
        """
        @return:  A string is label
        """     
        return self.label + ' ' + str(self.value) + ' - ' + self.spectrum
    
    def pin(self, axes, flux, marker_size = 10):
        """
        @set:  Plot pin
        """     
        # Plot marker
        # axes : matplotlib axes
        # flux : flux value
        # marker_size : size
        axes.plot(self.value, flux, marker = 'o', linewidth = 2, markersize = marker_size, linestyle = 'solid', color = 'black', alpha = 0.1)

    def marker(self, axes, flux, max_flux, font_size = 6):
        """
        @set:  Plot marker
        """     
        # Plot marker
        # axes : matplotlib axes
        # flux : flux value
        # font_size : size
        axes.vlines(self.value, flux, max_flux + 0.2, linewidths=1, linestyles = 'dashed', colors = 'red', alpha = 0.5)
        axes.annotate(f'{self.get_label}', xy=(self.value, max_flux + 0.2), xytext=(0,5), textcoords='offset points', rotation=90, va='bottom', ha='center', annotation_clip=False, fontsize=font_size)

        
class Ha(AtomicLine):
    # Class H alpha Balmer     
    def __init__(self):
        self.set_atomic_line()
        
    def set_atomic_line(self):
        """
        @set:  Set atomic line H alpha
        """     
        self.name = 'H alpha'
        self.label = r'H$\alpha$'
        self.atomic_line_request(650, 660, 'H I')       
    
class Hb(AtomicLine):
    # Class H beta Balmer 
    def __init__(self):
        self.set_atomic_line()
        
    def set_atomic_line(self):
        """
        @set:  Set atomic line H beta
        """     
        self.name = 'H beta'
        self.label = r'H$\beta$'
        self.atomic_line_request(480, 490, 'H I')
        
class Hg(AtomicLine):
    # Class H gamma Balmer    
    def __init__(self):
        self.set_atomic_line()
        
    def set_atomic_line(self):
        """
        @set:  Set atomic line H gamma
        """     
        self.name = 'H gamma'
        self.label = r'H$\gamma$'
        self.atomic_line_request(430, 440, 'H I')

class Hd(AtomicLine):
    # Class H delta Balmer    
    def __init__(self):
        self.set_atomic_line()
        
    def set_atomic_line(self):
        """
        @set:  Set atomic line H delta
        """     
        self.name = 'H delta'
        self.label = r'H$\delta$'
        self.atomic_line_request(410, 411, 'H I')
        
class He(AtomicLine):
    # Class H epsilon Balmer    
    def __init__(self):
        self.set_atomic_line()
        
    def set_atomic_line(self):
        """
        @set:  Set atomic line H epsilon
        """     
        self.name = 'H epsilon'
        self.label = r'H$\epsilon$'
        self.atomic_line_request(390, 399, 'H I')
        
class Hz(AtomicLine):
    # Class H zeta Balmer     
    def __init__(self):
        self.set_atomic_line()
        
    def set_atomic_line(self):
        """
        @set:  Set atomic line H zeta
        """     
        self.name = 'H zeta'
        self.label = r'H$\zeta$'
        self.atomic_line_request(388, 389, 'H I')
        
class D2(AtomicLine):
    # Class Sodium D2
    def __init__(self):
        self.set_atomic_line()
        
    def set_atomic_line(self):
        """
        @set:  Set atomic line sodium D2
        """     
        self.name = 'sodium D2'
        self.label = 'D2'
        self.atomic_line_request(589.1, 589.9, 'Na I')

class D1(AtomicLine):
    # Class sodium D1   
    def __init__(self):
        self.set_atomic_line()
        
    def set_atomic_line(self):
        """
        @set:  Set atomic line sodium D1
        """     
        self.name = 'sodium D1'
        self.label = 'D1'
        self.atomic_line_request(588.8 , 589, 'Na I')

class H(AtomicLine):
    # Class calcium H    
    def __init__(self):
        self.set_atomic_line()
        
    def set_atomic_line(self):
        """
        @set:  Set atomic line calcium H
        """     
       self.name = 'calcium H'
        self.label = 'H'
        self.atomic_line_request(396.7 , 397, 'Ca II')

class K(AtomicLine):
    # Class calcium K   
    def __init__(self):
        self.set_atomic_line()
        
    def set_atomic_line(self):
        """
        @set:  Set atomic line calcium K
        """     
        self.name = 'calcium K'
        self.label = 'K'
        self.atomic_line_request(393.1 , 393.7, 'Ca II')
        
class G(AtomicLine):
    # Class bande G
    def __init__(self):
        self.set_atomic_line()
        
    def set_atomic_line(self):
        """
        @set:  Set atomic line bande G (Ca+Fe)
        """     
        self.name = 'bande G (Ca+Fe)'
        self.label = 'G'
        self.atomic_line_request(430.79, 430.8, 'Fe I')  
        
class Mb1(AtomicLine):
    # Class magnesium b1   
    def __init__(self):
        self.set_atomic_line()
        
    def set_atomic_line(self):
        """
        @set:  Set atomic line magnesium b1
        """     
        self.name = 'magnesium b1'
        self.label = 'b1'
        self.atomic_line_request(516.6, 516.8, 'Mg I') 
         
class Mb2(AtomicLine):
    # Class magnesium b2
    def __init__(self):
        self.set_atomic_line()
        
    def set_atomic_line(self):
        """
        @set:  Set atomic line magnesium b2
        """     
        self.name = 'magnesium b2'
        self.label = 'b2'
        self.atomic_line_request(517.1, 517.3, 'Mg I')  

class Mb3(AtomicLine):
    # Class magnesium b3   
    def __init__(self):
        self.set_atomic_line()
        
    def set_atomic_line(self):
        """
        @set:  Set atomic line magnesium b3
        """     
        self.name = 'magnesium b3'
        self.label = 'b3'
        self.atomic_line_request(518.1, 518.4, 'Mg I')  
        
class g(AtomicLine):
    # Class calcium g    
    def __init__(self):
        self.set_atomic_line()
        
    def set_atomic_line(self):
        """
        @set:  Set atomic line calcium g
        """     
        self.name = 'calcium g'
        self.label = 'g'
        self.atomic_line_request(422.4, 422.8, 'Ca I')

class e(AtomicLine):
    # Class bande e   
    def __init__(self):
        self.set_atomic_line()
        
    def set_atomic_line(self):
        """
        @set:  Set atomic line fer e
        """     
        self.name = 'fer e'
        self.label = 'e'
        self.atomic_line_request(438.35, 438.36, 'Fe I') 

class d(AtomicLine):
    # Class fer d    
    def __init__(self):
        self.set_atomic_line()
        
    def set_atomic_line(self):
        """
        @set:  Set atomic line fer d
        """     
        self.name = 'fer d'
        self.label = 'd'
        self.atomic_line_request(466.8138, 466.82, 'Fe I') 

class c(AtomicLine):
    # Class fer c   
    def __init__(self):
        self.set_atomic_line()
        
    def set_atomic_line(self):
        """
        @set:  Set atomic line fer c
        """     
       self.name = 'fer c'
        self.label = 'c'
        self.atomic_line_request(495.759, 495.76, 'Fe I') 
    
class E(AtomicLine):
    # Class fer E    
    def __init__(self):
        self.set_atomic_line()
        
    def set_atomic_line(self):
        """
        @set:  Set atomic line fer E
        """     
       self.name = 'fer E'
        self.label = 'E'
        self.atomic_line_request(526.95, 526.98, 'Fe I') 

 