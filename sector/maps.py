"""
Maps class
"""

import matplotlib.pyplot as plt
from astropy.table import Table
from astropy import wcs
from ciboulette.sector import sector 

class Map(object):
    
    def __init__(self,size=15):
        self.size = size
        self.title = ''
        self.data = Table()
        self.WCS = wcs
        self.target = Table()
   
    def stars(self,ra,dec,naxis1,naxis2,binXY,pixelXY,focal,instrument,telescope_name,observer_name,filter_name):
        """
        Set data, WCS and title for display
        Attribut : 
                ciboulette (object): Ciboulette class
        """
        sct = sector.Sector()
        self.WCS = sct.WCS(ra,dec,naxis1,naxis2,binXY,pixelXY,focal)
        #field_RA = WCS.wcs.cdelt[0]*self.naxis1
        field = self.WCS.wcs.cdelt[1]*naxis2
        mag = 11
        if field <= 3:
            mag = 14
        if field <= 1:
            mag = 18
        catalog = 'GAIA-EDR3'
        self.data = sct.regionincatalog(ra*15, dec,field,field,mag,catalog,'_RAJ2000', '_DEJ2000', 'Gmag')   
        self.title = self.title+'VizieR-'+catalog+' | F'+str(focal)+' | '+instrument+' | '+telescope_name+' | '+observer_name+' | '+filter_name+'\n'
        
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
    def display(self):
        """
        Display map
        """
        fig = plt.figure(figsize=(self.size,self.size))
        ax = fig.add_subplot(111, projection=self.WCS)
        ax.grid(b = True, linestyle = '--', color = 'black', alpha = 0.40)
        if len(self.data) > 0:
            ax.scatter(self.data['RA'], self.data['DEC'], transform=ax.get_transform('icrs'), s=self.data['MARKER'],edgecolor='black', facecolor='black')
        if len(self.target) > 0:
            ax.plot(self.target['RA'], self.target['DEC'], transform=ax.get_transform('icrs'), lw=3)
        fig.suptitle(self.title, y = 0.92, fontsize = 12)
        plt.xlabel(constent.RA_J2000)
        plt.ylabel(constent.DEC_J2000)
        plt.show()