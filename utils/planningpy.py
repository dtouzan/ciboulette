"""Planning class

"""

from astropy.table import Table
import os
import wget


class Planning:
    
    idgoogledrive = '1Yc-QxFr9veMeGjqvedRMrcEDL2GRyTS_'
    fileoutput = 'planning.csv'
    
    def __init__(self,idgoogledrive,fileoutput):
        
        self.data = []
        self.idgoogledrive = idgoogledrive
        self.fileoutput = fileoutput

    
    def get(self):
        """Return table of planning with google drive 
            Ex:  wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1Yc-QxFr9veMeGjqvedRMrcEDL2GRyTS_' -O planning.csv
        
        """
        
        if os.path.exists(self.fileoutput) :
            os.remove(self.fileoutput)
    
        url = 'https://docs.google.com/uc?export=download&id='+self.idgoogledrive
        filedownload = wget.download(url,out=self.fileoutput)
        
        planningtable = Table.read(self.fileoutput, format='ascii.csv')
    
        return planningtable
    
    
    def setidgoogledrive(self,idgoogledrive):
        """Set ID google drive file
        
        Attributes:
            idgoogledrive (str): ID google drive file.csv.
        
        """
        
        self.idgoogledrive = idgoogledrive
        
        return True
        
    
    def setfileoutput(self,fileoutput):
        """Set table of exposures with google drive 
        
        Attributes:
            fileoutput (str): file.csv output.
        
        """

        self.fileoutput = fileoutput
        
        return True