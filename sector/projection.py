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

class Projection(object):
        
    def __init__(self,size=10,title=''):
            self.title = title
            self.size = size
            self.cursorsize = 15
            self.ra = 0
            self.dec = 0
            self.date = Time.now()
            self.sct = Sct.Sector()
            self.archive = Table()
            self.cursor = Table()
            self.moon = Table()
            self.lmc = Table()
            self.smc = Table()
            self.milkyway = Table()
            self.constellation = Table()
            self.catalog = Table()
    
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
        self.cursor = Table([_ra,_dec,['o'],['blue'],[5]], names=['RA','DEC','Marker','Color','Size'])
    
    def _lmc(self):
        """
        Set LMC for display
        """
        _ra = []
        _dec = []
        lmc = self.sct.lmc
        for line in lmc:
            c = SkyCoord(ra = line['RA'], dec = line['DEC'], unit = (u.deg, u.deg), frame='icrs')
            _ra.append(-c.ra.wrap_at(180 * u.deg).radian)
            _dec.append(c.dec.radian)
        self.lmc = Table([_ra,_dec], names=['RA','DEC'])
    
    def _smc(self):
        """
        Set SMC for display
        """
        _ra = []
        _dec = []
        smc = self.sct.smc
        for line in smc:
            c = SkyCoord(ra = line['RA'], dec = line['DEC'], unit = (u.deg, u.deg), frame='icrs')
            _ra.append(-c.ra.wrap_at(180 * u.deg).radian)
            _dec.append(c.dec.radian)
        self.smc = Table([_ra,_dec], names=['RA','DEC'])

    def _milkyway(self):
        """
        Set milkyway for display
        """
        _ra = []
        _dec = []
        milkyway = self.sct.MilkyWay
        for line in milkyway:
            c = SkyCoord(ra = line['RA'], dec = line['DEC'], unit = (u.deg, u.deg), frame='icrs')
            _ra.append(-c.ra.wrap_at(180 * u.deg).radian)
            _dec.append(c.dec.radian)
        self.milkyway = Table([_ra,_dec], names=['RA','DEC'])

    def _constellation(self):
        """
        Set constellation for display
        """
        _ra = []
        _dec = []
        constellation = self.sct.constellation
        for line in constellation:
            c = SkyCoord(ra = line['RA'], dec = line['DEC'], unit = (u.deg, u.deg), frame='icrs')
            _ra.append(-c.ra.wrap_at(180 * u.deg).radian)
            _dec.append(c.dec.radian)
        self.constellation = Table([_ra,_dec], names=['RA','DEC']) 
    
    def _archive(self,archives):
        """
        Attribut : archives(string): archives fits repository
        """
        _ra = []
        _dec = []
        archive = self.sct.readarchives(archives)
        for line in archive:
            c = SkyCoord(ra = line['RA'], dec = line['DEC'], unit = (u.deg, u.deg), frame='icrs')
            _ra.append(-c.ra.wrap_at(180 * u.deg).radian)
            _dec.append(c.dec.radian)
        self.archive = Table([_ra,_dec], names=['RA','DEC'])

    def Moon(self,date,latitude,longitude,elevation):
        """
        Set moon for display
        """
        _ra = []
        _dec = []
        _marker = []
        location = str(longitude) + ' ' + str(latitude) + ' ' + str(elevation)
        moon = self.sct.miriademoon(date,location)
        for line in moon:
            c = SkyCoord(ra = line['RA'], dec = line['DEC'], unit = (u.deg, u.deg), frame='icrs')
            _ra.append(-c.ra.wrap_at(180 * u.deg).radian)
            _dec.append(c.dec.radian)
            _marker.append(line['MARKER'])
        self.moon = Table([_ra,_dec,_marker], names=['RA','DEC','MARKER'])

    def projections(self,RA,DEC,archives):
        """
        Create the archived sectors, cursor, milkyway, lmc, smc, moon for display
        """
        self.title = 'Standard projection'
        self.ra = RA
        self.dec = DEC
        self._cursor()
        self._archive(archives)
        self._lmc()
        self._smc()
        self._milkyway()
        self._constellation()

    def planning(self,planning):
        """
        Set cursors with planning
        """
        self.title = 'Planning projection'           
        for plan in planning.observations:
            ra,dec = planning.coordinates(plan)
            c = SkyCoord(ra*15*u.deg, dec*u.deg, frame='icrs', unit=(u.deg, u.deg))
            _ra = -c.ra.wrap_at(180 * u.deg).radian
            _dec = c.dec.radian
            self.cursor.add_row([_ra,_dec,'s','red',15])       
            
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
        self.catalog = Table([_ra,_dec], names=['RA','DEC'])
 
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
        self.catalog = Table([_ra,_dec], names=['RA','DEC'])
 
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
        self.catalog = Table([_ra,_dec], names=['RA','DEC'])
 
    @property
    def display(self):
        """
        Display projection 
        """              
        fig = plt.figure(figsize=(self.size,self.size))
        ax = fig.add_subplot(111,projection='aitoff')
        plt.grid(True,axis='both',linestyle='--')
        plt.plot(self.milkyway['RA'], self.milkyway['DEC'], color='blue', lw=1, alpha=0.2)
        plt.fill_between(self.milkyway['RA'],self.milkyway['DEC'], color='blue', alpha=0.1)  
        plt.plot(self.smc['RA'], self.smc['DEC'], color='blue', lw=1, alpha=0.2)
        plt.fill_between(self.smc['RA'],self.smc['DEC'], color='blue', alpha=0.1)        
        plt.plot(self.lmc['RA'], self.lmc['DEC'], color='blue', lw=1, alpha=0.2)
        plt.plot(self.constellation['RA'], self.constellation['DEC'], '--', color='black', lw=1, alpha=0.4)
        plt.fill_between(self.lmc['RA'],self.lmc['DEC'], color='blue', alpha=0.1)  
        if len(self.catalog) > 0:
            plt.plot(self.catalog['RA'],self.catalog['DEC'], 'o', color='blue', markersize=2, alpha=0.25)    
        if len(self.moon) >0:
            moon_marker = self.moon['MARKER']
            plt.plot(self.moon['RA'],self.moon['DEC'], 'o', color='black', markersize=moon_marker, alpha=0.25)        
        if len(self.archive) > 0:
            plt.plot(self.archive['RA'], self.archive['DEC'], 's', color='green', markersize=5, alpha=0.2) 
        plt.plot(self.cursor['RA'], self.cursor['DEC'], 's', color='red', markersize=15, alpha=0.2)
        plt.plot(self.cursor['RA'][0], self.cursor['DEC'][0], 's', color='blue', markersize=5, alpha=0.2)
        ax.set_xticklabels(['10h','08h','06h','04h','02h','0h','22h','20h','18h','16h','14h'],alpha=0.4)
        ax.set_title(self.title, fontsize = 12)
        plt.show()
