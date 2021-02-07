"""Ciboulette class

"""

from astropy.io import fits
from astropy.table import Table
from astropy.coordinates import SkyCoord, Angle
from astropy import units as u
import matplotlib.pyplot as plt
from ciboulette.sector import sectorpy as Sct
from astropy import wcs


class Ciboulette :

    driver_name = 'FITS astropy 4.2'
    server = '192.168.1.18:11111'
    device = 0
    focale = 85.0
    site_lat = 49.5961
    site_long = -0.3531
    site_elev = 100
    instrument = 'Atik 383L+'
    naxis1 = 3326
    naxis2 = 2504
    binXY = 1
    pixelXY = 5.4
    filter_name = 'L'
    telescope_name = 'CIBOULETTE-A'
    observer_name = 'CAM1'
    dataset = '/home/dataset'
    archive_table = '/home/dataset/archives'
    ra = 0.0 # hours
    dec = 90.0 # degrees
    object_name = 'INIT'
        
    def __init__(self):
        
        self.data = []

    
    def ciboulettetable(self):
        """Return table of ciboulette values
        
        """
    
        tdriver_name = [self.driver_name]                        # Astropy driver
        tserver = [self.server]                                  # Server IP:port
        tdevice = [self.device]                                  # Device for alpaca
        tfocale = [self.focale]                                  # Focal millimeter
        tsite_lat = [self.site_lat]                              # Site latitude degrees
        tsite_long = [self.site_long]                            # Site longitude degrees
        tsite_elev = [self.site_elev]                            # Site elevation meter
        tinstrument = [self.instrument]                          # Instrument name
        tnaxis1 = [self.naxis1]                                  # Size naxis1
        tnaxis2 = [self.naxis2]                                  # Size naxis2
        tbinXY = [self.binXY]                                    # Binning
        tpixelXY = [self.pixelXY]                                # Pixel size X and Y
        tfilter_name = [self.filter_name]                        # Filter name
        ttelescope_name = [self.telescope_name]                  # Telescope name
        tobserver_name = [self.observer_name]                    # Observer name
        tdataset = [self.dataset]                                # Dataset repository
        tarchive_table = [self.archive_table]                    # Archives repository
        tra = [self.ra]                                          # Hours
        tdec = [self.dec]                                        # Degrees
        tobject_name = [self.object_name]                        # Object name
        
        return Table([tdriver_name,tserver,tdevice,tfocale,tsite_lat,tsite_long,tsite_elev,tinstrument,tnaxis1,tnaxis2,
                      tbinXY,tpixelXY,tfilter_name,ttelescope_name,tobserver_name,tdataset,tarchive_table,tra,tdec,tobject_name], 
                      names=['DRV_NAME','SERVER','DEVICE','FOCAL','SITE_LAT','SITE_LONG','SITE_ELEV','INSTRUME','NAXIS1','NAXIS2',
                         'BINXY','PIXELXY','FILTER','NAME','OBSERVER','DATASET','ARCHIVES','RA','DEC','OBECT'])


    def ephemccgetobserver(self):
        """Return site ephemcc format
            Ex.: -0.3531%2049.5961%20100.0
        
        """
        
        key_space = '%20'     
        
        return  str(self.site_long)+key_space+str(self.site_lat)+key_space+str(self.site_elev)
    

    def projections(self,sector_arch):
        """Displays the archived sectors, RA and DEC on an aitoff projection
        
        Attributes:
                sector_arch (Table): sector table.
        
        """
     
        # Read archive table
        value_quadran_ra = []
        value_quadran_dec = []
    
        for line in sector_arch:
        
            # RA and DEC in degrees
            value_RA_quadran = float(line['RA'])*u.deg
            value_DEC_quadran = float(line['DEC'])*u.deg
            # ICRS configuration
            c = SkyCoord(value_RA_quadran, value_DEC_quadran, frame='icrs')
            # RA and DEC in radian
            value_quadran_ra.append(-c.ra.wrap_at(180 * u.deg).radian)
            value_quadran_dec.append(c.dec.radian)

        value_ra_graph = []
        value_dec_graph = []
        value_color_graph = []
        title =''
    
        # RA and DEC in degrees
        ra=float(self.ra)*15*u.deg
        dec=float(self.dec)*u.deg

        # ICRS configuration
        c = SkyCoord(ra, dec, frame='icrs', unit=(u.deg, u.deg))
        # RA and DEC in radian
        value_ra = -c.ra.wrap_at(180 * u.deg).radian
        value_dec= c.dec.radian

        title = self.telescope_name + ' | ' + self.observer_name + ' | ' + self.filter_name + '\n'

        # Display configuration
        fig = plt.figure(figsize=(7,7))
        # Configuration de la projecion cartographique du titre et grille 
        ax = fig.add_subplot(111,projection='aitoff')
        plt.grid(True,axis='both',linestyle='--')

        # Projection drawing
        if len(sector_arch) > 0:
            plt.plot(value_quadran_ra, value_quadran_dec, 's', color='green', markersize=5, alpha=0.2) 
  
        plt.plot(value_ra, value_dec, 's', color='red', markersize=5, alpha=0.4)

        # Modification of labels in hours
        ax.set_xticklabels(['10h','08h','06h','04h','02h','0h','22h','20h','18h','16h','14h'],alpha=0.4)
        ax.set_title(title, fontsize = 12)
        # Display
        plt.show()
        
        
    def starmap(self):
        """Displays the stars map with maximal magnitude 12
        
        """

        RA_deg = self.ra*15
        DEC_deg = self.dec
      
        # Element for CRPIX
        crpix1 = int(self.naxis1)/2
        crpix2 = int(self.naxis2)/2

        # Element for CDELT
        cdelt1 = (206*int(self.pixelXY)*int(self.binXY)/self.focale)/3600
        cdelt2 = (206*int(self.pixelXY)*int(self.binXY)/self.focale)/3600

        # Header WCS
        w = wcs.WCS(naxis=2)
        w.wcs.ctype = ["RA---TAN", "DEC--TAN"]
        # CRVAL 
        w.wcs.crval = [RA_deg, DEC_deg] 
        # CRPIX Vecteur à 2 éléments donnant les coordonnées X et Y du pixel de référence 
        # (def = NAXIS / 2) dans la convention FITS (le premier pixel est 1,1)
        w.wcs.crpix = [crpix1, crpix2]
        # CDELT Vecteur à 2 éléments donnant l'incrément physique au pixel de référence
        w.wcs.cdelt = [-cdelt1, cdelt2]   
    
        sct = Sct.Sector()
        field_RA = cdelt1*self.naxis1
        field_DEC= cdelt2*self.naxis2
        field_RA = 1.5
        field_DEC= 1.5
        mag = 12
        catalog = 'GSC2.3'
        data_field = sct.regionincatalog(RA_deg, DEC_deg,field_RA,field_DEC,mag,catalog,'_RAJ2000', '_DEJ2000', 'Vmag')
    
        title = 'VizieR-' + catalog + ' | ' + 'F'+str(self.focale) + ' | ' +  self.instrument
    
        fig = plt.figure(figsize=(7,7))
        ax = fig.add_subplot(111, projection=w)
        ax.grid(b = True, linestyle = '--', color = 'black', alpha = 0.40)
        ax.scatter(data_field['RA'], data_field['DEC'], transform=ax.get_transform('icrs'), s=data_field['MARKER'],edgecolor='black', facecolor='black')
        fig.suptitle(title, y = 0.92, fontsize = 12)
        plt.xlabel('RA')
        plt.ylabel('Dec')
        # Display
        plt.show()