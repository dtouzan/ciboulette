"""
Exposure class
"""

from datetime import datetime

class Exposure(object):
    
    def __init__(self):
        self.data = []
        self.exptime = 0
        self.label = 1       

    @property
    def exp_time(self):
        """
        Return exposure time                  
        """            
        return self.exptime
    
    @property
    def exp_label(self):
        """
        Return label of frame
        """
        return self.label

    @exp_time.setter
    def exp_time(self,exptime):
        """
        Initialization exposure time
        exptime (float): Exposure time second.
        """                    
        self.exptime = exptime            

    @exp_label.setter  
    def exp_label(self,label):
        """
        Initialization serial number
         label (int): Serial number.
        """
        self.number = label

    @property    
    def inc_label(self):
        """
        Increment serial number
        """
        self.number = self.number + 1
     
    @property
    def today_to_label(self):
        """
        Initialization serial number whit date end time                         
        """
        today = datetime.today()        
        self.label = today.strftime('%Y%m%d%H%M%S')
