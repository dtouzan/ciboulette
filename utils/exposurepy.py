"""Exposure class

"""

from datetime import datetime

class Exposure:
        
        exptime = 0
        number = 1       

        def __init__(self):
        
            self.data = []
       
        def getexptime(self):
            """Return exposure time                  

            """
            
            return self.exptime
        
        def getnumber(self):
            """Return number of frame
                
            """
 
            return self.number


        def setexptime(self,exptime):
            """Initialization exposure time
                 
            Attributes:
                exptime (float): Exposure time.
                
            """
                    
            self.exptime = exptime
            
            return True
      
        
        def setnumber(self,number):
            """Initialization serial number
                 
            Attributes:
                number (int): Serial number.
                
            """
                    
            self.number = number
            
            return True

        def incnumber(self):
            """Increment serial number
                 
            """
                    
            self.number = self.number + 1
            
            return True
        
        def todaytonumber(self):
            """Initialization serial number whit date end time
                                 
            """
            today = datetime.today()        
            self.number = today.strftime('%Y%m%d%H%M%S')
            
            return True