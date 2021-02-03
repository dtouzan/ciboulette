"""Ciboulette class

"""

from astropy.io import fits
from astropy.table import Table


class ciboulette :

    driver_name = 'FITS astropy 4.2'
    server = '192.168.1.18:11111'
    device = 0
    focale = 100.0
    site_lat = 49.5961
    site_long = -0.3531
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
        
    def __init__(self) :
        
        self.data = []

    
    def ciboulettetable(self):
    
        tdriver_name = [self.driver_name]
        tserver = [self.server]
        tdevice = [self.device]
        tfocale = [self.focale]
        tsite_lat = [self.site_lat]
        tsite_long = [self.site_long]
        tinstrument = [self.instrument]
        tnaxis1 = [self.naxis1]
        tnaxis2 = [self.naxis2]
        tbinXY = [self.binXY]
        tpixelXY = [self.pixelXY]
        tfilter_name = [self.filter_name]
        ttelescope_name = [self.telescope_name]
        tobserver_name = [self.observer_name]
        tdataset = [self.dataset]
        tarchive_table = [self.archive_table]
        tra = [self.ra]                                          # hours
        tdec = [self.dec]                                        # degrees
        tobject_name = [self.object_name]
        
        return Table([tdriver_name,tserver,tdevice,tfocale,tsite_lat,tsite_long,tinstrument,tnaxis1,tnaxis2,
                      tbinXY,tpixelXY,tfilter_name,ttelescope_name,tobserver_name,tdataset,tarchive_table,tra,tdec,tobject_name], 
                      names=['DRV_NAME','SERVER','DEVICE','FOCAL','SITE_LAT','SITE_LONG','INSTRUME','NAXIS1','NAXIS2',
                         'BINXY','PIXELXY','FILTER','NAME','OBSERVER','DATASET','ARCHIVES','RA','DEC','OBECT'])

