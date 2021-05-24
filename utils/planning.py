"""
Planning class

"""

from astropy.table import Table
from astropy import units as u
import numpy as np
import matplotlib.pyplot as plt
import os
import wget
from ciboulette.base import constant


class Planning(object):
    """
    Class for planning observation.
     idgoogledrive = 1Yc-QxFr9veMeGjqvedRMrcEDL2GRyTS_
     fileoutput = planning.csv    
    """
    
    def __init__(self, title='Planning', idgoogledrive='1Yc-QxFr9veMeGjqvedRMrcEDL2GRyTS_', fileoutput='planning.csv'):       
        self.idgoogledrive = idgoogledrive
        self.fileoutput = fileoutput
        self.title = title
        self.observation = Table()
        self.available = False
        self.timerinit = 10
        self.timerslew = 5
        self.timerguider = 3
        self.timerfilter = 3
        self.read
    

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
        self.observation = Table.read(self.fileoutput, format='ascii.csv')   
        if len(self.observation) > 0:
            self.available = True
        else:
            self.available = False
       
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
        return float(plan[constant.MAST_t_exptime])
    

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

    def collection(self,string):
        """
        Return find collection 
        """
        if self.available:
            mask = self.observation[constant.MAST_obs_collection] == string
            return self.observation[mask]

    def instrument(self,string):
        """
        Return find instrument
        """
        if self.available:
            mask = self.observation[constant.MAST_instrument_name] == string
            return self.observation[mask]      
            
    @property
    def observations(self):
        """
        Return observations table
        """
        if len(self.observation) > 0:
            return self.observation
        else:
            return None

    @property
    def duration(self):
        """
        Return planning duration
        """
        d = 0 * u.second
        if self.available:
            duration = 0
            for exptime in self.observation[constant.MAST_t_exptime]:
                duration = duration + float(exptime) + self.timerguider + self.timerslew + self.timerfilter
            d = (self.timerinit+duration) * u.second                     
        return d.to(u.hour)
        
    @property
    def number(self):
        """
        Return planning duration
        """
        number = 0
        if self.available:
            number = len(self.observations)
        return number
    
    def exposure(self,plan):
        """
        Return 
        """
        return self.exptime(plan), self.observationID(plan), self.dataproducttype(plan)
    
    @property
    def header(self):
        """
        Return title,number and duration in table
        """
        if self.available:
            title = [self.title]
            number = [self.number]
            duration = [self.duration]
            return Table([title,number,duration], names=['Title','Number','Duration'])  
        return None

