"""
Mast class
File id google 12QY7fQLqnoySHFnEoLMWQbqYjHmaDpGn
"""

import time
from astropy.table import Table
from astropy import units as u
import os
import wget
from ciboulette.base import constant
from ciboulette.utils import exposure


class Mast(object):
    
    def __init__(self, idgoogledrive='12QY7fQLqnoySHFnEoLMWQbqYjHmaDpGn', fileoutput='mast.csv'):
        self.idgoogledrive = idgoogledrive
        self.fileoutput = fileoutput
        self.observation = Table()
        self.available = False

        
        
    @property
    def create(self):
        """
        Create MAST type file with fits archives file
        """
        return True
    
    @property
    def read(self):
        """
        Read MAST type file
        Ex:  wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=12QY7fQLqnoySHFnEoLMWQbqYjHmaDpGn' -O mast.csv        
        """
        if os.path.exists(self.fileoutput) :
            os.remove(self.fileoutput)
        url = 'https://docs.google.com/uc?export=download&id='+self.idgoogledrive
        filedownload = wget.download(url,out=self.fileoutput,bar=None)      
        # For MAST data_start=3
        self.observation = Table.read(self.fileoutput, format='ascii.csv',header_start=2,data_start=3)   
        if len(self.observation) > 0:
            self.available = True
        else:
            self.available = False
        return self.available
    
    