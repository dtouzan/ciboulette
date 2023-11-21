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
from astropy.table import Table, vstack as astropy_vstack

SPECTRUM_FILE = (('atomicline_HI.csv', 'H I'),
                 ('atomicline_FeI.csv', 'Fe I'),
                 ('atomicline_FeII.csv', 'Fe II'),
                 ('atomicline_FeIII.csv', 'Fe III'),
                 ('atomicline_NaI.csv', 'Na I'),
                 ('atomicline_NaII.csv', 'Na II'),
                 ('atomicline_CaI.csv', 'Ca I'),
                 ('atomicline_CaII.csv', 'Ca II'),
                 ('atomicline_MgI.csv', 'Mg I'),
                 ('atomicline_MgII.csv', 'Mg II'),
                 ('atomicline_OI.csv', 'O I'),
                 ('atomicline_OII.csv', 'O II'),
                 ('atomicline_OIII.csv', 'O III'))

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
        atomic_line = Table.read(package_file, format='ascii.csv', header_start=5, data_start=6, delimiter='|') 

        # Re-Type colunm

        atomic_line['Rel'] = atomic_line['Rel'].astype(str)  
        atomic_line['Aki'] = atomic_line['Aki'].astype(str)     
        atomic_line['Acc'] = atomic_line['Acc'].astype(str)       
        atomic_line['Ei - Ek'] = atomic_line['Ei - Ek'].astype(str)              
        atomic_line['L Conf'] = atomic_line['L Conf'].astype(str)     
        atomic_line['L J'] = atomic_line['L J'].astype(str)
        atomic_line['L Term'] = atomic_line['L Term'].astype(str) 
        atomic_line['U Conf'] = atomic_line['U Conf'].astype(str)
        atomic_line['U J'] = atomic_line['U J'].astype(str)
        atomic_line['U Term'] = atomic_line['U Term'].astype(str)
        atomic_line['gi - gk'] = atomic_line['gi - gk'].astype(str)
        atomic_line['Type'] = atomic_line['Type'].astype(str)
        atomic_line['TP'] = atomic_line['TP'].astype(str)    

        # Rename colunm(15)
        atomic_line.rename_column('col15', 'Spectrum')
        atomic_line['Spectrum'] = atomic_line['Spectrum'].astype(str)
        atomic_line[:]['Spectrum']=self.spectrum
        
        if self.available:
            self.atomic_line = astropy_vstack([self.atomic_line, atomic_line])
        else:
            self.atomic_line = atomic_line
        self.spectrum=''

    @property
    def catalog(self):
        """
        Set ciboulette catalog atomic linesn in module path spectrum
        """
        for file, spectrum in SPECTRUM_FILE:
            self.spectrum = spectrum
            self.read('ciboulette/spectrum/', file)


    @property
    def minmax(self):
        """
        @init Lambda min and lambda max
        @return: wavelength range
        """
        if self.available:
            lambda_min = min(self.atomic_line['Wavelength'])
            lambda_max = max(self.atomic_line['Wavelength'])                
        else:
            lambda_min = 300
            lambda_max = 800    
        return lambda_min, lambda_max, lambda_max - lambda_min

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
            self.thick_headed
            if self.spectrum != '':
                mask = (self.lambda_min < self.atomic_line['Wavelength']) & (self.atomic_line['Wavelength'] < self.lambda_max) & (self.atomic_line['Spectrum']==self.spectrum)
            else:
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
            
    @property
    def header_names(self):
        """
        @return:  A list representing dataset headers
        """
        return self.atomic_line.colnames

    def get(self, name='', label=''):
        """
        @return:  A dict representing data line
        """
        spectrum = 'H I'
        wavelength = 658.28
        request = self.request
        spectrum = request['Spectrum'][0]
        wavelength = str(request['Wavelength'][0])
        value = {'name': name, 'label': label, 'wavelength': wavelength, 'spectrum': spectrum}
        return value
               



