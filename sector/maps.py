"""
Maps class
"""

__authors__ = ("Dominique Touzan","ciboulette module")
__contact__ = ("dtouzan@gmail.com","https://github.com/dtouzan/ciboulette")
__copyright__ = "MIT"
__date__ = "2024-11-27"
__version__= "1.0.0"

# Global mods
import matplotlib.pyplot as plt
# Astropy mods
from astropy.table import Table
from astropy import wcs
#  local mods
from ciboulette.sector import sector
from ciboulette.base import constant


class compoment():
    
        def __init__(self,table):
            self.data = table
            self.title = 'Cursor'
            self.size = 2
            self.color = 'blue'
            self.alpha = 0.8
         
        def properties(self,style=dict()):
            """
            set properties
            """
            self.size = style['size']
            self.color = style['color']
            self.alpha = style['alpha']
       
        def plot(self, axe):
            """
            Plot database
            """
            axe.scatter(self.data['RA'], self.data['DEC'], transform=axe.get_transform('icrs'), s=self.data['MARKER']*10,edgecolor=self.color, facecolor=self.color, alpha=self.alpha)

        @property
        def get(self):
            """
            Return dict of data
            """
            return {'title': self.title, 'data': self.data}


class compoment_constellations(compoment):

        def plot(self,axe):
            """
            Plot database
            """
            axe.scatter(self.data['RA'], self.data['DEC'], transform=axe.get_transform('icrs'), s=2, edgecolor=self.color, facecolor=self.color, alpha=self.alpha)


        @property
        def get(self):
            """
            Return dict of data
            """
            return {'title': self.title, 'data': self.data}


class compoment_cursor(compoment):

        def plot(self,axe):
            """
            Plot database
            """
            axe.scatter(self.data['RA'], self.data['DEC'], transform=axe.get_transform('icrs'), s=self.data['MARKER'], edgecolor='red', linewidths=self.size, facecolor='none', alpha=0.2)


class compoment_scale(compoment):

        def rotation(self, angle=0):
            """
            set angle
            """   
            self.angle = angle
    
        def plot(self,axe):
            """
            Plot database
            """
            label = str(self.data['MARKER'].value[0]) + '°'
            RA, DEC = self.data['RA'].value[0], self.data['DEC'].value[0]
            axe.arrow(RA, DEC, 0, self.data['MARKER'].value[0], head_width=0, head_length=0, fc=self.color, ec=self.color, width=self.size, transform=axe.get_transform('icrs'), alpha=self.alpha)
            plt.text(RA+0.1, DEC+(self.data['MARKER'].value[0]/2), label, color='black', rotation=self.angle, transform=axe.get_transform('icrs'))

class compoment_stars(compoment):

        def plot(self, axe):
            """
            Plot database
            """
            axe.scatter(self.data['RA'], self.data['DEC'], transform=axe.get_transform('icrs'), s=self.data['MARKER'],edgecolor=self.color, facecolor=self.color, alpha=self.alpha)


class Map(object):
    
    def __init__(self):
        self.size = 5
        self.title = ''
        self.databaselist = []
        self.WCS = wcs

    def new(self, table=dict()):
        """
        Set data, WCS for display
            table: {'RA': right ascention heure, 'DEC': declination degre, 'naxis1': naxis1, 'naxis2': naxis2, 'binXY': binning, 'pixelXY': pixel size, 'focal': focal, 'projection': 'TAN'}
        """
        if not table:
            table = {'RA': 0, 'DEC': 0, 'naxis1': 4000, 'naxis2': 3000, 'binXY': 1, 'pixelXY': 1.55, 'focal': 85, 'projection': 'TAN'}

        ra = table['RA']
        dec = table['DEC']
        naxis1 = table['naxis1']
        naxis2 = table['naxis2']
        binXY = table['binXY']
        pixelXY = table['pixelXY']
        focal = table['focal']
        projection = table['projection']    
        sct = sector.Sector()
        self.WCS = sct.WCS(ra,dec,naxis1,naxis2,binXY,pixelXY,focal,projection)
        #field_RA = WCS.wcs.cdelt[0]*self.naxis1
        self.size = self.WCS.wcs.cdelt[1]*naxis2
        self.title = ''
        self.databaselist = []
        return {'coords': (self.WCS.wcs.crval[0], self.WCS.wcs.crval[1]), 'field': self.size}

    
    def marker(self, table=dict(), style=dict()):
        """
        Set marker
            table: {'RA': right ascention heure, 'DEC':declination degre, 'marker': mag, 'source': source_id}
            style: {'color': 'blue', 'size': 2, 'alpha': 0.8}
        """
        if not table:
            table = {'RA': 0, 'DEC': 0, 'marker': 15, 'source': 'marker'}
        if not style:
            style = {'color': 'blue', 'size': 2, 'alpha': 0.8}

        sct = sector.Sector()
        data = compoment(sct.marker(table['RA'], table['DEC'], table['marker'], table['source']))
        if data:
            data.properties(style)
            data.title = 'marker'
            self.databaselist.append(data)      

    
    def constellations(self, table=dict(), style=dict()):
        """
        Set constellations
            table: {'title': 'name'}
            style: {'color': 'green', 'size': 1, 'alpha': 0.4}
        """
        if not table:
            table = {'title': 'CYG'}
        if not style:
            style = {'color': 'green', 'size': 1, 'alpha': 0.4}

        sct = sector.Sector()
        data = compoment_constellations(sct.constellations(table['title']))
        if data:
            data.properties(style)
            data.title = table['title']
            self.databaselist.append(data)      

            
    def gaiaedr3(self, style=dict()):
        """
        Set gaiaedr3 catalog
            style: {'color': 'black', 'size': 0, 'alpha': 0.4}
        """
        if not style:
            style = {'color': 'black', 'size': 1, 'alpha': 1}

        magnitude = 8
        field = self.size

        if field > 5:
            field = 5
        
        if field <= 5:
            magnitude = 8
        if field <= 3:
            magnitude = 12.5
        if field <= 1.5: 
            magnitude = 14.5
        if field <= 0.75:
            magnitude = 16    
        if field <= 0.30:
            mamagnitudeg = 18  
            
        catalog = 'I/350/gaiaedr3'
        sct = sector.Sector()
        data = compoment_stars(sct.regionincatalog(self.WCS.wcs.crval[0], self.WCS.wcs.crval[1], field, field, magnitude, catalog, '_RAJ2000', '_DEJ2000', 'Gmag', 'Source'))   
        if data:
            data.properties(style)
            data.title = 'gaia_edr3'
            self.databaselist.append(data)      

        
    def trajectory(self,target,epoch,epoch_step,epoch_nsteps,latitude,longitude,elevation):
        """
        Set target, WCS and titlefor display
        Attribut:
                target (string)    : Miriade target
                epoch (string)     : Miriade epoch
                epoch_step (string): Miriade epoch_step 
                epoch_nsteps (int) : Miriade epoch_nsteps
                latitude (float)   : Site latitude
                longitude (float)  : Site longitude
                elevation (float)  : Site elevation
        """   
        sct = sector.Sector()
        location = str(longitude) + ' ' + str(latitude) + ' ' + str(elevation)
        self.target = sct.miriadeincatalog(target,epoch,epoch_step,epoch_nsteps,1,location)
        self.title = self.title+target+' | '+epoch.value+'\n'        


    def cursor(self, style=dict()):
        """
        Set cursor map
            style: {'color': 'red', 'size': 5, 'alpha': 0.3}
        """
        if not style:
            style = {'color': 'red', 'size': 5, 'alpha': 0.3}

        table = {'RA': self.WCS.wcs.crval[0]/15, 'DEC': self.WCS.wcs.crval[1], 'marker': 250, 'source': 'cursor'}
        sct = sector.Sector()
        data = compoment_cursor(sct.marker(table['RA'], table['DEC'], table['marker'], table['source']))
        if data:
            data.properties(style)
            data.title = table['source']
            self.databaselist.append(data)      

    
    def scale(self, table=dict(), style=dict()):
        """
        Set scale map
            table: {'RA': right ascention heure, 'DEC':declination degre, 'marker': sise, 'source': 'scale'}
            style: {'color': 'blue', 'size': 2, 'alpha': 0.8, 'rotation': 0}
        """
        if not table:
            table = {'RA': 0, 'DEC': 0, 'marker': 5, 'source': 'scale'}
        if not style:
            style = {'color': 'black', 'size': 1, 'alpha': 0.8, 'rotation': 0}

        sct = sector.Sector()
        data = compoment_scale(sct.marker(table['RA'], table['DEC'], table['marker'], table['source']))
        if data:
            data.properties(style)
            data.title = table['source']
            data.rotation(style['rotation'])
            self.databaselist.append(data) 

            
    def plot(self,axe):
        """
        Plot map
        """
        axe.grid(linestyle = '--', color = 'black', alpha = 0.40)
        for database in self.databaselist:
            database.plot(axe)    

        axe.set_title(self.title, fontsize = 8)
        plt.xlabel(constant.RA_J2000)
        plt.ylabel(constant.DEC_J2000)

        
