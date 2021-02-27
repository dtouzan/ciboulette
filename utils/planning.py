"""
Planning class

"""

from astropy.table import Table
import os
import wget
from ciboulette.base import constent


class Planning(object):
    """
    Class for planning observation.
     idgoogledrive = 1Yc-QxFr9veMeGjqvedRMrcEDL2GRyTS_
     fileoutput = planning.csv    
    """
    
    def __init__(self,idgoogledrive='1Yc-QxFr9veMeGjqvedRMrcEDL2GRyTS_',fileoutput='planning.csv'):       
        self.data = []
        self.idgoogledrive = idgoogledrive
        self.fileoutput = fileoutput
    

    @property
    def get(self):
        """
        Return table of planning with google drive 
         Ex:  wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1Yc-QxFr9veMeGjqvedRMrcEDL2GRyTS_' -O planning.csv        
        """
        if os.path.exists(self.fileoutput) :
            os.remove(self.fileoutput)
        url = 'https://docs.google.com/uc?export=download&id='+self.idgoogledrive
        filedownload = wget.download(url,out=self.fileoutput,bar=None)      
        # For MAST data_start=3
        planningtable = Table.read(self.fileoutput, format='ascii.csv')   
        return planningtable
       
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
    

    def filtername(self,plan):
        """
        Return filter name of plan
         plan (Table): plan of planning.
        """
        filter_name = 'L'
        filter_name = plan[constent.MAST_filters]       
        return filter_name
    

    def ra(self,plan):
        """
        Return RA of plan. Format: Hours H.HHHH
         plan (Table): plan of planning.
        """     
        ra = 0.0
        ra = plan[constent.MAST_s_ra]        
        return ra


    def dec(self,plan):
        """
        Return RA of plan. Format: Degrees D.DDDD
         plan (Table): plan of planning.
        """
        dec = 0.0
        dec = plan[constent.MAST_s_dec]     
        return dec


    def observationID(self,plan):
        """
        Return observation ID of plan
         plan (Table): plan of planning.
        """
        obs_id = 0
        obs_id = plan[constent.MAST_obs_id]         
        return obs_id
    

    def exptime(self,plan):
        """
        Return exposure of plan
         plan (Table): plan of planning.
        """    
        exptime = 0
        exptime = plan[constent.MAST_t_exptime] 
        return exptime
    

    def observaiontitle(self,plan):
        """
        Return observaion title of plan
         plan (Table): plan of planning.
        """       
        obs_title = 'none'
        obs_title = plan[constent.MAST_obs_title] 
        return obs_title
    

    def dataproducttype(self,plan):
        """
        Return dataproduct type of plan
         plan (table): plan of planning.          
        """       
        dataproduct_type = 'Intensity'
        dataproduct_type = plan[constent.MAST_dataproduct_type] 
        return dataproduct_type