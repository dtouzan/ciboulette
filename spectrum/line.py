"""
Lines class


"""

__authors__ = ("Dominique Touzan","ciboulette module")
__contact__ = ("dtouzan@gmail.com","https://github.com/dtouzan/ciboulette")
__copyright__ = "MIT"
__date__ = "2023-04-10"
__version__ = "1.0.0"

# Astropy mods
from astropy import units as u
from astropy.table import Table
# Local mods
from ciboulette.spectrum import atomiclines

AtomicLine_Ha = {'name': 'H alpha', 'label': "r'H$\alpha$'", 'wavelength': 660, 'spectrum': 'H I'}
AtomicLine_Hb = {'name': 'H beta', 'label': "r'H$\beta$'", 'wavelength': 490, 'spectrum': 'H I'}
AtomicLine_Hg = {'name': 'H gamma', 'label': "r'H$\gamma$'", 'wavelength': 440, 'spectrum': 'H I'}
AtomicLine_Hd = {'name': 'H delta', 'label': "r'H$\delta$'", 'wavelength': 411, 'spectrum': 'H I'}
AtomicLine_He = {'name': 'H epsilon', 'label': "r'H$\epsilon$'", 'wavelength': 399, 'spectrum': 'H I'}
AtomicLine_Hz = {'name': 'H zeta', 'label': "r'H$\zeta$'", 'wavelength': 389, 'spectrum': 'H I'}
AtomicLine_D2 = {'name': 'sodium D2', 'label': 'D2', 'wavelength': 589.9, 'spectrum': 'Na I'}
AtomicLine_D1 = {'name': 'sodium D1', 'label': 'D1', 'wavelength': 589, 'spectrum': 'Na I'}
AtomicLine_H = {'name': 'calcium H1', 'label': 'H', 'wavelength': 397, 'spectrum': 'Ca II'}
AtomicLine_K = {'name': 'calcium K', 'label': 'K', 'wavelength': 393.7, 'spectrum': 'Ca II'}
AtomicLine_G = {'name': 'bande G (Ca+Fe)', 'label': 'G', 'wavelength': 430.8, 'spectrum': 'Fe I'}
AtomicLine_Mb1 = {'name': 'magnesium b1', 'label': 'b1', 'wavelength': 516.8, 'spectrum': 'Mg I'}
AtomicLine_Mb2 = {'name': 'magnesium b2', 'label': 'b2', 'wavelength': 517.3, 'spectrum': 'Mg I'}
AtomicLine_Mb3 = {'name': 'magnesium b2', 'label': 'b2', 'wavelength': 518.4, 'spectrum': 'Mg I'}
AtomicLine_g = {'name': 'calcium g', 'label': 'g', 'wavelength': 422.8, 'spectrum': 'Ca I'}
AtomicLine_e = {'name': 'fer e', 'label': 'e', 'wavelength': 438.36, 'spectrum': 'Fe I'}
AtomicLine_d = {'name': 'fer d', 'label': 'e', 'wavelength': 466.82, 'spectrum': 'Fe I'}
AtomicLine_c = {'name': 'fer c', 'label': 'e', 'wavelength': 495.76, 'spectrum': 'Fe I'}
AtomicLine_E = {'name': 'fer E', 'label': 'E', 'wavelength': 526.98, 'spectrum': 'Fe I'}
AtomicLine_Ha = {'name': 'H alpha', 'label': "r'H$\alpha$'", 'wavelength': 657, 'spectrum': 'H I'}

class lines():
    """
    Create and plot atomic lines H alpha
    @set: dict.
          Ex: {'name': 'fer E', 'label': 'E', 'wavelength': 526.98, 'spectrum': 'Fe I'}
    """

    def __init__(self, spectrum_configure=dict):
        self.name = spectrum_configure['name']
        self.label = spectrum_configure['label']
        self.wavelength = float(spectrum_configure['wavelength'])
        self.spectrum = spectrum_configure['spectrum']
















