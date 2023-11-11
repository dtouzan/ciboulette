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

    def __init__(self, spectrum='H I'):
        self.atomic_line = []
        self.lambda_min = 300
        self.lambda_max = 800
        self.spectrum = spectrum
        self.unit = u.nm

    @property
    def available(self):
        if len(self.atomic_line) > 0:
            return True
        else:
            return False
    
    def read(self,package='ciboulette/spectrum/', file='atomicline_HI.csv'):
        """
        Set atomic_line
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
    def minmax(self):
        """
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
            """
            for value in values:
                if value['Wavelength'] < self.lambda_min or value['Wavelength'] > self.lambda_max:
                    index_table.append(index)
                index += 1
            index_table.reverse()
            for index in index_table:
                values.remove_row(index)
            """
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
            



