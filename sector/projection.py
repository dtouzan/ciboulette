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

class Projection(object):
        
    def __init__(self,size=10,title=''):
            self.data = []
            self.title = title
            self.size = size
            self.ra = 0
            self.dec = 0
            self.sct = Sct.Sector()
            self.archive = Table()
            self.cursor = Table()
            self.moon = Table()
            self.lmc = Table()
            self.smc = Table()
            self.milkyway = Table()
            self.catalog = Table()
    
    def _cursor(self):
        _ra = []
        _dec = []
        ra=float(self.ra)*15*u.deg
        dec=float(self.dec)*u.deg
        c = SkyCoord(ra, dec, frame='icrs', unit=(u.deg, u.deg))
        _ra.append(-c.ra.wrap_at(180 * u.deg).radian)
        _dec.append(c.dec.radian)
        self.cursor = Table([_ra,_dec], names=['RA','DEC'])

    def _moon(self,latitude,longitude,elevation):
        _ra = []
        _dec = []
        _marker = []
        location = str(longitude) + ' ' + str(latitude) + ' ' + str(elevation)
        moon = self.sct.miriademoon(location)
        for line in moon:
            c = SkyCoord(ra = line['RA'], dec = line['DEC'], unit = (u.deg, u.deg), frame='icrs')
            _ra.append(-c.ra.wrap_at(180 * u.deg).radian)
            _dec.append(c.dec.radian)
            _marker.append(line['MARKER'])
        self.moon = Table([_ra,_dec,_marker], names=['RA','DEC','MARKER'])

    def _lmc(self):
        _ra = []
        _dec = []
        lmc = self.sct.lmc
        for line in lmc:
            c = SkyCoord(ra = line['RA'], dec = line['DEC'], unit = (u.deg, u.deg), frame='icrs')
            _ra.append(-c.ra.wrap_at(180 * u.deg).radian)
            _dec.append(c.dec.radian)
        self.lmc = Table([_ra,_dec], names=['RA','DEC'])
    
    def _smc(self):
        _ra = []
        _dec = []
        smc = self.sct.smc
        for line in smc:
            c = SkyCoord(ra = line['RA'], dec = line['DEC'], unit = (u.deg, u.deg), frame='icrs')
            _ra.append(-c.ra.wrap_at(180 * u.deg).radian)
            _dec.append(c.dec.radian)
        self.smc = Table([_ra,_dec], names=['RA','DEC'])

    def _milkyway(self):
        _ra = []
        _dec = []
        milkyway = self.sct.MilkyWay
        for line in milkyway:
            c = SkyCoord(ra = line['RA'], dec = line['DEC'], unit = (u.deg, u.deg), frame='icrs')
            _ra.append(-c.ra.wrap_at(180 * u.deg).radian)
            _dec.append(c.dec.radian)
        self.milkyway = Table([_ra,_dec], names=['RA','DEC'])
    
    def _archive(self,archives):
        """
        Attribut : archives(string): répertoire des archives fits
        """
        _ra = []
        _dec = []
        archive = self.sct.readarchives(archives)
        for line in archive:
            c = SkyCoord(ra = line['RA'], dec = line['DEC'], unit = (u.deg, u.deg), frame='icrs')
            _ra.append(-c.ra.wrap_at(180 * u.deg).radian)
            _dec.append(c.dec.radian)
        self.archive = Table([_ra,_dec], names=['RA','DEC'])

    def projections(self,RA,DEC,archives,latitude,longitude,elevation):
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
        self._moon(latitude,longitude,elevation)
    
    @property
    def opencluster16(self):
        """
        Create open cluster for display
        """ 
        self.title = 'Open cluster catalog less than magnitude 18\n'
        opc = self.sct.opencluster16
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
        moon_marker = self.moon['MARKER']
        
        fig = plt.figure(figsize=(self.size,self.size))
        ax = fig.add_subplot(111,projection='aitoff')
        plt.grid(True,axis='both',linestyle='--')
        plt.plot(self.milkyway['RA'], self.milkyway['DEC'], color='blue', lw=1, alpha=0.2)
        plt.fill_between(self.milkyway['RA'],self.milkyway['DEC'], color='blue', alpha=0.1)  
        plt.plot(self.smc['RA'], self.smc['DEC'], color='blue', lw=1, alpha=0.2)
        plt.fill_between(self.smc['RA'],self.smc['DEC'], color='blue', alpha=0.1)        
        plt.plot(self.lmc['RA'], self.lmc['DEC'], color='blue', lw=1, alpha=0.2)
        plt.fill_between(self.lmc['RA'],self.lmc['DEC'], color='blue', alpha=0.1)  
        if len(self.catalog) > 0:
            plt.plot(self.catalog['RA'],self.catalog['DEC'], 'o', color='blue', markersize=2, alpha=0.25)    
        plt.plot(self.moon['RA'],self.moon['DEC'], 'o', color='black', markersize=moon_marker, alpha=0.25)        
        if len(self.archive) > 0:
            plt.plot(self.sector['RA'], self.sector['DEC'], 's', color='green', markersize=5, alpha=0.2)   
        plt.plot(self.cursor['RA'], self.cursor['DEC'], 's', color='red', markersize=5, alpha=0.4)
        ax.set_xticklabels(['10h','08h','06h','04h','02h','0h','22h','20h','18h','16h','14h'],alpha=0.4)
        ax.set_title(self.title, fontsize = 12)
        plt.show()
