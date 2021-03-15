"""
Ciboulette class
"""

import time
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.time import Time
from astropy.table import Table
from astropy.coordinates import SkyCoord, Angle
from astropy import units as u
from astropy import wcs
from astropy.io.votable import parse_single_table
from astropy.utils.data import get_pkg_data_filename
from astroquery.simbad import Simbad
from alpaca import Telescope, Camera, FilterWheel
from ciboulette.base import constent
from ciboulette.sector import sector as Sct
from ciboulette.utils import exposure as Exp
from ciboulette.utils import planning as Pln

class Ciboulette(object):
        
    def __init__(self):
        self.data = []
        self.api_version = constent.API_version
        self.server = '192.168.1.18'
        self.port = 11111
        self.device = 0
        self.focal = 85.0
        self.diameter = 60
        self.latitude = 49.5961
        self.longitude = 359.65
        self.elevation = 100
        self.instrument = 'Atik 383L+'
        self.naxis1 = 3326
        self.naxis2 = 2504
        self.binXY = 1
        self.pixelXY = 5.4
        self.filter_name = 'L'
        self.telescope_name = 'CIBOULETTE-A'
        self.observer_name = 'CAM1'
        self.dataset = 'dataset'
        self.archive_table = 'dataset/archives'
        self.ra = 0.0 # hours
        self.dec = 90.0 # degrees
        self.object_name = 'INIT'
        self._date = '2021-01-01T00:00:00'
        self._temperature = 0
        self._exp_time = 0
        self._frameid = 0
        self._datatype = ''
        self._pressure = 0
        self._humidity  = 0
        self._temperature  = 0
        self._description = 'Observatory UT1, 10 route de la mare maury, France. @' + str(self.latitude) + ',' + str(self.longitude) + ',' + str(self.elevation) + 'm'

    @property
    def table(self):
        """
        Return table of ciboulette values
        """
    
        api = [self.api_version]                                # Astropy API
        server = [self.server + ':' + str(self.port)]           # Server IP:port
        device = [self.device]                                  # Device for alpaca
        focal = [self.focal]                                    # Focal millimeter
        diameter = [self.diameter]                              # Diameter millimeter
        latitude = [self.latitude]                              # Site latitude degrees
        longitude = [self.longitude]                            # Site longitude degrees
        elevation = [self.elevation]                            # Site elevation meter
        instrument = [self.instrument]                          # Instrument name
        naxis1 = [self.naxis1]                                  # Size naxis1
        naxis2 = [self.naxis2]                                  # Size naxis2
        binXY = [self.binXY]                                    # Binning
        pixelXY = [self.pixelXY]                                # Pixel size X and Y
        filter_name = [self.filter_name]                        # Filter name
        telescope_name = [self.telescope_name]                  # Telescope name
        observer_name = [self.observer_name]                    # Observer name
        dataset = [self.dataset]                                # Dataset repository
        archive_table = [self.archive_table]                    # Archives repository
        ra = [self.ra]                                          # Hours
        dec = [self.dec]                                        # Degrees
        object_name = [self.object_name]                        # Object name
        
        return Table([api,server,device,focal,diameter,latitude,longitude,elevation,instrument,naxis1,naxis2,
                      binXY,pixelXY,filter_name,telescope_name,observer_name,dataset,archive_table,ra,dec,object_name], 
                      names=['API','SERVER','DEVICE','FOCAL','DIAM','SITE_LAT','SITE_LONG','SITE_ELEV','INSTRUME','NAXIS1','NAXIS2',
                         'BINXY','PIXELXY','FILTER','NAME','OBSERVER','DATASET','ARCHIVES','RA','DEC','OBJECT'])  

    @property
    def serverport(self):
        """
        Return Server:port configuration
        """
        return self.server + ':' + str(self.port)

    @serverport.setter
    def serverport(self,serverdict):
        """
        Set server and port
         serverdict:
         {
            "SVR": string - Server 
            "PORT": int - Port
          }
        """  
        self.server = str(serverdict['SVR'])
        self.port = int(serverdict['PORT'])
                
    @property
    def atik383L(self):
        """
        Set Atik383L+ configuration
        """
        self.instrument = 'Atik 383L+'
        self.naxis1 = 3326
        self.naxis2 = 2504
        self.pixelXY = 5.4
    
    @property
    def atiktitan(self):
        """
        Set Atik Titan configuration
        """
        self.instrument = 'Atik Titan'
        self.naxis1 = 659
        self.naxis2 = 494
        self.pixelXY = 7.4       
    
    @property
    def asi120(self):
        """
        Set ASI 120 configuration
        """
        self.instrument = 'ASI 120'
        self.naxis1 = 1280
        self.naxis2 = 960
        self.pixelXY = 3.75       

    @property
    def samyang85_1_4(self):
        """
        Set Samyang 85mm F1.4 configuration
        """
        self.focal = 85
        self.diameter = 60

    @property
    def canon200_2_8(self):
        """
        Set Canon 200mm F2.8 configuration
        """
        self.focal = 200
        self.diameter = 71

    @property
    def sigma120_400(self):
        """
        Set Sigma 120-400 configuration 120mm
        """
        self.focal = 120
        self.diameter = 71

    @sigma120_400.setter
    def sigma120_400(self,f):
        """
        Set Sigma 120-400 configuration
        """
        if f >= 120 and f <= 400:
            self.focal = f
            self.diameter = 71
            
    @property
    def lens70_300(self):
        """
        Set 70-300 configuration 70mm
        """
        self.focal = 70
        self.diameter = 53

    @lens70_300.setter
    def lens70_300(self,f):
        """
        Set Sigma 120-400 configuration
        """
        if f >= 70 and f <= 300:
            self.focal = f
            self.diameter = 53
    
    @property
    def M603(self):
        """
        Set Intes M603 configuration 1500mm
        """
        self.focal = 1500
        self.diameter = 150

    @property
    def filtername(self):
        """
        Return filter name
        """
        return self.filter_name
    
    @filtername.setter
    def filtername(self,string):
        """
        Set filter name
        """
        self.filter_name = string
    
    def filterwheel(self,filterwheel):
        """
        Set filter of filterweel
         filterwheel (Filterwheel): Filterwheel object (Alpaca or Indilib).
         filter_name (str): Filter name.           
        """       
        filter_number = 0  
        filter_names = filterwheel.names()
        if self.filter_name in filter_names:
            filter_number = filter_names.index(self.filter_name)
            filterwheel.position(filter_number)

    @property
    def coordinates(self):
        """
        Return RA and DEC to hours and degrees
        """
        return self.ra,self.dec
    
    @coordinates.setter
    def coordinates(self,coordinatesdict):
        """
        Set RA and DEC
         coordinatesdict:
         {
            "RA": float - Right ascencion
            "DEC": float - Declination
          }
        """  
        if 'RA' in coordinatesdict:
            ra = float(coordinatesdict['RA'])
            if ra >= 0 and ra < 24:
                self.ra = ra
        if 'DEC' in coordinatesdict:
            dec = float(coordinatesdict['DEC'])
            if dec >= -90 and dec <= 90:
                self.dec = dec    

    @property
    def site(self):
        """
        Return site latitude, site longitude and site elevation 
        """
        return self.latitude,self.longitude,self.elevation
    
    @site.setter
    def site(self,sitedict):
        """
        Set latitude, longitude and elevation
         coordinatesdict:
         {
            "LAT": float - Latitude
            "LONG": float - Longitude
            "ELEV": float - Elevation
          }
        """  
        if 'LAT' in sitedict:
            latitude = float(sitedict['LAT'])
            if latitude >= -90 and latitude <= 90:
                self.latitude = latitude
        if 'LONG' in sitedict:
            longitude = float(sitedict['LONG'])
            if longitude >= 0 and longitude <= 360:
                self.longitude = longitude    
        if 'ELEV' in sitedict:
            elevation = float(sitedict['ELEV'])
            if elevation >= 0 and elevation <= 8000:
                self.elevation = elevation    

    def slewtocoordinates(self,telescope):
        """
        Slew RA and DEC to telescope 
         telescope (Telescope): Telescope object (Alpaca or Indilib).
         ra (float): Hours.
         dec (float): Degrees           
        """
        telescope.slewtocoordinates(self.ra,self.dec)

    @property    
    def positionsbyname(self):
        """
        Return object name, RA and DEC
        """
        return self.object_name,self.ra,self.dec
    
    @positionsbyname.setter
    def positionsbyname(self,string):
        """
        Set RA and DEC with astroquery name object
        """
        ra = 0
        dec = 90
        result_table = Simbad.query_object(string)
        c = SkyCoord(ra=result_table['RA'], dec=result_table['DEC'], unit=(u.deg, u.deg))
        self.ra = c.ra.deg[0]    # Hours
        self.dec = c.dec.deg[0]  # degrees
        self.object_name = result_table['MAIN_ID'][0]

    @property
    def projections(self):
        """
        Displays the archived sectors, RA and DEC on an aitoff projection      
        """
        sct = Sct.Sector()
        sector_arch = sct.readarchives(self.archive_table)
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
         
        milkyway = sct.MilkyWay
        milkyway_ra = []
        milkyway_dec = []
        for line in milkyway:
            ra = float(line['RA'])*u.deg
            dec = float(line['DEC'])*u.deg
            c = SkyCoord(ra, dec, frame='icrs')
            milkyway_ra.append(-c.ra.wrap_at(180 * u.deg).radian)
            milkyway_dec.append(c.dec.radian)
            
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
        plt.plot(milkyway_ra, milkyway_dec, color='blue', lw=2, alpha=0.2)
        if len(sector_arch) > 0:
            plt.plot(value_quadran_ra, value_quadran_dec, 's', color='green', markersize=5, alpha=0.2)   
        plt.plot(value_ra, value_dec, 's', color='red', markersize=5, alpha=0.4)
        # Modification of labels in hours
        ax.set_xticklabels(['10h','08h','06h','04h','02h','0h','22h','20h','18h','16h','14h'],alpha=0.4)
        ax.set_title(title, fontsize = 12)
        # Display
        plt.show()
        
    @property    
    def starmap(self):
        """
        Return data, WCS and title for display
        """
        sct = Sct.Sector()
        WCS = sct.WCS(self.ra,self.dec,self.naxis1,self.naxis2,self.binXY,self.pixelXY,self.focal)
        #field_RA = WCS.wcs.cdelt[0]*self.naxis1
        field = WCS.wcs.cdelt[1]*self.naxis2
        mag = 11
        if field <= 3:
            mag = 14
        if field <= 1:
            mag = 18
        catalog = 'GAIA-EDR3'
        data = sct.regionincatalog(self.ra*15, self.dec,field,field,mag,catalog,'_RAJ2000', '_DEJ2000', 'Gmag')   
        title = 'VizieR-' + catalog + ' | ' + 'F'+str(self.focal) + ' | ' +  self.instrument
        return data,WCS,title
          
    def miriademap(self,target,epoch,epoch_step,epoch_nsteps):
        """
        Return data and title Miriade for display
        """   
        sct = Sct.Sector()
        WCS = sct.WCS(self.ra,self.dec,self.naxis1,self.naxis2,self.binXY,self.pixelXY,self.focal)
        location = str(self.longitude) + ' ' + str(self.latitude) + ' ' + str(self.elevation)
        data = sct.miriadeincatalog(target,epoch,epoch_step,epoch_nsteps,1,location)
        title = target +' | ' + epoch.value        
        return data,WCS,title
       
    
    def exposure(self,exposure,ccd,telescope,filterwheel):
        """
        Get CCD, telescope and filterwheel and write fits file 
         exposure (Exposure): Exposure object.
         ccd (Camera): CCD alpaca or indilib object.
         telescope (Telescope): Telescope alpaca or indilib object.
         filterwheel (Filterwheel): Filterwheel alpaca or indilib object.         
        """
        self._exp_time = exposure.exp_time()
        self._frameid = exposure.exp_label()
        self._datatype = exposure.datatype

        if isinstance(telescope, Telescope):
            self.ra = telescope.rightascension()
            self.dec = telescope.declination()
            self.latitude = telescope.sitelatitude()
            self.longitude = telescope.sitelongitude()
        else:
            self.ra = telescope.rightascension
            self.dec = telescope.declination                
            self.latitude = telescope.sitelatitude
            self.longitude = telescope.sitelongitude

        if isinstance(filterwheel, Filterwheel):
            filter_names = filterwheel.names()
            self.filter_name = filter_names[filterwheel.position()]
        else:
            filter_names = filterwheel.names
            self.filter_name = filter_names[filterwheel.position()]       

        if isinstance(ccd, Camera):
            self.binXY = ccd.binx()
            self.pixelXY = ccd.pixelsizex()
            self._date = ccd.lastexposurestarttime()
            self._temperature = ccd.ccdtemperature()
            _exposurealpaca(exposure,ccd,telescope,filterwheel)
        else:
            _exposureindilib(exposure,ccd,telescope,filterwheel)
        
        self.extendedfits()       

    def _exposureindilib(self,exposure,ccd,telescope,filterwheel):
        """
        Get CCD, telescope and filterwheel and write fits file 
         exposure (Exposure): Exposure object.
         ccd (Camera): CCD indilib object.
         telescope (Telescope): Telescope indilib object.
         filterwheel (Filterwheel): Filterwheel indilib object.           
        """
        hdul = ccd.startexposure(self._exp_time,True)
        while not ccd.imageready():
            time.sleep(1)  
        file_name = self.dataset+'/'+self.observer_name+'_'+self.object_name+'_'+str(self._frameid)+'.fits'
        fits.writeto(file_name, hdul[0].data, hdul[0].header, overwrite=True)         
         
    def _exposurealpaca(self,exposure,ccd,telescope,filterwheel):
        """
        Get CCD, telescope and filterwheel and write fits file 
         exposure (Exposure): Exposure object.
         ccd (Camera): CCD alpaca object.
         telescope (Telescope): Telescope alpaca object.
         filterwheel (Filterwheel): Filterwheel alpaca object.           
        """
        ccd.startexposure(self._exp_time,True)
        while not ccd.imageready():
            time.sleep(1)         
        # Translate picture
        data_ccd = ccd.imagearray()
        data_new = np.rot90(data_ccd)
        data_int16 = data_new.astype(np.int16)       
        #Vertical inversion if necessary
        #data_real = np.fliplr(data_int16)
        #Create simple fits
        hdu = fits.PrimaryHDU(data=data_int16)
        file_name = self.dataset+'/'+self.observer_name+'_'+self.object_name+'_'+str(self._frameid)+'.fits'
        fits.writeto(file_name, hdu.data, hdu.header, overwrite=True) 
    
    def extendedfits(self):
        """
        Write fits header extended and fits file
        """
        fits_file = self.dataset+'/'+self.observer_name+'_'+self.object_name+'_'+str(self._frameid)+'.fits'
        
        fits.setval(fits_file, 'PIXSIZE1', value=self.pixelXY, comment='[um] Pixel Size X, binned', savecomment=True)
        fits.setval(fits_file, 'PIXSIZE2', value=self.pixelXY, comment='[um] Pixel Size Y, binned', savecomment=True)
        fits.setval(fits_file, 'XBINNING', value=self.binXY, comment='Binning factor X', savecomment=True)
        fits.setval(fits_file, 'YBINNING', value=self.binXY, comment='Binning factor Y', savecomment=True)
        fits.setval(fits_file, 'EXPTIME', value=self._exp_time, comment='[s] Total Exposure Time', savecomment=True)
        fits.setval(fits_file, 'OBJECT', value=self.object_name, comment='Observed object name', savecomment=True)
        fits.setval(fits_file, 'OBSERVER', value=self.observer_name, comment='Observed name', savecomment=True)
        fits.setval(fits_file, 'TELESCOP', value=self.telescope_name, comment='Telescope name', savecomment=True)
        fits.setval(fits_file, 'INSTRUME', value=self.instrument, comment='Instrument used for acquisition', savecomment=True)                         
        fits.setval(fits_file, 'ROWORDER', value='TOP-DOWN', comment='Order of the rows in image array', savecomment=True)                 
        fits.setval(fits_file, 'CCD-TEMP', value=self._temperature, comment='CCD temperature (Celsius)', savecomment=True) 
        fits.setval(fits_file, 'FILTER', value=self.filter_name, comment='Filter info', savecomment=True)     
        fits.setval(fits_file, 'SITELAT', value=self.latitude, comment='Observatory latitude', savecomment=True) 
        fits.setval(fits_file, 'SITELONG', value=self.longitude, comment='Observatory longitude', savecomment=True)
        fits.setval(fits_file, 'SITEELEV', value=self.elevation, comment='Driver create', savecomment=True) 
        fits.setval(fits_file, 'SWCREATE', value=self.driver_name, comment='Driver create', savecomment=True) 
        fits.setval(fits_file, 'FOCALLEN', value=self.focal, comment='[mm] Telescope focal length', savecomment=True) 
        fits.setval(fits_file, 'FRAMEX', value=0, comment='Frame start x', savecomment=True)
        fits.setval(fits_file, 'FRAMEY', value=0, comment='Frame start y', savecomment=True)                                                                   
        fits.setval(fits_file, 'DATE-OBS', value=self._date, comment='UTC start date of observation', savecomment=True)
        fits.setval(fits_file, 'RADESYSA', value='ICRS', comment='Equatorial coordinate system', savecomment=True)
        fits.setval(fits_file, 'FRAMEID', value=self._frameid, comment='Frame ID', savecomment=True)
        fits.setval(fits_file, 'EQUINOX', value=2000.0, comment='Equinox date', savecomment=True)
        fits.setval(fits_file, 'DATATYPE', value=self._datatype, comment='Type of data', savecomment=True)
        fits.setval(fits_file, 'MJD-OBS', value=0.0, comment='MJD of start of obseration', savecomment=True)
        fits.setval(fits_file, 'JD-OBS', value=0.0, comment='JD of start of obseration', savecomment=True)

        hdu = fits.open(fits_file)[0]
        header = hdu.header

        # Modification telescope name header
        header['TELESCOP'] = self.telescope_name

        # Modification JD and MJD header
        date_obs = header['DATE-OBS']
        time_obs = Time(header['DATE-OBS'])
        header['JD-OBS'] = time_obs.jd
        header['MJD-OBS'] = time_obs.mjd

        # Elements for CRVAL
        RA_deg = 15 * self.ra
        DEC_deg = self.dec

        # Elements for CRPIX
        crpix1 = int(header['NAXIS1'])/2
        crpix2 = int(header['NAXIS2'])/2

        # Element for CDELT
        cdelt1 = (206*int(header['PIXSIZE1'])*int(header['XBINNING'])/self.focal)/3600
        cdelt2 = (206*int(header['PIXSIZE2'])*int(header['YBINNING'])/self.focal)/3600

        # Header WCS
        w = wcs.WCS(naxis=2)
        w.wcs.ctype = ["RA---TAN", "DEC--TAN"]
        # CRVAL position
        w.wcs.crval = [RA_deg, DEC_deg] 
        # CRPIX Vecteur à 2 éléments donnant les coordonnées X et Y du pixel de référence 
        # (def = NAXIS / 2) dans la convention FITS (le premier pixel est 1,1)
        w.wcs.crpix = [crpix1, crpix2]
        # CDELT Vecteur à 2 éléments donnant l'incrément physique au pixel de référence
        w.wcs.cdelt = [-cdelt1, cdelt2] 

        # Now, write out the WCS object as a FITS header
        hdu.header = header + w.to_header()
        # Header and data
        hdr = hdu.header
        data = hdu.data
        # Sauvegarde
        fits.writeto(file_name, data, hdr, overwrite=True)
 