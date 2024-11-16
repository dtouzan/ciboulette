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


class compoment():
    
        def __init__(self,table):
            self.data = table
            self.title = 'Cursor'
            self.size = 2
            self.color = 'blue'
            self.marker = 'o'
            self.alpha = 0.8
         
        def properties(self,style=dict()):
            """
            set properties
            """
            self.size = style['size']
            self.color = style['color']
            self.marker = style['marker']
            self.alpha = style['alpha']
       
        def plot(self):
            """
            Plot database
            """
            plt.plot(self.data['RA'], self.data['DEC'],ls='', marker=self.marker, color=self.color, markersize=self.size, alpha=self.alpha)

        @property
        def get(self):
            """
            Return dict of data
            """
            return {'title': self.title, 'RA': self.data['RA'].value, 'DEC': self.data['DEC'].value}


class compoment_cluster(compoment):
    
        def plot(self):
            """
            Plot database
            """
            plt.plot(self.data['RA'], self.data['DEC'],ls='', marker=self.marker, color=self.color, markersize=self.size, alpha=self.alpha)
            plt.plot(self.data['RA'], self.data['DEC'],ls='', marker=self.marker, color='black', markersize=self.size+1, alpha=self.alpha/2)

            
class compoment_constellation(compoment):
    
        def plot(self):
            """
            Plot database
            """
            plt.plot(self.data['RA'], self.data['DEC'], ls=self.marker, color=self.color, lw=self.size, alpha=self.alpha)

class compoment_aera(compoment):
    
        def plot(self):
            """
            Plot database
            """
            plt.plot(self.data['RA'], self.data['DEC'],  ls=self.marker, color=self.color, lw=self.size, alpha=self.alpha)
            plt.fill_between(self.data['RA'],self.data['DEC'], color=self.color, alpha=self.alpha-0.1)           
                

class Projection(object):
        
    def __init__(self,type_projection='aitoff',title=''):
        self.type_projection=type_projection
        self.title = title
        self.width = 8
        self.height = 6
        self.date = Time.now()
        self.databaselist = []
        self.size = 1
        self.color = 'black'
        self.mark = 'dotted'
        self.alpha = 0.2


    def marker(self, table=dict(), style=dict()):
        """
        Set marker
            table: {'title': title, 'RA': right ascention heure, 'DEC':declination degre}
            style: {'marker': 'o', 'color': 'blue', 'size': 2, 'alpha': 0.8}
        """
        if not style:
            style = {'marker': 'o', 'color': 'blue', 'size': 2, 'alpha': 0.8}
        ra = []
        dec = []
        RA=float(table['RA'])*15*u.deg
        DEC=float(table['DEC'])*u.deg       
        c = SkyCoord(RA, DEC, unit = (u.deg, u.deg), frame='icrs')
        ra.append(-c.ra.wrap_at(180 * u.deg).radian)
        dec.append(c.dec.radian)
        data = compoment(Table([ra, dec], names=['RA','DEC']))
        data.properties(style)
        data.title = table['title']
        self.databaselist.append(data)
        
    def cursor(self,table=dict(), style=dict()):
        """
        Create cursor for database
            table: {'title': title, 'RA': right ascention heure, 'DEC':declination degre}
            style: {'marker': '+', 'color': 'red', 'size': 4, 'alpha': 0.8}
        """
        if not style:
            style = {'marker': '+', 'color': 'red', 'size': 4, 'alpha': 0.8}
        self.marker(table, style)      

    def aera(self,name, style, data):
        """
        Create aera for database
        """
        ra = []
        dec = []
        if len(data) > 0:
            for line in data:
                c = SkyCoord(ra = line['RA'], dec = line['DEC'], unit = (u.deg, u.deg), frame='icrs')
                ra.append(-c.ra.wrap_at(180 * u.deg).radian)
                dec.append(c.dec.radian)
            database = compoment_aera(Table([ra,dec], names=['RA','DEC']))
            database.properties(style)
            database.title = name
            self.databaselist.append(database)           

    
    def lmc(self, style=dict()):
        """
        Set LMC for display
            style: {'marker': 'dotted', 'color': 'blue', 'size': 1, 'alpha': 0.25}
        """
        if not style:
            style = {'marker': 'dotted', 'color': 'blue', 'size': 1, 'alpha': 0.25}
        sct = Sct.Sector()
        data = sct.lmc
        self.aera('LMC', style, data)
        
    def smc(self, style=dict()):
        """
        Set SMC for display
            style: {'marker': 'dotted', 'color': 'blue', 'size': 1, 'alpha': 0.25}
        """
        if not style:
            style = {'marker': 'dotted', 'color': 'blue', 'size': 1, 'alpha': 0.25}
        sct = Sct.Sector()
        data = sct.smc
        self.aera('SMC', style, data)

    def milkyway(self, style=dict()):
        """
        Set milkyway for display
            style: {'marker': 'dotted', 'color': 'blue', 'size': 1, 'alpha': 0.2}
        """
        if not style:
            style = {'marker': 'dotted', 'color': 'blue', 'size': 1, 'alpha': 0.2}
        sct = Sct.Sector()
        data = sct.MilkyWay
        self.aera('MilkyWay', style, data)
        

    def constellation(self, table=dict(), style=dict()):
        """
        Set constellation for display
            table: {'title': title, 'RA': right ascention heure, 'DEC':declination degre}
            style: {'marker': 'dotted', 'color': 'green', 'size': 1, 'alpha': 0.4}
        """
        if not style:
            style = {'marker': 'dotted', 'color': 'green', 'size': 1, 'alpha': 0.4}
        sct = Sct.Sector()
        data = sct.constellation
        _ra = []
        _dec = []
        if len(data) > 0:
            for line in data:
                c = SkyCoord(ra = line['RA'], dec = line['DEC'], unit = (u.deg, u.deg), frame='icrs')
                _ra.append(-c.ra.wrap_at(180 * u.deg).radian)
                _dec.append(c.dec.radian)
            database = compoment_constellation(Table([_ra,_dec], names=['RA','DEC']))
            database.properties(style)
            database.title = table['title']
            self.databaselist.append(database)           

    
    def Moon(self,date,latitude,longitude,elevation):
        """
        Set moon for display
        """
        location = str(longitude) + ' ' + str(latitude) + ' ' + str(elevation)
        moon = self.sct.miriademoon(date,location)
        self._datacursor('Moon',10,'black','o',0.25,moon)
 
    
    def mast(self, table=dict(), style=dict()):
        """
        Set marker with mast object for display
            table: {'title': title, 'RA': right ascention heure, 'DEC':declination degre}
            style: {'marker': 's', 'color': 'green', 'size': 5, 'alpha': 0.2}
        """
        if not style:
            style = {'marker': 's', 'color': 'green', 'size': 5, 'alpha': 0.2}
        data = Mast()
        data.read(table['title'])
        _ra = []
        _dec = []
        for obs in data.observations:
            ra,dec = data.coordinates(obs)
            c = SkyCoord(ra*15*u.deg, dec*u.deg, frame='icrs', unit=(u.deg, u.deg))
            _ra.append(-c.ra.wrap_at(180 * u.deg).radian)
            _dec.append(c.dec.radian)
        database = compoment(Table([_ra,_dec], names=['RA','DEC']))
        database.properties(style)
        database.title = table['title']
        self.databaselist.append(database)   
        

    def opencluster(self, style=dict()):
        """
        Create open cluster for display
            style: {'marker': 'o', 'color': 'orange', 'size': 2, 'alpha': 0.4}
        """ 
        if not style:
            style = {'marker': 'o', 'color': 'orange', 'size': 2, 'alpha': 0.4}
        sct = Sct.Sector()
        data = sct.opencluster
        _ra = []
        _dec = []
        for line in data:
            c = SkyCoord(ra = line['RA'], dec = line['DEC'], unit = (u.deg, u.deg), frame='icrs')
            ra = c.ra*15
            _ra.append(-ra.wrap_at(180 * u.deg).radian)
            _dec.append(c.dec.radian) 
        database = compoment_cluster(Table([_ra,_dec], names=['RA','DEC']))
        database.properties(style)
        database.title = 'Open cluster catalog less than magnitude 18'
        self.databaselist.append(database)   
 

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

    
    def properties(self,style=dict()):
        """
        set properties
        """
        if not style:
            style = {'marker': 'dotted', 'color': 'black', 'size': 1, 'alpha': 0.2}
        self.size = style['size']
        self.color = style['color']
        self.mark = style['marker']
        self.alpha = style['alpha']


    def plot(self,axe):
        """
        Display projection 
        """ 
        plt.grid(True,axis='both',color= self.color, linestyle=self.mark, linewidth=self.size, alpha=self.alpha)
        for database in self.databaselist:
            database.plot()       
        axe.set_xticklabels(['10h','08h','06h','04h','02h','0h','22h','20h','18h','16h','14h'],alpha=self.alpha+0.1)
        axe.set_title(self.title, fontsize = 8)
