"""
Ciboulette class
"""

import time
import numpy as np
import math 
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.time import Time
from astropy.table import Table
from astropy.coordinates import SkyCoord, Angle
from astropy import units as u
from astropy.coordinates import Angle
from astropy import wcs
from astropy.io.votable import parse_single_table
from astropy.utils.data import get_pkg_data_filename
from astroquery.simbad import Simbad
from alpaca import Telescope, Camera, FilterWheel
from ciboulette.base import constant
from ciboulette.sector import projection
from ciboulette.sector import maps
from ciboulette.utils import exposure as Exp
from ciboulette.utils import planning as Pln
from ciboulette.aavso.webobs import WebObs, datadownload, vsx

class Ciboulette(object):
        
    def __init__(self):
        self.data = []
        self.api_version = constant.API_version
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
        self._date = Time( Time.now(), format='fits', scale='utc', out_subfmt='date_hms').value
        self._exp_time = 0
        self._frameid = 1
        self._datatype = 'Light'
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
        
        return Table([api,focal,diameter,latitude,longitude,elevation,instrument,naxis1,naxis2,
                      binXY,pixelXY,filter_name,telescope_name,observer_name,dataset,archive_table,ra,dec,object_name], 
                      names=['API','FOCAL','DIAM','SITE_LAT','SITE_LONG','SITE_ELEV','INSTRUME','NAXIS1','NAXIS2',
                         'BINXY','PIXELXY','FILTER','NAME','OBSERVER','DATASET','ARCHIVES','RA','DEC','OBJECT'])  

    def datastream(self):
        """
        Return JSON of ciboulette values
        """
        name = '"' + self.observer_name + '":'
        api = '{ "api":' + '"' + str(self.api_version) + '", '                              # Astropy API
        focal = '"focal":' + '"' + str(self.focal) + '", '                                  # Focal millimeter
        diameter = '"diameter":' + '"' + str(self.diameter) + '", '                         # Diameter millimeter
        latitude = '"latitude":' + '"' + str(self.latitude) + '", '                         # Site latitude degrees
        longitude = '"longitude":' + '"' + str(self.longitude) + '", '                      # Site longitude degrees
        elevation = '"elevation":' + '"' + str(self.elevation) + '", '                      # Site elevation meter
        instrument = '"instrument":' + '"' + self.instrument + '", '                        # Instrument name
        naxis1 = '"naxis1":' + '"' + str(self.naxis1) + '", '                               # Size naxis1
        naxis2 = '"naxis2":' + '"' + str(self.naxis2) + '", '                               # Size naxis2
        binXY = '"binXY":' + '"' + str(self.binXY) + '", '                                  # Binning
        pixelXY = '"pixelXY":' + '"' + str(self.pixelXY) + '", '                            # Pixel size X and Y
        filter_name = '"filter":' + '"' + self.filter_name + '", '                          # Filter name
        telescope_name = '"telescope":' + '"' + self.telescope_name + '", '                 # Telescope name
        observer_name = '"observer":' + '"' + self.observer_name + '", '                    # Observer name
        dataset = '"dataset":' + '"' + self.dataset + '", '                                 # Dataset repository
        archive_table = '"archive":' + '"' + self.archive_table + '", '                     # Archives repository
        ra = '"RA":' + '"' + str(self.ra) + '", '                                           # Hours
        dec = '"DEC":' + '"' + str(self.dec) + '", '                                        # Degrees
        object_name = '"object":' + '"' + self.object_name + '" }'                          # Object name     
        
        data= "{ "+name+api+focal+diameter+latitude+longitude+elevation+instrument+naxis1+naxis2+binXY+pixelXY+filter_name+telescope_name+observer_name+dataset+archive_table+ra+dec+object_name+" }"
        return data

    
    @property
    def header(self):
        return self.table
               
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
    def asi178(self):
        """
        Set ASI 178 configuration
        """
        self.instrument = 'ASI 178'
        self.naxis1 = 3096
        self.naxis2 = 2080
        self.pixelXY = 2.4       

    @property
    def asi294(self):
        """
        Set ASI 294 configuration
        """
        self.instrument = 'ASI 294'
        self.naxis1 = 4144
        self.naxis2 = 2822
        self.pixelXY = 4.63      
    
    @property
    def qhy5M(self):
        """
        Set QHY5M configuration
        """
        self.instrument = 'QHY-5M'
        self.naxis1 = 1280
        self.naxis2 = 1024
        self.pixelXY = 5.20    

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
    def tokinaSZX400(self):
        """
        Set Tokina 400mm F8 configuration
        """
        self.focal = 400
        self.diameter = 50

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
        Set 70-300 configuration configuration
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
    def binning(self):
        """
        Return binnning value
        """
        return self.binXY
    
    @binning.setter
    def binning(self,binXY):
        """
        Set binning 
        """
        if binXY < 1:
            binXY = 1
        self.binXY = binXY        
        
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
        if isinstance(filterwheel, FilterWheel):
            filter_names = filterwheel.names()
        else:
            filter_names = filterwheel.names
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
            if longitude >= -360 and longitude <= 360:
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
        if isinstance(telescope, Telescope):
            while telescope.slewing():
                time.sleep(1)

    
    def synctocoordinates(self,telescope):
        """
        Synchronize the telescope with RA and DEC
         telescope (Telescope): Telescope object (Alpaca or Indilib).
         ra (float): Hours.
         dec (float): Degrees           
        """
        if isinstance(telescope, Telescope):
            telescope.unpark()
            telescope.tracking()
        else :
            telescope.unpark
            telescope.tracking
        telescope.synctocoordinates(self.ra,self.dec)

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
    def positionsbyaavso(self):
        """
        Return object name, RA and DEC
        """
        return self.positionsbyname

    @positionsbyaavso.setter
    def positionsbyaavso(self,string):
        """
        Set RA and DEC with VSX AAVSO name object
        """
        ra = 0
        dec = 90
        v = vsx(string)
        ra,dec = v.hourdegree
        self.ra = ra    # Hours
        self.dec = dec  # degrees
        self.object_name = v.name

    @property
    def projectionslight(self):
        """
        Displays the archived sectors, RA and DEC on an aitoff projection      
        """
        p = projection.Projection()
        p.projections(self.ra,self.dec,self.archive_table)
        p.display

    @property
    def projections(self):
        """
        Displays the archived sectors, RA and DEC and Moon on an aitoff projection      
        """
        p = projection.Projection()
        p.Moon(self._date,self.latitude,self.longitude,self.elevation)
        p.projections(self.ra,self.dec,self.archive_table)
        return p

    def projections_planning(self,planning):
        """
        Add planning positions
        """
        p = projection.Projection()
        p.Moon(self._date,self.latitude,self.longitude,self.elevation)
        p.projections(self.ra,self.dec,self.archive_table)
        p.planning(planning)
        p.display

    def projections_mast(self,mast):
        """
        Add planning positions
        """
        p = projection.Projection()
        p.Moon(self._date,self.latitude,self.longitude,self.elevation)
        p.projections(self.ra,self.dec,self.archive_table)
        p.mast(mast)
        p.display

    @property
    def opencluster(self):
        """
        Displays open cluster on an aitoff projection (mag < 18)     
        """
        p = projection.Projection()
        p.Moon(self._date,self.latitude,self.longitude,self.elevation)
        p.projections(self.ra,self.dec,self.archive_table)
        p.opencluster
        p.display

    @property
    def HerbigAeBe(self):
        """
        Displays Herbig Ae/Be on an aitoff projection
        """
        p = projection.Projection()
        p.Moon(self._date,self.latitude,self.longitude,self.elevation)
        p.projections(self.ra,self.dec,self.archive_table)
        p.HerbigAeBe
        p.display

    @property
    def cepheid(self):
        """
        Displays cepheid on an aitoff projection (mag < 18)     
        """
        p = projection.Projection()
        p.Moon(self._date,self.latitude,self.longitude,self.elevation)
        p.projections(self.ra,self.dec,self.archive_table)
        p.cepheid
        p.display

    @property    
    def starsmap(self):
        """
        Display stars map at RA and DEC
        """   
        m = maps.Map()
        m.stars(self.ra,self.dec,self.naxis1,self.naxis2,self.binXY,self.pixelXY,self.focal,self.instrument,self.telescope_name,self.observer_name,self.filter_name)
        return m
          
    def trajectory(self,target,epoch,epoch_step,epoch_nsteps):
        """
        Display map with target
        """   
        m = maps.Map()
        m.trajectory(target,epoch,epoch_step,epoch_nsteps,self.latitude,self.longitude,self.elevation)
        ra = m.target['RA'][0]/15
        dec = m.target['DEC'][0]
        self.coordinates = { "RA": ra, "DEC": dec }
        m.stars(self.ra,self.dec,self.naxis1,self.naxis2,self.binXY,self.pixelXY,self.focal,self.instrument,self.telescope_name,self.observer_name,self.filter_name)
        m.display           
    
    def camera(self,camera):
        """
        Get CCD and write fits file 
         camera (object): Camera alpaca or indilib object.
        """
        if isinstance(camera, Camera):
            t = Time( Time.now(), format='fits', scale='utc', out_subfmt='date_hms')
            self._date = t.value
            camera.binx(self.binXY)
            camera.biny(self.binXY)
            camera.startexposure(self._exp_time,True)
            i = self._exp_time + (((self.naxis1 * self.naxis2)/1048576) *2)
            while i > 0:
                time.sleep(1)
                i = i - 1
                 
            self.binXY = camera.binx()
            self.pixelXY = camera.pixelsizex()
            
            """
            Not implemented in all drivers : lastexposurestarttime()
            """
            #self._date = camera.lastexposurestarttime()
            
            if camera.cansetccdtemperature():
                self._temperature = camera.ccdtemperature()
            # Translate picture
            data_ccd = camera.imagearray()
            data_new = np.rot90(data_ccd)
            data_int16 = data_new.astype(np.int16)       
            #Vertical inversion if necessary
            #data_real = np.fliplr(data_int16)
            #Create simple fits
            hdu = fits.PrimaryHDU(data=data_int16)
            file_name = self.dataset+'/_'+self.observer_name+'_'+self.object_name+'_'+str(self._frameid)+'.fits'
            fits.writeto(file_name, hdu.data, hdu.header, overwrite=True)  
        else:
            camera.binning({'X':self.binXY, 'Y':self.binXY})
            hdul = camera.expose(self._exp_time)
            i = self._exp_time + (((self.naxis1 * self.naxis2)/1048576) *2)
            while i > 0:
                time.sleep(1)
                i = i - 1
            file_name = self.dataset+'/_'+self.observer_name+'_'+self.object_name+'_'+str(self._frameid)+'.fits'
            fits.writeto(file_name, hdul[0].data, hdul[0].header, overwrite=True)  
        self.extendedfits()           

    def frameid(self):
        """
        Return frame ID value
        """
        return self._frameid

    def datatype(self):
        """
        Return datatype value
        """
        return self._datatype
    
    def expose(self):
        """
        Return exposure value
        """
        return self._exp_time
    
    @property
    def exposure(self):
        """
        Return exposure value
        """
        return self._exp_time,self._frameid,self._datatype
    
    @exposure.setter
    def exposure(self,exposure):
        """
        Set exposure values
         exposure (object): Exposure object.
        """
        self._exp_time = exposure.exp_time
        self._frameid = exposure.exp_label
        self._datatype = exposure.datatype
    
    def extendedfits(self):
        """
        Write fits header extended and fits file
        """
        fits_file = self.dataset+'/_'+self.observer_name+'_'+self.object_name+'_'+str(self._frameid)+'.fits'
        
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
        fits.setval(fits_file, 'CCD-TEMP', value=self._temperature, comment='[C] CCD temperature (Celsius)', savecomment=True) 
        fits.setval(fits_file, 'FILTER', value=self.filter_name, comment='Filter info', savecomment=True)     
        fits.setval(fits_file, 'SITELAT', value=self.latitude, comment='[deg] Observatory latitude', savecomment=True) 
        fits.setval(fits_file, 'SITELONG', value=self.longitude, comment='[deg] Observatory longitude', savecomment=True)
        fits.setval(fits_file, 'SITEELEV', value=self.elevation, comment='[deg] Observatory elevation', savecomment=True) 
        fits.setval(fits_file, 'SWCREATE', value=self.api_version, comment='Driver create', savecomment=True) 
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
        fits_file_name = self.dataset+'/'+self.observer_name+'_'+self.object_name+'_'+str(self._frameid)+'.fits'
        fits.writeto(fits_file_name, data, hdr, overwrite=True)

    def extendedhdr(self,header):
        """
        Set header extended 
        """     
        hdr = header
        hdr.set('PIXSIZE1', self.pixelXY, '[um] Pixel Size X, binned') 
        hdr.set('PIXSIZE2', self.pixelXY, '[um] Pixel Size Y, binned')
        hdr.set('XBINNING', self.binXY, 'Binning factor X')
        hdr.set('YBINNING', self.binXY, 'Binning factor Y')
        hdr.set('EXPTIME', self._exp_time, '[s] Total Exposure Time')
        hdr.set('OBJECT', self.object_name, 'Observed object name')
        hdr.set('OBSERVER', self.observer_name, 'Observed name')
        hdr.set('TELESCOP', self.telescope_name, 'Telescope name')
        hdr.set('INSTRUME', self.instrument, 'Instrument used for acquisition')                         
        hdr.set('ROWORDER', 'TOP-DOWN', 'Order of the rows in image array')                 
        hdr.set('CCD-TEMP', self._temperature, '[C] CCD temperature (Celsius)') 
        hdr.set('FILTER', self.filter_name, 'Filter info')     
        hdr.set('SITELAT', self.latitude, '[deg] Observatory latitude') 
        hdr.set('SITELONG', self.longitude, '[deg] Observatory longitude')
        hdr.set('SITEELEV', self.elevation, '[deg] Observatory elevation') 
        hdr.set('SWCREATE', self.api_version, 'Driver create') 
        hdr.set('FOCALLEN', self.focal,'[mm] Telescope focal length') 
        hdr.set('FRAMEX', 0, 'Frame start x')
        hdr.set('FRAMEY', 0, 'Frame start y')                                                                   
        hdr.set('DATE-OBS', self._date, 'UTC start date of observation')
        hdr.set('RADESYSA', 'ICRS', 'Equatorial coordinate system')
        hdr.set('FRAMEID', self._frameid, 'Frame ID')
        hdr.set('EQUINOX', 2000.0, 'Equinox date')
        hdr.set('DATATYPE', self._datatype, 'Type of data')
        hdr.set('MJD-OBS', 0.0, 'MJD of start of obseration')
        hdr.set('JD-OBS', 0.0, 'JD of start of obseration')
        hdr.set('TELESCOP', self.telescope_name, 'Telescope name')

        # Modification JD and MJD header
        date_obs = hdr['DATE-OBS']
        time_obs = Time(hdr['DATE-OBS'])
        hdr['JD-OBS'] = time_obs.jd
        hdr['MJD-OBS'] = time_obs.mjd

        # Elements for CRVAL
        RA_deg = 15 * self.ra
        DEC_deg = self.dec

        # Elements for CRPIX
        crpix1 = int(hdr['NAXIS1'])/2
        crpix2 = int(hdr['NAXIS2'])/2

        # Element for CDELT
        cdelt1 = (206*int(hdr['PIXSIZE1'])*int(hdr['XBINNING'])/self.focal)/3600
        cdelt2 = (206*int(hdr['PIXSIZE2'])*int(hdr['YBINNING'])/self.focal)/3600

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
        hdu = hdr + w.to_header()
        return hdu

    def reversex(self, data):
        """
        Reverse data of fits image
        """
        return  np.flipud(data)
            
    def reversey(self, data):
        """
        Reverse data of fits image
        """
        return np.fliplr(data)
    
    @property
    def functions(self):
        """
        Return other functions, resolve, fields, magnitude
        """
        resolve = Angle( (((206 * self.pixelXY) / self.focal)) / 3600, unit=u.degree)
        fieldRA = Angle( resolve * self.naxis1, unit=u.degree)
        fieldDEC = Angle(resolve * self.naxis2, unit=u.degree)
        magnitude = math.log10(self.diameter) * 5 + 7.2      
        t = Table()
        t['Resolve'] = [resolve]
        t['Field RA'] = [fieldRA]
        t['Field DEC'] = [fieldDEC]
        t['Mv'] = [magnitude]           
        t['Resolve'].info.format = '.8f'
        t['Field RA'].info.format = '.8f'
        t['Field DEC'].info.format = '.8f'
        t['Mv'].info.format = '.2f'
        return t

    @property
    def resolve(self):
        return Angle((((206 * self.pixelXY) / self.focal)) / 3600, unit=u.degree)
    
    @property
    def fieldRA(self):
        return Angle(self.resolve * self.naxis1, unit=u.degree)
    
    @property
    def fieldDEC(self):
        return Angle(self.resolve * self.naxis2, unit=u.degree)

    @property
    def magnitude(self):
        return math.log10(self.diameter) * 5 + 7.2