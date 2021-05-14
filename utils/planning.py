"""
Planning class

"""

from astropy.table import Table
import os
import wget
from ciboulette.base import constant


class Planning(object):
    """
    Class for planning observation.
     idgoogledrive = 1Yc-QxFr9veMeGjqvedRMrcEDL2GRyTS_
     fileoutput = planning.csv    
    """
    
    def __init__(self,idgoogledrive='1Yc-QxFr9veMeGjqvedRMrcEDL2GRyTS_',fileoutput='planning.csv'):       
        self.idgoogledrive = idgoogledrive
        self.fileoutput = fileoutput
    

    @property
    def read(self):
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
        return plan[constant.MAST_filters] 
    

    def ra(self,plan):
        """
        Return RA of plan. Format: Hours H.HHHH
         plan (Table): plan of planning.
        """           
        return plan[constant.MAST_s_ra]


    def dec(self,plan):
        """
        Return RA of plan. Format: Degrees D.DDDD
         plan (Table): plan of planning.
        """    
        return plan[constant.MAST_s_dec] 


    def observationID(self,plan):
        """
        Return observation ID of plan
         plan (Table): plan of planning.
        """        
        return plan[constant.MAST_obs_id]
    

    def exptime(self,plan):
        """
        Return exposure of plan
         plan (Table): plan of planning.
        """    
        return plan[constant.MAST_t_exptime]
    

    def observationtitle(self,plan):
        """
        Return observaion title of plan
         plan (Table): plan of planning.
        """       
        return plan[constant.MAST_obs_title] 
    

    def dataproducttype(self,plan):
        """
        Return dataproduct type of plan
         plan (table): plan of planning.          
        """       
        return plan[constant.MAST_dataproduct_type]

    def target(self,plan):
        """
        Return target of plan
         plan (table): plan of planning.          
        """       
        return plan[constant.MAST_target_name]
    
    def observationcollection(self,plan):
        """
        Return obs_collection of plan
         plan (table): plan of planning.          
        """       
        return plan[constant.MAST_obs_collection]
    
    def instrumentname(self,plan):
        """
        Return instrument_name of plan
         plan (table): plan of planning.          
        """       
        return plan[constant.MAST_instrument_name]

    def proposalpi(self,plan):
        """
        Return proposal_pi of plan
         plan (table): plan of planning.          
        """       
        return plan[constant.MAST_proposal_pi]

    def moon(self,plan):
        """
        Return moon % of plan
         plan (table): plan of planning.          
        """       
        return plan[constant.MAST_moon]
