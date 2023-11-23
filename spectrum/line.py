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

AtomicLine_y = {'name': 'y', 'label': 'y', 'wavelength': 898.765, 'spectrum': 'O II'}
AtomicLine_Z = {'name': 'Z', 'label': 'Z', 'wavelength': 822.696, 'spectrum': 'O II'}
AtomicLine_A = {'name': 'A', 'label': 'A', 'wavelength': 759.37, 'spectrum': 'O II'}
AtomicLine_B = {'name': 'B', 'label': 'B', 'wavelength': 686.719, 'spectrum': 'O II'}
AtomicLine_C = {'name': 'C', 'label': 'H Alpha', 'wavelength': 656.285175, 'spectrum': 'H I'}
AtomicLine_a = {'name': 'a', 'label': 'a', 'wavelength': 627.661, 'spectrum': 'O II'}
AtomicLine_D1 = {'name': 'D1', 'label': 'D1', 'wavelength': 589.592, 'spectrum': 'Na I'}
AtomicLine_D2 = {'name': 'D2', 'label': 'D2', 'wavelength': 588.995, 'spectrum': 'Na I'}
AtomicLine_D3 = {'name': 'D3 ou d', 'label': 'D3 ou d', 'wavelength': 587.562, 'spectrum': 'He I'}
AtomicLine_e = {'name': 'e', 'label': 'e', 'wavelength': 546.073, 'spectrum': 'Hg I'}
AtomicLine_E2 = {'name': 'E2', 'label': 'E2', 'wavelength': 527.039, 'spectrum': 'Fe I'}
AtomicLine_b1 = {'name': 'b1', 'label': 'b1', 'wavelength': 518.362, 'spectrum': 'Mg I'}
AtomicLine_b2 = {'name': 'b2', 'label': 'b2', 'wavelength': 517.27, 'spectrum': 'Mg I'}
AtomicLine_b3 = {'name': 'b3', 'label': 'b3', 'wavelength': 516.891, 'spectrum': 'Fe I'}
AtomicLine_b4 = {'name': 'b4', 'label': 'b4', 'wavelength': 516.722, 'spectrum': 'Mg I'}
AtomicLine_c = {'name': 'c', 'label': 'c', 'wavelength': 495.761, 'spectrum': 'Fe I'}
AtomicLine_F = {'name': 'F', 'label': 'H Beta', 'wavelength': 486.134, 'spectrum': 'H I'}
AtomicLine_d = {'name': 'd', 'label': 'd', 'wavelength': 466.814, 'spectrum': 'Fe I'}
AtomicLine_e = {'name': 'e', 'label': 'e', 'wavelength': 438.355, 'spectrum': 'Fe I'}
AtomicLine_Hg = {'name': 'G ou f', 'label': 'H gamma', 'wavelength': 434.047, 'spectrum': 'H I'}
AtomicLine_G_fe = {'name': 'G', 'label': 'G', 'wavelength': 430.79, 'spectrum': 'Fe I'}
AtomicLine_G = {'name': 'G', 'label': 'G', 'wavelength': 430.774, 'spectrum': 'Ca I'}
AtomicLine_h = {'name': 'h', 'label': 'H Delta', 'wavelength': 410.175, 'spectrum': 'H I'}
AtomicLine_He = {'name': 'H epsilon', 'label': 'He', 'wavelength': 397.0075, 'spectrum': 'H I'}
AtomicLine_Hz = {'name': 'H zeta', 'label': 'Hz', 'wavelength': 388.9064, 'spectrum': 'H I'}
AtomicLine_H = {'name': 'H', 'label': 'H', 'wavelength': 396.847, 'spectrum': 'Ca II'}
AtomicLine_K = {'name': 'K', 'label': 'K', 'wavelength': 393.366, 'spectrum': 'Ca II'}
AtomicLine_L = {'name': 'L', 'label': 'L', 'wavelength': 382.044, 'spectrum': 'Fe I'}
AtomicLine_N = {'name': 'N', 'label': 'N', 'wavelength': 358.121, 'spectrum': 'Fe I'}
AtomicLine_P = {'name': 'P', 'label': 'P', 'wavelength': 336.112, 'spectrum': 'Ti II'}
AtomicLine_T = {'name': 'T', 'label': 'T', 'wavelength': 302.108, 'spectrum': 'Fe I'}
AtomicLine_t = {'name': 't', 'label': 't', 'wavelength': 299.444, 'spectrum': 'Ni I'}




class lines():
    """
    Create and plot atomic lines H alpha
    @set: dict.
          Ex: {'name': 'fer E', 'label': 'E', 'wavelength': 526.98, 'spectrum': 'Fe I'}
    """

    def __init__(self, spectrum_configure: dict):
        self.name = spectrum_configure['name']
        self.label = spectrum_configure['label']
        self.wavelength = float(spectrum_configure['wavelength'])
        self.spectrum = spectrum_configure['spectrum']

    @property
    def get(self):
        """
        @return:  A json data line
        """
        return {'name': self.name, 'label': self.label, 'wavelength': self.wavelength, 'spectrum': self.spectrum}

    @property
    def labels(self):
        """
        @return:  A string is 'label value-spectrum'
        """
        dataset = self.label + ' ' + str(self.wavelength) + ' - ' + self.spectrum
        return {'label': dataset}

    @property
    def Angstrom(self):
        """
        @set:   convert nm in Angstron 
        """
        self.wavelength = self.wavelength*10

    @property
    def nm(self):
        """
        @set:   convert nm in Angstron 
        """
        self.wavelength = self.wavelength/10
    

    def pin(self, flux: float, size: int = 10):
        """
        @set:  Plot pin
        @set:  flux
        """
        # Plot marker
        # axes : matplotlib axes define in plot fonction
        # flux : flux value
        # marker_size : size
        self.axis.plot(self.wavelength, flux, marker = 'o', linewidth = 2, markersize = size, linestyle = 'solid', color = 'black', alpha = 0.1)

    def marker(self, flux: float, max_flux: float, font_size: int = 6):
        """
        @set:  Plot marker
        """
        # Plot marker
        # axes : matplotlib axes define in plot fonction
        # flux : flux value
        # font_size : size
        self.axis.vlines(self.wavelength, flux, max_flux + 0.2, linewidths=1, linestyles = 'dashed', colors = 'red', alpha = 0.5)
        self.axis.annotate(f'{self.labels['label']}', xy=(self.wavelength, flux), xytext=(font_size,0), textcoords='offset points', rotation=90, va='bottom', ha='center', annotation_clip=False, fontsize=font_size)














