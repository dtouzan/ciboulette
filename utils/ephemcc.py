"""Ephemcc software

"""

from astropy.io.votable import parse_single_table
import os
import wget


class Ephemcc :
    
    """Ephemcc class, Miriade Ephemeris Generator
        http://vo.imcce.fr/webservices/miriade/?ephemcc   
    
    """
    
    filename = 'imcce_query.xml'
    key_space = '%20'
    
    url_base = 'http://vo.imcce.fr/webservices/miriade/ephemcc_query.php?'
    name_query = 'c/2020_m3'
    type_query = 'comet'
    ep_query = '2021-01-01T22:00:0.0'
    ndb_query = '1'
    step_query = '1d'
    observer = '-0.3531'+key_space+'49.5961'+key_space+'100.0'
    
    
    
    def __init__(self) :
        
        self.data = []


        
    def get(self) :
        
        """The Miriade ephemcc service where [parameters] is a list of parameters separated by the character &.
            http://vo.imcce.fr/webservices/miriade/ephemcc_query.php?[parameters]    
        
        """
    
        if os.path.exists(self.filename) :
            os.remove(self.filename)
    
        url = self.url_base+'-name='+self.name_query+'&-type='+self.type_query+'&-nbd='+self.ndb_query+'&-ep='+self.ep_query+'&-step='+self.step_query+'&-observer='+self.observer+'&-mime=votable'
        filedownload = wget.download(url,out='imcce_query.xml')
    
        ephemcctable = parse_single_table(filedownload).to_table()
    
        return ephemcctable
    
    
    
    def setname(self,name_query) :
        
        """The designation (1) of the target
            Ex.: p:Mars, p:5, a:Pallas, a:1999 TC36(*), c:p/halley
        
        Attributes:
                name_query (str): name traget.        

        """
  
        self.name_query = name_query
    
    
    
    def settype(self,type_query) :
        
        """Type of the target (1)
            [Optional parameter, default = empty]
            Asteroid | Comet | Dwarf Planet | Planet | Satellite
                a    |   c   |       d      |    p   |     s
        
         Attributes:
                type_query (str): type target.           
       
        """

        choices = {'c': 'comet', 'd': 'Dwarf Planet', 'a': 'asteroid', 'p': 'planet', 's': 'satellite'}
        result = choices.get(type_query, 'asteroid')
        
        self.type_query = result
        
        
            
    def setndb(self,ndb_query) :
        
        """Number of dates of ephemeris to compute
            [Optional parameter, default = 1]
            
        Attributes:
                ndb_query (int): result number.   
        
        """
        
        if ndb_query < 1 :
            ndb_query = 1
        if ndb_query > 5000 :
            ndb_query = 5000
        self.ndb_query = str(ndb_query)
        
        
            
    def setep(self,ep_query):
        
        """Requested epoch, expressed in Julian day, ISO format, or formatted as any English textual datetime
            http://php.net/manual/en/function.strtotime.php
            Ex.: 2021-01-01T22:00:00
            
        Attributes:
                ep_query (str): Requested epoch.           
        
        """
        
        self.ep_query = ep_query
        
        
            
    def setstep(self,step_query) :

        """Step of increment (float) followed by one of (d)ays or (h)ours or (m)inutes or (s)econds.
            [Optional parameter, default = 1d]
            Ex.: 2.345h or 1d
           
        Attributes:
                step_query (str): step of increment.           

        """
       
        self.step_query = step_query
