"""
AtomicLine class

Use astroquery / Atomic Line List (astroquery.atomic). Deprecated

Citation Form staticmethod
        Kramida, A., Ralchenko, Yu., Reader, J. and NIST ASD Team (2022) ]. Available: https://physics.nist.gov/PhysRefData/ASD/index.html#Team.
        NIST Atomic Spectra Database (version 5.10), [Online]. Available: https://physics.nist.gov/asd [Thu Nov 09 2023].
        National Institute of Standards and Technology, Gaithersburg, MD. DOI: https://doi.org/10.18434/T4W30F
"""

__authors__ = ("Dominique Touzan","ciboulette module")
__contact__ = ("dtouzan@gmail.com","https://github.com/dtouzan/ciboulette")
__copyright__ = "MIT"
__date__ = "2023-04-10"
__version__ = "1.0.0"
__citation__ = "Kramida, A., Ralchenko, Yu., Reader, J. and NIST ASD Team (2022) ]. Available: https://physics.nist.gov/PhysRefData/ASD/index.html#Team.\n" \
                "NIST Atomic Spectra Database (version 5.10), [Online]. Available: https://physics.nist.gov/asd [Thu Nov 09 2023].\n" \
                "National Institute of Standards and Technology, Gaithersburg, MD. DOI: https://doi.org/10.18434/T4W30F" 

# Astropy mods
from astropy import units as u
from astropy.table import Table
from astropy.utils.data import get_pkg_data_filename

class atomic_lines():
    # Class for Element spectrum.
    """
    Create atomic line table
    """

    def __init__(self):
        self.atomic_line = Table()
        self.lambda_min = 300
        self.lambda_max = 800
        self.spectrum = ''
        self.unit = u.nm

    @property
    def available(self):
        if len(self.atomic_line) > 0:
            return True
        else:
            return False
    
    def read(self,package='ciboulette/spectrum/', file='atomicline_HI.csv'):
        """
        Set atomic_line whith file
        @set: package file directory
        @set: file 
        """
        package_file = package+file
        self.atomic_line = Table.read(package_file, format='ascii.csv', header_start=5, data_start=6, delimiter='|') 

    @property
    def H_I(self):
        """
        Set atomic_line H I
        """
        self.spectrum = 'H I'
        self.read('ciboulette/spectrum/','atomicline_HI.csv')

    @property
    def Fe_I(self):
        """
        Set atomic_line Fe I
        """
        self.spectrum = 'Fe I'
        self.read('ciboulette/spectrum/','atomicline_FeI.csv')

    @property
    def Fe_II(self):
        """
        Set atomic_line Fe II
        """
        self.spectrum = 'Fe II'
        self.read('ciboulette/spectrum/','atomicline_FeII.csv')

    @property
    def Fe_III(self):
        """
        Set atomic_line Fe III
        """
        self.spectrum = 'Fe III'
        self.read('ciboulette/spectrum/','atomicline_FeIII.csv')

    @property
    def Na_I(self):
        """
        Set atomic_line Na I
        """
        self.spectrum = 'Na I'
        self.read('ciboulette/spectrum/','atomicline_NaI.csv')

    @property
    def Na_II(self):
        """
        Set atomic_line Na II
        """
        self.spectrum = 'Na II'
        self.read('ciboulette/spectrum/','atomicline_NaII.csv')

    @property
    def Ca_I(self):
        """
        Set atomic_line Ca I
        """
        self.spectrum = 'Ca I'
        self.read('ciboulette/spectrum/','atomicline_CaI.csv')

    @property
    def Ca_II(self):
        """
        Set atomic_line Ca II
        """
        self.spectrum = 'Ca II'
        self.read('ciboulette/spectrum/','atomicline_CaII.csv')

    @property
    def Mg_I(self):
        """
        Set atomic_line Mg I
        """
        self.spectrum = 'Mg I'
        self.read('ciboulette/spectrum/','atomicline_MgI.csv')

    @property
    def Mg_II(self):
        """
        Set atomic_line Mg II
        """
        self.spectrum = 'Mg II'
        self.read('ciboulette/spectrum/','atomicline_MgII.csv')

    @property
    def O_I(self):
        """
        Set atomic_line O I
        """
        self.spectrum = 'O I'
        self.read('ciboulette/spectrum/','atomicline_OI.csv')

    @property
    def O_II(self):
        """
        Set atomic_line O II
        """
        self.spectrum = 'O II'
        self.read('ciboulette/spectrum/','atomicline_OII.csv')

    @property
    def O_III(self):
        """
        Set atomic_line O III
        """
        self.spectrum = 'O III'
        self.read('ciboulette/spectrum/','atomicline_OIII.csv')

    @property
    def minmax(self):
        """
        @init Lambda min and lambda max
        @return: wavelength range
        """
        if self.available:
            self.lambda_min = min(self.atomic_line['Wavelength'])
            self.lambda_max = max(self.atomic_line['Wavelength'])                
        else:
            self.lambda_min = 300
            self.lambda_max = 800    
        return self.lambda_max - self.lambda_min

    @property
    def wavelength_values(self):
        """
        @return:  A float Wavelength in atomic line
        """
        if self.available:
            return self.atomic_line['Wavelength']
        else:
            return False    

    @property
    def request(self):
        """
        @return:  A table in min and max atomic line
        """
        if self.available:
            index = 0
            index_table = []
            self.thick_headed
            mask = (self.lambda_min < self.atomic_line['Wavelength']) & (self.atomic_line['Wavelength'] < self.lambda_max)
            values = self.atomic_line[mask]
            return values
        else:
            return False   
    
    @property
    def thick_headed(self):
        """
        @set:  min and max (min < max)
        """
        if self.lambda_min > self.lambda_max:
            max = self.lambda_min
            self.lambda_min = self.lambda_max
            self.lambda_max = max
            



