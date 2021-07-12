"""
Projection class
"""

from astropy.time import Time
from astropy.table import Table
from astropy.coordinates import SkyCoord, Angle
from astropy import units as u
from astropy import wcs
import matplotlib.pyplot as plt
from ciboulette.sector import sector as Sct
from ciboulette.utils import planning
from ciboulette.utils.mast import Mast


class _database(object):
    
        def __init__(self,table):
            self.data = table
            self.title = 'Cursor'
            self.size = 2
            self.color = 'blue'
            self.marker = 'o'
            self.alpha = 0.8
         
        def properties(self,title='',size=2,color='blue',marker='o',alpha='0.8'):
            """
            Properties initialisation
            """
            self.title = title
            self.size = size
            self.color = color
            self.marker = marker
            self.alpha = alpha      
        
        def plot(self):
            """
            Plot database
            """
            plt.plot(self.data['RA'], self.data['DEC'],ls='', marker=self.marker, color=self.color, markersize=self.size, alpha=self.alpha)

class _databaseconstellation(_database):
    
        def plot(self):
            """
            Plot database
            """
            plt.plot(self.data['RA'], self.data['DEC'], ls=self.marker, color=self.color, lw=self.size, alpha=self.alpha)

class _databaseaera(_database):
    
        def plot(self):
            """
            Plot database
            """
            plt.plot(self.data['RA'], self.data['DEC'],  ls=self.marker, color=self.color, lw=self.size, alpha=self.alpha)
            plt.fill_between(self.data['RA'],self.data['DEC'], color=self.color, alpha=self.alpha-0.1)           
            
"""
Main class
"""           

class Projection(object):
        
    def __init__(self,title=''):
            self.title = title
            self.width = 8
            self.height = 6
            self.ra = 0
            self.dec = 0
            self.date = Time.now()
            self.sct = Sct.Sector()
            self.databaselist = []
 
    def _datacursor(self,name,size,color,marker,alpha,data):
        """
        Create aera for database
        """
        _ra = []
        _dec = []
        if len(data) > 0:
            for line in data:
                c = SkyCoord(ra = line['RA'], dec = line['DEC'], unit = (u.deg, u.deg), frame='icrs')
                _ra.append(-c.ra.wrap_at(180 * u.deg).radian)
                _dec.append(c.dec.radian)
            database = _database(Table([_ra,_dec], names=['RA','DEC']))
            database.properties(title=name,size=size,color=color,marker=marker,alpha=alpha)
            self.databaselist.append(database)           

    def _dataaera(self,name,size,color,marker,alpha,data):
        """
        Create aera for database
        """
        _ra = []
        _dec = []
        if len(data) > 0:
            for line in data:
                c = SkyCoord(ra = line['RA'], dec = line['DEC'], unit = (u.deg, u.deg), frame='icrs')
                _ra.append(-c.ra.wrap_at(180 * u.deg).radian)
                _dec.append(c.dec.radian)
            database = _databaseaera(Table([_ra,_dec], names=['RA','DEC']))
            database.properties(title=name,size=size,color=color,marker=marker,alpha=alpha)
            self.databaselist.append(database)           

    def _dataconstellation(self,name,size,color,marker,alpha,data):
        """
        Create aera for database
        """
        _ra = []
        _dec = []
        if len(data) > 0:
            for line in data:
                c = SkyCoord(ra = line['RA'], dec = line['DEC'], unit = (u.deg, u.deg), frame='icrs')
                _ra.append(-c.ra.wrap_at(180 * u.deg).radian)
                _dec.append(c.dec.radian)
            database = _databaseconstellation(Table([_ra,_dec], names=['RA','DEC']))
            database.properties(title=name,size=size,color=color,marker=marker,alpha=alpha)
            self.databaselist.append(database)           


    def _cursor(self):
        """
        Set cursor for display
        """
        _ra = []
        _dec = []
        ra=float(self.ra)*15*u.deg
        dec=float(self.dec)*u.deg
        c = SkyCoord(ra, dec, frame='icrs', unit=(u.deg, u.deg))
        _ra.append(-c.ra.wrap_at(180 * u.deg).radian)
        _dec.append(c.dec.radian)
        self.databaselist.append(_database(Table([_ra,_dec], names=['RA','DEC'])))
        
    def _lmc(self):
        """
        Set LMC for display
        """
        lmc = self.sct.lmc
        self._dataaera('LMC',1,'blue','-',0.2,lmc)
        
    def _smc(self):
        """
        Set SMC for display
        """
        smc = self.sct.smc
        self._dataaera('SMC',1,'blue','-',0.2,smc)

    def _milkyway(self):
        """
        Set milkyway for display
        """
        milkyway = self.sct.MilkyWay
        self._dataaera('MilkyWay',1,'blue','-',0.2,milkyway)
        
    def _constellation(self):
        """
        Set constellation for display
        """
        _ra = []
        _dec = []
        constellation = self.sct.constellation
        self._dataconstellation('Cyg',1,'black','--',0.4,constellation)   
    
    def _archive(self,archives):
        """
        Attribut : archives(string): archives fits repository
        """
        archive = self.sct.readarchives(archives)
        self._datacursor('Archives',5,'blue','s',0.2,archive)

    def Moon(self,date,latitude,longitude,elevation):
        """
        Set moon for display
        """
        location = str(longitude) + ' ' + str(latitude) + ' ' + str(elevation)
        moon = self.sct.miriademoon(date,location)
        self._datacursor('Moon',10,'black','o',0.25,moon)
 
    def planning(self,planning):
        """
        Set cursors with planning for display
        """
        self.title = 'Planning projection\n'           
        _ra = []
        _dec = []
        for plan in planning.observations:
            ra,dec = planning.coordinates(plan)
            c = SkyCoord(ra*15*u.deg, dec*u.deg, frame='icrs', unit=(u.deg, u.deg))
            _ra.append(-c.ra.wrap_at(180 * u.deg).radian)
            _dec.append(c.dec.radian) 
        database = _database(Table([_ra,_dec], names=['RA','DEC']))
        database.properties(title='Planning',size=15,color='red',marker='s',alpha=0.2)
        self.databaselist.append(database)   

    def mast(self,mast):
        """
        Set cursors with mast object for display
        """
        self.title = 'Mast projection\n'
        _ra = []
        _dec = []
        for obs in mast.observations:
            ra,dec = mast.coordinates(obs)
            c = SkyCoord(ra*15*u.deg, dec*u.deg, frame='icrs', unit=(u.deg, u.deg))
            _ra.append(-c.ra.wrap_at(180 * u.deg).radian)
            _dec.append(c.dec.radian)
        database = _database(Table([_ra,_dec], names=['RA','DEC']))
        database.properties(title='Mast',size=5,color='green',marker='s',alpha=0.2)
        self.databaselist.append(database)   
        
    @property
    def opencluster(self):
        """
        Create open cluster for display
        """ 
        self.title = 'Open cluster catalog less than magnitude 18\n'
        opc = self.sct.opencluster
        _ra = []
        _dec = []
        for line in opc:
            c = SkyCoord(ra = line['RA'], dec = line['DEC'], unit = (u.deg, u.deg), frame='icrs')
            ra = c.ra*15
            _ra.append(-ra.wrap_at(180 * u.deg).radian)
            _dec.append(c.dec.radian) 
        database = _database(Table([_ra,_dec], names=['RA','DEC']))
        database.properties(title='Open cluster',size=2,color='blue',marker='o',alpha=0.25)
        self.databaselist.append(database)   
 
    @property
    def HerbigAeBe(self):
        """
        Create open cluster for display
        """ 
        self.title = 'Herbig Ae/Be catalog\n'
        opc = self.sct.HerbigAeBeStars
        _ra = []
        _dec = []
        for line in opc:
            c = SkyCoord(ra = line['RA'], dec = line['DEC'], unit = (u.deg, u.deg), frame='icrs')
            _ra.append(-c.ra.wrap_at(180 * u.deg).radian)
            _dec.append(c.dec.radian) 
        database = _database(Table([_ra,_dec], names=['RA','DEC']))
        database.properties(title='Herbig',size=2,color='blue',marker='o',alpha=0.25)
        self.databaselist.append(database)   
 
    @property
    def cepheid(self):
        """
        Create cepheid for display
        """ 
        self.title = 'Cepheid star catalog\n'
        opc = self.sct.CepheidStars
        _ra = []
        _dec = []
        for line in opc:
            c = SkyCoord(ra = line['RA'], dec = line['DEC'], unit = (u.deg, u.deg), frame='icrs')
            ra = c.ra*15
            _ra.append(-c.ra.wrap_at(180 * u.deg).radian)
            _dec.append(c.dec.radian) 
        database = _database(Table([_ra,_dec], names=['RA','DEC']))
        database.properties(title='Cepheid',size=2,color='blue',marker='o',alpha=0.25)
        self.databaselist.append(database)   
        
    def projections(self,RA,DEC,archives):
        """
        Create the archived sectors, cursor, milkyway, lmc, smc, moon for display
        """
        self.title = 'Standard projection\n'
        self.ra = RA
        self.dec = DEC
        self._cursor()
        self._archive(archives)
        self._lmc()
        self._smc()
        self._milkyway()
        self._constellation()

    @property
    def display(self):
        """
        Display projection 
        """              
        fig = plt.figure(figsize=(self.width,self.height))
        ax = fig.add_subplot(projection='aitoff')
        plt.grid(True,axis='both',linestyle='--')
        for database in self.databaselist:
            database.plot()       
        ax.set_xticklabels(['10h','08h','06h','04h','02h','0h','22h','20h','18h','16h','14h'],alpha=0.4)
        ax.set_title(self.title, fontsize = 12)
        plt.show()
