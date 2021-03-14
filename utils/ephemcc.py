"""
Ephemcc software
"""

from astropy.io.votable import parse_single_table
from astropy.table import Table
from astropy.coordinates import SkyCoord, Angle
import os
import wget

class Ephemcc(object):    
    """
    Ephemcc class, Miriade Ephemeris Generator
     http://vo.imcce.fr/webservices/miriade/?ephemcc   
    """
    
    def __init__(self):
        
        self.data = []
        self.filename = 'imcce_query.xml'
        self.key_space = '%20'
        self.url_base = 'http://vo.imcce.fr/webservices/miriade/ephemcc_query.php?'
        self.name_query = 'c/2020_m3'
        self.type_query = 'comet'
        self.ep_query = '2021-01-01T22:00:0.0'
        self.ndb_query = '1'
        self.step_query = '1d'
        self.observer = '-0.3531'+self.key_space+'49.5961'+self.key_space+'100.0'
    
    @property
    def get(self):
        
        """
        The Miriade ephemcc service where [parameters] is a list of parameters separated by the character &.
         http://vo.imcce.fr/webservices/miriade/ephemcc_query.php?[parameters]            
        """    
        if os.path.exists(self.filename) :
            os.remove(self.filename)    
        url = self.url_base+'-name='+self.name_query+'&-type='+self.type_query+'&-nbd='+self.ndb_query+'&-ep='+self.ep_query+'&-step='+self.step_query+'&-observer='+self.observer+'&-mime=votable'
        filedownload = wget.download(url,out='imcce_query.xml',bar=None)   
        ephemcctable = parse_single_table(filedownload).to_table()   
        return ephemcctable     
    
    @property
    def name(self):
        return self.name_query
    
    @name.setter
    def name(self,name_query):     
        """
        The designation (1) of the target
         Ex.: Mars, 5, Pallas, 1999 TC36(*), p/halley       
         Attributes:
                name_query (str): name traget.        
        """ 
        self.name_query = name_query   
    
    @property
    def typequery(self):
        return self.type_query
    
    @typequery.setter
    def typequery(self,type_query):        
        """
        Type of the target (1)
         [Optional parameter, default = empty]
         Asteroid | Comet | Dwarf Planet | Planet | Satellite
             a    |   c   |       d      |    p   |     s
         Attributes:
                type_query (str): type target.                 
        """
        choices = {'c': 'comet', 'd': 'Dwarf Planet', 'a': 'asteroid', 'p': 'planet', 's': 'satellite'}
        result = choices.get(type_query, 'asteroid')      
        self.type_query = result
               
    @property
    def ndb(self): 
        return self.ndb_query
    
    @ndb.setter
    def ndb(self,ndb_query): 
        """
        Number of dates of ephemeris to compute
         [Optional parameter, default = 1]            
         Attributes:
                ndb_query (int): result number.          
        """       
        if ndb_query < 1 :
            ndb_query = 1
        if ndb_query > 5000 :
            ndb_query = 5000
        self.ndb_query = str(ndb_query)
                    
    @property
    def ep(self): 
        return self.ep_query
    
    @ep.setter
    def ep(self,ep_query):        
        """
        Requested epoch, expressed in Julian day, ISO format, or formatted as any English textual datetime
         http://php.net/manual/en/function.strtotime.php
         Ex.: 2021-01-01T22:00:00
         Attributes:
                ep_query (str): Requested epoch.                   
        """       
        self.ep_query = ep_query
        
    @property
    def step(self): 
        return self.step_query        
    
    @step.setter
    def step(self,step_query):
        """
        Step of increment (float) followed by one of (d)ays or (h)ours or (m)inutes or (s)econds.
         [Optional parameter, default = 1d]
         Ex.: 2.345h or 1d
         Attributes:
                step_query (str): step of increment.           
        """    
        self.step_query = step_query

    @property
    def observers(self): 
        return self.observer        
    
    @observers.setter
    def observers(self,sitedict):
        """
        Code or geographic coordinates of the observer's location (2)
         [Optional parameter, default = 500]  
         sitedict:
         {
            "LAT": float - site latitude
            "LONG": float - site longitude
            "ELEV": float - site elevation
          }
        """  
        latitude = 0
        longitude = 0
        elevation = 0
        if 'LAT' in sitedict:
            latitude = float(sitedict['LAT'])
        if 'LONG' in sitedict:
            longitude = float(sitedict['LONG'])
        if 'ELEV' in sitedict:
            elevation = float(sitedict['ELEV'])
        self.observer = str(longitude)+self.key_space+str(latitude)+self.key_space+str(elevation)    

    @property
    def regionincatalog(self):
        """
        Return data of file
        """
        table_ra = []
        table_dec = []
        table_marker = []
        table = parse_single_table(self.filename).to_table()
        if table:
            for line in table:
                c = SkyCoord(line['ra'], line['dec'], unit='deg', frame='icrs')
                table_ra.append(c.ra.degree*15)
                table_dec.append(c.dec.degree)
                table_marker.append(int(line['mv']))
        return Table([table_ra,table_dec,table_marker], names=['RA', 'DEC', 'MARKER'])
