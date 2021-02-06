"""Ciboulette class

"""

from astropy.io import fits
from astropy.table import Table


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
    filter_name = 'CLS'
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