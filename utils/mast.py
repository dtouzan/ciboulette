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

    @property
    def idfiledrive(self):
        """
        Return ID google drive file
        """     
        return self.idgoogledrive    
    
    @idfiledrive.setter
    def idfiledrive(self,idgoogledrive):
        """
        Set ID google drive file
         idgoogledrive (str): ID google drive file.csv.       
        """     
        self.idgoogledrive = idgoogledrive                 

    @property
    def output(self):
        """
        Return fileoutput
        """     
        return self.fileoutput

    @output.setter
    def output(self,fileoutput):
        """
        Set table of exposures with google drive 
         fileoutput (str): file.csv output.
        """
        self.fileoutput = fileoutput

    def ra(self,observation):
        """
        Return RA of plan. Format: Hours H.HHHH
         plan (Table): plan of planning.
        """           
        if self.available:
            return float(observation[constant.MAST_s_ra])/15

    def dec(self,observation):
        """
        Return RA of plan. Format: Degrees D.DDDD
         plan (Table): plan of planning.
        """    
        if self.available:
            return float(observation[constant.MAST_s_dec]) 

    def coordinates(self,observation):
        """
        Return coordinates RA,DEC
        """
        if self.available:
            return self.ra(observation), self.dec(observation)

    @property
    def observations(self):
        """
        Return observations table
        """
        if len(self.observation) > 0:
            return self.observation
        else:
            return None
