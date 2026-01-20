# Licensed under GPL3 (see LICENSE)
# coding=utf-8

"""
Classes and utility functions for communicating with cameras via the INDI protocol, http://www.indilib.org.

# pylibcamera Main
pylibcamera Main.CAMERA_SELECTION.CAM0=On
pylibcamera Main.CONNECTION.CONNECT=On
pylibcamera Main.CONNECTION.DISCONNECT=Off
pylibcamera Main.DRIVER_INFO.DRIVER_NAME=pylibcamera Main
pylibcamera Main.DRIVER_INFO.DRIVER_EXEC=/home/ut1/astropy/bin/indi_pylibcamera
pylibcamera Main.DRIVER_INFO.DRIVER_VERSION=3.1.0
pylibcamera Main.DRIVER_INFO.DRIVER_INTERFACE=2
pylibcamera Main.LOGGING_LEVEL.LOGGING_DEBUG=Off
pylibcamera Main.LOGGING_LEVEL.LOGGING_INFO=On
pylibcamera Main.LOGGING_LEVEL.LOGGING_WARN=Off
pylibcamera Main.LOGGING_LEVEL.LOGGING_ERROR=Off
pylibcamera Main.POLLING_PERIOD.PERIOD_MS=1000.0
pylibcamera Main.GEOGRAPHIC_COORD.LAT=0
pylibcamera Main.GEOGRAPHIC_COORD.LONG=0
pylibcamera Main.GEOGRAPHIC_COORD.ELEV=0
pylibcamera Main.EQUATORIAL_EOD_COORD.RA=0
pylibcamera Main.EQUATORIAL_EOD_COORD.DEC=0
pylibcamera Main.TELESCOPE_PIER_SIDE.PIER_WEST=On
pylibcamera Main.TELESCOPE_PIER_SIDE.PIER_EAST=Off
pylibcamera Main.SCOPE_INFO.FOCAL_LENGTH=0.0
pylibcamera Main.SCOPE_INFO.APERTURE=0.0
pylibcamera Main.DO_SNOOPING.SNOOP=On
pylibcamera Main.DO_SNOOPING.NO_SNOOP=Off
pylibcamera Main.ACTIVE_DEVICES.ACTIVE_TELESCOPE=
pylibcamera Main.CAMERA_INFO.CAMERA_MODEL=imx477
pylibcamera Main.CAMERA_INFO.CAMERA_PIXELARRAYSIZE=(4056, 3040)
pylibcamera Main.CAMERA_INFO.CAMERA_PIXELARRAYACTIVEAREA=[(8, 16, 4056, 3040)]
pylibcamera Main.CAMERA_INFO.CAMERA_UNITCELLSIZE=(1550, 1550)
pylibcamera Main.CCD_CAPTURE_FORMAT.INDI_RAW=Off
pylibcamera Main.CCD_CAPTURE_FORMAT.RAW_MONO=On
pylibcamera Main.CCD_CAPTURE_FORMAT.INDI_RGB=Off
pylibcamera Main.CCD_CAPTURE_FORMAT.INDI_MONO=Off
pylibcamera Main.RAW_FORMAT.RAWFORMAT0=On
pylibcamera Main.RAW_FORMAT.RAWFORMAT1=Off
pylibcamera Main.RAW_FORMAT.RAWFORMAT2=Off
pylibcamera Main.RAW_FORMAT.RAWFORMAT3=Off
pylibcamera Main.RAW_FORMAT.RAWFORMAT4=Off
pylibcamera Main.RAW_FORMAT.RAWFORMAT5=Off
pylibcamera Main.RAW_FORMAT.RAWFORMAT6=Off
pylibcamera Main.RAW_FORMAT.RAWFORMAT7=Off
pylibcamera Main.RAW_FORMAT.RAWFORMAT8=Off
pylibcamera Main.RAW_FORMAT.RAWFORMAT9=Off
pylibcamera Main.RAW_FORMAT.RAWFORMAT10=Off
pylibcamera Main.RAW_FORMAT.RAWFORMAT11=Off
pylibcamera Main.RAW_FORMAT.RAWFORMAT12=Off
pylibcamera Main.RAW_FORMAT.RAWFORMAT13=Off
pylibcamera Main.RAW_FORMAT.RAWFORMAT14=Off
pylibcamera Main.CCD_PROCFRAME.WIDTH=4056.0
pylibcamera Main.CCD_PROCFRAME.HEIGHT=3040.0
pylibcamera Main.CAMCTRL_AEENABLE.INDI_ENABLED=Off
pylibcamera Main.CAMCTRL_AEENABLE.INDI_DISABLED=On
pylibcamera Main.CAMCTRL_AECONSTRAINTMODE.NORMAL=On
pylibcamera Main.CAMCTRL_AECONSTRAINTMODE.HIGHLIGHT=Off
pylibcamera Main.CAMCTRL_AECONSTRAINTMODE.SHADOWS=Off
pylibcamera Main.CAMCTRL_AECONSTRAINTMODE.CUSTOM=Off
pylibcamera Main.CAMCTRL_AEEXPOSUREMODE.NORMAL=On
pylibcamera Main.CAMCTRL_AEEXPOSUREMODE.SHORT=Off
pylibcamera Main.CAMCTRL_AEEXPOSUREMODE.LONG=Off
pylibcamera Main.CAMCTRL_AEEXPOSUREMODE.CUSTOM=Off
pylibcamera Main.CAMCTRL_AEMETERINGMODE.CENTREWEIGHTED=On
pylibcamera Main.CAMCTRL_AEMETERINGMODE.SPOT=Off
pylibcamera Main.CAMCTRL_AEMETERINGMODE.MATRIX=Off
pylibcamera Main.CAMCTRL_AEMETERINGMODE.CUSTOM=Off
pylibcamera Main.CAMCTRL_AWBENABLE.INDI_ENABLED=Off
pylibcamera Main.CAMCTRL_AWBENABLE.INDI_DISABLED=On
pylibcamera Main.CAMCTRL_AWBMODE.AUTO=On
pylibcamera Main.CAMCTRL_AWBMODE.TUNGSTEN=Off
pylibcamera Main.CAMCTRL_AWBMODE.FLUORESCENT=Off
pylibcamera Main.CAMCTRL_AWBMODE.INDOOR=Off
pylibcamera Main.CAMCTRL_AWBMODE.DAYLIGHT=Off
pylibcamera Main.CAMCTRL_AWBMODE.CLOUDY=Off
pylibcamera Main.CAMCTRL_AWBMODE.CUSTOM=Off
pylibcamera Main.CAMCTRL_BRIGHTNESS.BRIGHTNESS=0.0
pylibcamera Main.CAMCTRL_COLOURGAINS.REDGAIN=2.0
pylibcamera Main.CAMCTRL_COLOURGAINS.BLUEGAIN=2.0
pylibcamera Main.CAMCTRL_CONTRAST.CONTRAST=1.0
pylibcamera Main.CAMCTRL_EXPOSUREVALUE.EXPOSUREVALUE=0.0
pylibcamera Main.CAMCTRL_NOISEREDUCTIONMODE.OFF=On
pylibcamera Main.CAMCTRL_NOISEREDUCTIONMODE.FAST=Off
pylibcamera Main.CAMCTRL_NOISEREDUCTIONMODE.HIGHQUALITY=Off
pylibcamera Main.CAMCTRL_SATURATION.SATURATION=1.0
pylibcamera Main.CAMCTRL_SHARPNESS.SHARPNESS=0.0
pylibcamera Main.CCD_EXPOSURE.CCD_EXPOSURE_VALUE=1.0
pylibcamera Main.CCD_ABORT_EXPOSURE.ABORT=Off
pylibcamera Main.CCD_FRAME.X=0.0
pylibcamera Main.CCD_FRAME.Y=0.0
pylibcamera Main.CCD_FRAME.WIDTH=4056.0
pylibcamera Main.CCD_FRAME.HEIGHT=3040.0
pylibcamera Main.CCD_BINNING.HOR_BIN=1
pylibcamera Main.CCD_BINNING.VER_BIN=1
pylibcamera Main.CCD_TEMPERATURE.CCD_TEMPERATURE_VALUE=0
pylibcamera Main.CCD_INFO.CCD_MAX_X=4056
pylibcamera Main.CCD_INFO.CCD_MAX_Y=3040
pylibcamera Main.CCD_INFO.CCD_PIXEL_SIZE=1.55
pylibcamera Main.CCD_INFO.CCD_PIXEL_SIZE_X=1.55
pylibcamera Main.CCD_INFO.CCD_PIXEL_SIZE_Y=1.55
pylibcamera Main.CCD_INFO.CCD_BITSPERPIXEL=12
pylibcamera Main.CCD_COMPRESSION.CCD_COMPRESS=Off
pylibcamera Main.CCD_COMPRESSION.CCD_RAW=On
pylibcamera Main.CCD_FRAME_TYPE.FRAME_LIGHT=On
pylibcamera Main.CCD_FRAME_TYPE.FRAME_BIAS=Off
pylibcamera Main.CCD_FRAME_TYPE.FRAME_DARK=Off
pylibcamera Main.CCD_FRAME_TYPE.FRAME_FLAT=Off
pylibcamera Main.UPLOAD_MODE.UPLOAD_CLIENT=On
pylibcamera Main.UPLOAD_MODE.UPLOAD_LOCAL=Off
pylibcamera Main.UPLOAD_MODE.UPLOAD_BOTH=Off
pylibcamera Main.UPLOAD_SETTINGS.UPLOAD_DIR=/home/ut1
pylibcamera Main.UPLOAD_SETTINGS.UPLOAD_PREFIX=IMAGE_XXX
pylibcamera Main.CCD_FAST_TOGGLE.INDI_ENABLED=Off
pylibcamera Main.CCD_FAST_TOGGLE.INDI_DISABLED=On
pylibcamera Main.CCD_FAST_COUNT.FRAMES=1
pylibcamera Main.CCD_GAIN.GAIN=10.0
pylibcamera Main.APPLY_CONFIG.CONFIG1=On
pylibcamera Main.APPLY_CONFIG.CONFIG2=Off
pylibcamera Main.APPLY_CONFIG.CONFIG3=Off
pylibcamera Main.APPLY_CONFIG.CONFIG4=Off
pylibcamera Main.APPLY_CONFIG.CONFIG5=Off
pylibcamera Main.APPLY_CONFIG.CONFIG6=Off
pylibcamera Main.CONFIG_NAME.CONFIG_NAME=
pylibcamera Main.CONFIG_PROCESS.CONFIG_LOAD=Off
pylibcamera Main.CONFIG_PROCESS.CONFIG_SAVE=Off
pylibcamera Main.CONFIG_PROCESS.CONFIG_DEFAULT=Off
pylibcamera Main.CONFIG_PROCESS.CONFIG_PURGE=Off
"""

__authors__ = ("Dominique Touzan","ciboulette module")
__contact__ = ("dtouzan@gmail.com","https://github.com/dtouzan/ciboulette")
__copyright__ = "MIT"
__date__ = "2024-11-02"
__version__= "1.0.0"
__citation__ = "MMT Observatory package. https://github.com/MMTObservatory/indiclient"

import time
import io

import logging
import logging.handlers

from astropy.io import fits

from .indiclient import indiclient
from ciboulette.indiclient.indicam import CCDCam
from ciboulette.indiclient.vectorlist import pylibcamera_vector

log = logging.getLogger("")
log.setLevel(logging.INFO)

class imx477Cam(CCDCam):
    """
    Wrap CCDCam,set the driver to the imx477 driver 
    """
    def __init__(self, host="localhost", port=7624):
        super(imx477Cam, self).__init__(host, port, driver="pylibcamera Main")
        self.camera_name = "imx477"

    @property
    def getprop(self):
        """
        Get properties info.
        """
        for vector in pylibcamera_vector:
            info = self.VECTOR_INFO(vector)
            for item in info.items():
                print(f'{self.driver}.{vector}.{item[0]}={item[1]}')
    
    def VECTOR_INFO(self, vector="DRIVER_INFO"):
        """
        Get the vector info.
        """
        self.process_events()
        info_vec = self.get_vector(self.driver, vector)
        info = {}
        if (info_vec):
            for e in info_vec.elements:
                if(type(e).__name__ == 'indinumber'):
                    info[e.getName()] = e.get_float()
                else:
                    info[e.getName()] = e.get_text()
        return info
        
    @property
    def DRIVER_INFO(self):
        """
        Get the Driver info.
        """
        return self.VECTOR_INFO('DRIVER_INFO')

    @property
    def CAMERA_INFO(self):
        """
        Get the Camera info.
        """
        return self.VECTOR_INFO('CAMERA_INFO')

    @property
    def CCD_CAPTURE_FORMAT(self):
        """
        Get the Capture format info.
        """
        return self.VECTOR_INFO("CCD_CAPTURE_FORMAT")
    
    @property
    def CCD_FRAME_TYPE(self):
        """
        Get the Frame Type format info.
        """
        return self.VECTOR_INFO('CCD_FRAME_TYPE')

    @property
    def CCD_INFO(self):
        """
        Get the CCD format info.
        """
        return self.VECTOR_INFO('CCD_INFO')

        
    @property
    def CONFIG_LOAD(self):
        """
        Get the load configuration.
        """
        self.set_and_send_text(self.driver, 'CONFIG_PROCESS', 'CONFIG_LOAD', 'On')

    @property
    def CONFIG_SAVE(self):
        """
        Get the load configuration.
        """
        self.set_and_send_text(self.driver, 'CONFIG_PROCESS', 'CONFIG_SAVE', 'On')
       
    @property
    def GAIN(self):
        self.process_events()
        gain = self.get_float(self.driver, "CCD_GAIN", "GAIN")
        return gain

    @GAIN.setter
    def GAIN(self,f):
        if f >=0 and f <=22:
            self.set_and_send_float(self.driver, 'CCD_GAIN', 'GAIN', f) 
            self.process_events()

    @property
    def REDGAIN(self):
        self.process_events()
        gain = self.get_float(self.driver, "CAMCTRL_COLOURGAINS", "REDGAIN")
        return gain

    @REDGAIN.setter
    def REDGAIN(self,f):
        if f >=0 and f <=22:
            self.set_and_send_float(self.driver, 'CAMCTRL_COLOURGAINS', 'REDGAIN', f) 
            self.process_events()

    @property
    def BLUEGAIN(self):
        self.process_events()
        gain = self.get_float(self.driver, "CAMCTRL_COLOURGAINS", "BLUEGAIN")
        return gain

    @REDGAIN.setter
    def BLUEGAIN(self,f):
        if f >=0 and f <=22:
            self.set_and_send_float(self.driver, 'CAMCTRL_COLOURGAINS', 'BLUEGAIN', f) 
            self.process_events()

    @property
    def HDUComment(self):
        """
        Return: tag HDUL comment
        """
        return 'Raspicam imx477 V1 for astronomy'

    @property
    def COMPRESS(self):
        """
        Turn CCD_COMPRESSION.CCD_COMPRESS=On 
        """
        self.set_and_send_text(self.driver, "CCD_COMPRESSION", "CCD_COMPRESS", "On")
        self.process_events()

    @property
    def UNCOMPRESS(self):
        """
        Turn CCD_COMPRESSION.CCD_RAW=On 
        """
        self.set_and_send_text(self.driver, "CCD_COMPRESSION", "CCD_COMPRESS", "Off")
        self.set_and_send_text(self.driver, "CCD_COMPRESSION", "CCD_RAW", "On")

    @property
    def INDI_RGB(self):
        """
        Turn CCD_CAPTURE_FORMAT.INDI_RGB=On
        """
        self.set_and_send_switchvector_by_elementlabel(self.driver, "CCD_CAPTURE_FORMAT", "RGB")

    @property
    def RAW(self):
        """
        Turn CCD_CAPTURE_FORMAT.INDI_RAW=On
        """
        self.set_and_send_switchvector_by_elementlabel(self.driver, "CCD_CAPTURE_FORMAT", "RAW")

    @property
    def RAW_MONO(self):
        """
        Turn CCD_CAPTURE_FORMAT.RAW_MONO=On
        """
        self.RAW
        self.set_and_send_text(self.driver, "CCD_CAPTURE_FORMAT", "RAW_MONO", "On")
    
    @property
    def default(self):
        """
        Configure camera to full frame and 1x1 binning and raw
        """
        ccdinfo = self.ccd_info
        self.RAW_MONO
        framedict = {
            'X': 0,
            'Y': 0,
            'width': int(ccdinfo['CCD_MAX_X']),
            'height': int(ccdinfo['CCD_MAX_Y'])
        }
        self.frame = framedict
        self.rgbframe(False)
        self.BINNING1
        self.UPLOAD_CLIENT
        self.FRAME_LIGHT
        self.GAIN = 10

    @property
    def BINNING2(self):
        """
        Configure camera to full frame and 2x2 binning
        """
        self.binning = {"X": 2, "Y": 2}
        ccdinfo = self.ccd_info
        framedict = {
            'X': 0,
            'Y': 0,
            'width': int(ccdinfo['CCD_MAX_X']),
            'height': int(ccdinfo['CCD_MAX_Y'])
        }
        self.frame = framedict
        self.rgbframe(True)

    @property
    def BINNING1(self):
        """
        Configure camera to full frame and 1x1 binning
        """
        self.binning = {"X": 1, "Y": 1}
        ccdinfo = self.ccd_info
        framedict = {
            'X': 0,
            'Y': 0,
            'width': int(ccdinfo['CCD_MAX_X']),
            'height': int(ccdinfo['CCD_MAX_Y'])
        }
        self.frame = framedict
        self.set_and_send_text(self.driver, 'RAW_FORMAT', 'RAWFORMAT14', 'Off')
        self.set_and_send_text(self.driver, 'RAW_FORMAT', 'RAWFORMAT13', 'Off')
        self.set_and_send_text(self.driver, 'RAW_FORMAT', 'RAWFORMAT12', 'Off')
        self.set_and_send_text(self.driver, 'RAW_FORMAT', 'RAWFORMAT11', 'Off')
        self.set_and_send_text(self.driver, 'RAW_FORMAT', 'RAWFORMAT10', 'Off')
        self.set_and_send_text(self.driver, 'RAW_FORMAT', 'RAWFORMAT9', 'Off')
        self.set_and_send_text(self.driver, 'RAW_FORMAT', 'RAWFORMAT8', 'Off')
        self.set_and_send_text(self.driver, 'RAW_FORMAT', 'RAWFORMAT7', 'Off')
        self.set_and_send_text(self.driver, 'RAW_FORMAT', 'RAWFORMAT6', 'Off')
        self.set_and_send_text(self.driver, 'RAW_FORMAT', 'RAWFORMAT5', 'Off')
        self.set_and_send_text(self.driver, 'RAW_FORMAT', 'RAWFORMAT4', 'Off')
        self.set_and_send_text(self.driver, 'RAW_FORMAT', 'RAWFORMAT3', 'Off')
        self.set_and_send_text(self.driver, 'RAW_FORMAT', 'RAWFORMAT2', 'Off')
        self.set_and_send_text(self.driver, 'RAW_FORMAT', 'RAWFORMAT1', 'Off')      
        self.set_and_send_text(self.driver, 'RAW_FORMAT', 'RAWFORMAT0', 'On')
        self.rgbframe(False)

    def rgbframe(self, binning=False):
        """
        Configure CCD_PROCFRAME.WIDTH and CCD_PROCFRAME.HEIGHT
        """
        ccdinfo = self.ccd_info
        x = int(ccdinfo['CCD_MAX_X'])
        y = int(ccdinfo['CCD_MAX_Y'])
        if binning:
            self.set_and_send_float(self.driver, 'CCD_PROCFRAME', 'WIDTH', int(x/2)) 
            self.set_and_send_float(self.driver, 'CCD_PROCFRAME', 'HEIGHT', int(y/2)) 
        else:
            self.set_and_send_float(self.driver, 'CCD_PROCFRAME', 'WIDTH', x) 
            self.set_and_send_float(self.driver, 'CCD_PROCFRAME', 'HEIGHT', y) 

    @property
    def FRAME_LIGHT(self):
        """
        Turn CCD_FRAME_TYPE.FRAME_LIGHT=On
        """
        self.set_and_send_switchvector_by_elementlabel(self.driver, 'CCD_FRAME_TYPE', 'Light')

    @property
    def FRAME_BIAS(self):
        """
        Turn CCD_FRAME_TYPE.FRAME_BIAS=On
        """
        self.set_and_send_switchvector_by_elementlabel(self.driver, 'CCD_FRAME_TYPE', 'Bias')

    @property
    def FRAME_DARK(self):
        """
        Turn CCD_FRAME_TYPE.FRAME_DARK=On
        """
        self.set_and_send_switchvector_by_elementlabel(self.driver, 'CCD_FRAME_TYPE', 'Dark')

    @property
    def FRAME_FLAT(self):
        """
        Turn CCD_FRAME_TYPE.FRAME_FLAT=On
        """
        self.set_and_send_switchvector_by_elementlabel(self.driver, 'CCD_FRAME_TYPE', 'Flat')
    
    @property
    def UPLOAD_LOCAL(self):
        """
        Turn UPLOAD_MODE.UPLOAD_LOCAL=On
        """
        self.set_and_send_switchvector_by_elementlabel(self.driver, 'UPLOAD_MODE', 'Local')

    @property
    def UPLOAD_CLIENT(self):
        """
        Turn UPLOAD_MODE.UPLOAD_CLIENT=On
        """
        self.set_and_send_switchvector_by_elementlabel(self.driver, 'UPLOAD_MODE', 'Client')

    def UPLOAD_DIR(self, string):
        """
        Set UPLOAD_SETTINGS.UPLOAD_DIR
        """
        if len(string) > 0:
            self.set_and_send_text(self.driver, 'UPLOAD_SETTINGS', 'UPLOAD_DIR', string)
     
    def UPLOAD_PREFIX(self, string):
        """
        Set UPLOAD_SETTINGS.UPLOAD_PREFIX
        """
        if len(string) > 0:
            self.set_and_send_text(self.driver, 'UPLOAD_SETTINGS', 'UPLOAD_PREFIX', string)       
   
    def expose(self, exptime=1.0, exptype="Light"):
        """
        Take exposure and return FITS data
        """
        self.ctrl = 1
        if exptype not in self.frame_types:
            raise Exception("Invalid exposure type, %s. Must be one of %s'." % (exptype, repr(self.frame_types)))

        if exptime < 0.0 or exptime > 3600.0:
            raise Exception("Invalid exposure time, %f. Must be >= 0 and <= 3600 sec." % exptime)

        ft_vec = self.set_and_send_switchvector_by_elementlabel(self.driver, "CCD_FRAME_TYPE", exptype)
        if self.debug:
            ft_vec.tell()

        exp_vec = self.set_and_send_float(self.driver, "CCD_EXPOSURE", "CCD_EXPOSURE_VALUE", exptime)
        if self.debug:
            exp_vec.tell()

        self.defvectorlist = []
        fitsdata = None

        local = self.get_text(self.driver, "UPLOAD_MODE", "UPLOAD_LOCAL")
        if local=='On':
            run = False
        else:
            run = True

        t = time.time()
        timeout = 1000 # 1000s (16 min)
        while run:
            self.process_receive_vector_queue()
            while self.receive_event_queue.empty() is False:               
                vector = self.receive_event_queue.get()
                if vector.tag.get_type() == "BLOBVector":
                    log.info("Reading FITS image out...")
                    blob = vector.get_first_element()              
                    if blob.get_plain_format() == ".fits":
                        buf = io.BytesIO(blob.get_data())
                        fitsdata = fits.open(buf)
                        if 'FILTER' not in fitsdata[0].header:
                            fitsdata[0].header['FILTER'] = 'L'
                        fitsdata[0].header['CAMERA'] = self.camera_name
                        self.ctrl = 0
                        run = False
                        break
                    
                if vector.tag.get_type() == "message":
                    msg = vector.get_text()
                    if "ERROR" in msg:
                        log.error(msg)
                    else:
                        if "saving image to file" in msg:
                            fitsdata = msg
                            self.ctrl = 0
                            run = False
                        log.info(msg)
            
            if ((time.time() - t) > timeout):
                log.warning("Exposure timed out.")
                self.ctrl = 0
                break
            time.sleep(1)
            
        self.ctrl = 0
        return fitsdata

    @property
    def isfile(self):
        """
        Validated FITS file for local
        """
        self.ctrl = 1
        run = True
        t = time.time()
        timeout = 1000 # 1000s (16 min)
        self.defvectorlist = []
        while run:
            self.process_receive_vector_queue()
            while self.receive_event_queue.empty() is False:               
                vector = self.receive_event_queue.get()                   
                if vector.tag.get_type() == "message":
                    msg = vector.get_text()
                    if "ERROR" in msg:
                        log.error(msg)
                    else:
                        if "saving image to file" in msg:
                            fitsdata = msg
                            self.ctrl = 0
                            run = False
                        log.info(msg)
            
            if ((time.time() - t) > timeout):
                log.warning("Exposure timed out.")
                self.ctrl = 0
                break
            time.sleep(1)
            
        self.ctrl = 0
        return fitsdata
        

