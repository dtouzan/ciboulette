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
        self.WCS = wcs
        self.target = Table()
   
    def stars(self,ra,dec,naxis1,naxis2,binXY,pixelXY,focal,instrument,telescope_name,observer_name,filter_name):
        """
        Set data, WCS and title for display
        """
        sct = sector.Sector()
        self.WCS = sct.WCS(ra,dec,naxis1,naxis2,binXY,pixelXY,focal)
        #field_RA = WCS.wcs.cdelt[0]*self.naxis1
        field = self.WCS.wcs.cdelt[1]*naxis2
        mag = 9
    
        if field >= 1.5:
            field = 1.5
            mag = 12.5
        if field < 1.5:   
            mag = 14.5
        if field < 0.75:   
            mag = 16    
        if field < 0.30:  
            mag = 18    

        catalog = 'GAIA-EDR3'
        self.data = sct.regionincatalog(ra*15, dec,field,field,mag,catalog,'_RAJ2000', '_DEJ2000', 'Gmag')   
        resolv = str("%.2f" %(206*pixelXY/focal))
        self.title = self.title+'VizieR-'+catalog+' | F'+str(focal)+' | '+instrument+' | '+telescope_name+' | '+observer_name+' | '+filter_name+' | '+resolv+ '"/p'+ ':Mv '+str(mag) +'\n'
        
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
    
    def plot(self,axe):
        """
        Plot map
        """
        #fig = plt.figure(figsize=(self.size,self.size))
        #axe = fig.add_subplot(111, projection=self.WCS)
        axe.grid(b = True, linestyle = '--', color = 'black', alpha = 0.40)
        if len(self.data) > 0:
            axe.scatter(self.data['RA'], self.data['DEC'], transform=axe.get_transform('icrs'), s=self.data['MARKER'],edgecolor='black', facecolor='black')
        if len(self.target) > 0:
            axe.plot(self.target['RA'], self.target['DEC'], transform=ax.get_transform('icrs'), lw=3)
        axe.scatter(self.WCS.wcs.crval[0], self.WCS.wcs.crval[1], transform=axe.get_transform('icrs'), s=50,edgecolor='red', linewidths=2, facecolor=None, alpha=0.6)
        #fig.suptitle(self.title, y = 0.92, fontsize = 12)
        axe.set_title(self.title, fontsize = 8)
        plt.xlabel(constant.RA_J2000)
        plt.ylabel(constant.DEC_J2000)
        #plt.show()
