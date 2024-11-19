"""
Maps class
"""

import matplotlib.pyplot as plt
from astropy.table import Table
from astropy import wcs
from ciboulette.sector import sector
from ciboulette.base import constant

class Map(object):
    
    def __init__(self,size=15):
        self.size = size
        self.title = ''
        self.data = Table()
        self.databaselist = []
        self.WCS = wcs
        self.target = Table()

    def new(self,ra,dec,naxis1,naxis2,binXY,pixelXY,focal,projection='TAN'):
        """
        Set data, WCS for display
        """
        sct = sector.Sector()
        self.WCS = sct.WCS(ra,dec,naxis1,naxis2,binXY,pixelXY,focal,projection)
        #field_RA = WCS.wcs.cdelt[0]*self.naxis1
        field = self.WCS.wcs.cdelt[1]*naxis2
        self.size = 15
        self.title = ''
        self.databaselist = []
        return {'field': field}

    def marker(self, ra=0, dec=0, mag=12, source=''):
        """
        Set data, WCS for display
        """
        sct = sector.Sector()
        data = sct.marker(ra, dec, mag, source)
        self.databaselist.append(data)
        
    def constellations(self, table=dict()):
        sct = sector.Sector()
        data = sct.constellations(table['title'])
        ra = []
        dec = []
        node = []
        if len(data) > 0:
            self.databaselist.append(data)      

            
    def gaiaedr3(self,ra,dec,naxis1,naxis2,binXY,pixelXY,focal):
        """
        Set data, WCS for display
        """
        sct = sector.Sector()
        self.WCS = sct.WCS(ra,dec,naxis1,naxis2,binXY,pixelXY,focal)
        #field_RA = WCS.wcs.cdelt[0]*self.naxis1
        field = self.WCS.wcs.cdelt[1]*naxis2
        mag = 8

        if field > 5:
            field = 5
        
        if field <= 5:
            mag = 8
        if field <= 3:
            mag = 12.5
        if field <= 1.5: 
            mag = 14.5
        if field <= 0.75:
            mag = 16    
        if field <= 0.30:
            mag = 18  
            
        catalog = 'I/350/gaiaedr3'
        self.data = sct.regionincatalog(ra*15, dec,field,field,mag,catalog,'_RAJ2000', '_DEJ2000', 'Gmag', 'Source')   
        #resolv = str("%.2f" %(206*pixelXY/focal))
        return {'field': field, 'mag': mag}
        
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

    @property
    def cursor(self):
        """
        Add cursor map
        """
        self.marker(self.WCS.wcs.crval[0]/15, self.WCS.wcs.crval[1], mag=1, source='cursor')

        
    def plot(self,axe):
        """
        Plot map
        """
        axe.grid(linestyle = '--', color = 'black', alpha = 0.40)
        if len(self.data) > 0:
            axe.scatter(self.data['RA'], self.data['DEC'], transform=axe.get_transform('icrs'), s=self.data['MARKER'],edgecolor='black', facecolor='black')
        axe.set_title(self.title, fontsize = 8)
        plt.xlabel(constant.RA_J2000)
        plt.ylabel(constant.DEC_J2000)

    def ploting(self, axe):
        axe.grid(linestyle = '--', color = 'black', alpha = 0.40)
        
        for data in self.databaselist:
                if 'MARKER' in data.colnames: 
                    if 'cursor' in data['SOURCE_ID']:
                        axe.scatter(data['RA'], data['DEC'], transform=axe.get_transform('icrs'), s=250, edgecolor='red', linewidths=5, facecolor='none', alpha=0.2)
                    else:
                        axe.scatter(data['RA'], data['DEC'], transform=axe.get_transform('icrs'), s=data['MARKER'],edgecolor='black', facecolor='black')
                if 'MAIN_ID' in data.colnames:
                    axe.scatter(data['RA'], data['DEC'], transform=axe.get_transform('icrs'), s=2, edgecolor='red', facecolor='red', alpha=0.3)
                    
        axe.set_title(self.title, fontsize = 8)
        plt.xlabel(constant.RA_J2000)
        plt.ylabel(constant.DEC_J2000)
        
