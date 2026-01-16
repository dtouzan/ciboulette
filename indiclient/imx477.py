# Licensed under GPL3 (see LICENSE)
# coding=utf-8

"""
Classes and utility functions for communicating with cameras via the INDI protocol, http://www.indilib.org.

# indi_pylibcamera
indi_pylibcamera.CAMERA_SELECTION.CAM0=On
indi_pylibcamera.CONNECTION.CONNECT=On
indi_pylibcamera.CONNECTION.DISCONNECT=Off
indi_pylibcamera.DRIVER_INFO.DRIVER_NAME=indi_pylibcamera
indi_pylibcamera.DRIVER_INFO.DRIVER_EXEC=/home/ut1/astropy/bin/indi_pylibcamera
indi_pylibcamera.DRIVER_INFO.DRIVER_VERSION=2.4.0
indi_pylibcamera.DRIVER_INFO.DRIVER_INTERFACE=2
indi_pylibcamera.LOGGING_LEVEL.LOGGING_DEBUG=Off
indi_pylibcamera.LOGGING_LEVEL.LOGGING_INFO=On
indi_pylibcamera.LOGGING_LEVEL.LOGGING_WARN=Off
indi_pylibcamera.LOGGING_LEVEL.LOGGING_ERROR=Off
indi_pylibcamera.POLLING_PERIOD.PERIOD_MS=1000
indi_pylibcamera.GEOGRAPHIC_COORD.LAT=0
indi_pylibcamera.GEOGRAPHIC_COORD.LONG=0
indi_pylibcamera.GEOGRAPHIC_COORD.ELEV=0
indi_pylibcamera.EQUATORIAL_EOD_COORD.RA=0
indi_pylibcamera.EQUATORIAL_EOD_COORD.DEC=0
indi_pylibcamera.TELESCOPE_PIER_SIDE.PIER_WEST=On
indi_pylibcamera.TELESCOPE_PIER_SIDE.PIER_EAST=Off
indi_pylibcamera.TELESCOPE_INFO.TELESCOPE_APERTURE=0
indi_pylibcamera.TELESCOPE_INFO.TELESCOPE_FOCAL_LENGTH=0
indi_pylibcamera.TELESCOPE_INFO.GUIDER_APERTURE=0
indi_pylibcamera.TELESCOPE_INFO.GUIDER_FOCAL_LENGTH=0
indi_pylibcamera.CAMERA_LENS.PRIMARY_LENS=On
indi_pylibcamera.CAMERA_LENS.GUIDER_LENS=Off
indi_pylibcamera.DO_SNOOPING.SNOOP=On
indi_pylibcamera.DO_SNOOPING.NO_SNOOP=Off
indi_pylibcamera.ACTIVE_DEVICES.ACTIVE_TELESCOPE=
indi_pylibcamera.CAMERA_INFO.CAMERA_MODEL=imx477
indi_pylibcamera.CAMERA_INFO.CAMERA_PIXELARRAYSIZE=(4056, 3040)
indi_pylibcamera.CAMERA_INFO.CAMERA_PIXELARRAYACTIVEAREA=[(8, 16, 4056, 3040)]
indi_pylibcamera.CAMERA_INFO.CAMERA_UNITCELLSIZE=(1550, 1550)
indi_pylibcamera.CCD_CAPTURE_FORMAT.INDI_RAW=On
indi_pylibcamera.CCD_CAPTURE_FORMAT.INDI_RGB=Off
indi_pylibcamera.RAW_FORMAT.RAWFORMAT0=On
indi_pylibcamera.RAW_FORMAT.RAWFORMAT1=Off
indi_pylibcamera.RAW_FORMAT.RAWFORMAT2=Off
indi_pylibcamera.RAW_FORMAT.RAWFORMAT3=Off
indi_pylibcamera.CCD_PROCFRAME.WIDTH=4056
indi_pylibcamera.CCD_PROCFRAME.HEIGHT=3040
indi_pylibcamera.CAMCTRL_AEENABLE.INDI_ENABLED=Off
indi_pylibcamera.CAMCTRL_AEENABLE.INDI_DISABLED=On
indi_pylibcamera.CAMCTRL_AECONSTRAINTMODE.NORMAL=On
indi_pylibcamera.CAMCTRL_AECONSTRAINTMODE.HIGHLIGHT=Off
indi_pylibcamera.CAMCTRL_AECONSTRAINTMODE.SHADOWS=Off
indi_pylibcamera.CAMCTRL_AECONSTRAINTMODE.CUSTOM=Off
indi_pylibcamera.CAMCTRL_AEEXPOSUREMODE.NORMAL=On
indi_pylibcamera.CAMCTRL_AEEXPOSUREMODE.SHORT=Off
indi_pylibcamera.CAMCTRL_AEEXPOSUREMODE.LONG=Off
indi_pylibcamera.CAMCTRL_AEEXPOSUREMODE.CUSTOM=Off
indi_pylibcamera.CAMCTRL_AEMETERINGMODE.CENTREWEIGHTED=On
indi_pylibcamera.CAMCTRL_AEMETERINGMODE.SPOT=Off
indi_pylibcamera.CAMCTRL_AEMETERINGMODE.MATRIX=Off
indi_pylibcamera.CAMCTRL_AEMETERINGMODE.CUSTOM=Off
indi_pylibcamera.CAMCTRL_AWBENABLE.INDI_ENABLED=Off
indi_pylibcamera.CAMCTRL_AWBENABLE.INDI_DISABLED=On
indi_pylibcamera.CAMCTRL_AWBMODE.AUTO=On
indi_pylibcamera.CAMCTRL_AWBMODE.TUNGSTEN=Off
indi_pylibcamera.CAMCTRL_AWBMODE.FLUORESCENT=Off
indi_pylibcamera.CAMCTRL_AWBMODE.INDOOR=Off
indi_pylibcamera.CAMCTRL_AWBMODE.DAYLIGHT=Off
indi_pylibcamera.CAMCTRL_AWBMODE.CLOUDY=Off
indi_pylibcamera.CAMCTRL_AWBMODE.CUSTOM=Off
indi_pylibcamera.CAMCTRL_BRIGHTNESS.BRIGHTNESS=0.0
indi_pylibcamera.CAMCTRL_COLOURGAINS.REDGAIN=2.0
indi_pylibcamera.CAMCTRL_COLOURGAINS.BLUEGAIN=2.0
indi_pylibcamera.CAMCTRL_CONTRAST.CONTRAST=1.0
indi_pylibcamera.CAMCTRL_EXPOSUREVALUE.EXPOSUREVALUE=0.0
indi_pylibcamera.CAMCTRL_NOISEREDUCTIONMODE.OFF=On
indi_pylibcamera.CAMCTRL_NOISEREDUCTIONMODE.FAST=Off
indi_pylibcamera.CAMCTRL_NOISEREDUCTIONMODE.HIGHQUALITY=Off
indi_pylibcamera.CAMCTRL_SATURATION.SATURATION=1.0
indi_pylibcamera.CAMCTRL_SHARPNESS.SHARPNESS=0.0
indi_pylibcamera.CCD_EXPOSURE.CCD_EXPOSURE_VALUE=1.0
indi_pylibcamera.CCD_ABORT_EXPOSURE.ABORT=Off
indi_pylibcamera.CCD_FRAME.X=0
indi_pylibcamera.CCD_FRAME.Y=0
indi_pylibcamera.CCD_FRAME.WIDTH=4056
indi_pylibcamera.CCD_FRAME.HEIGHT=3040
indi_pylibcamera.CCD_BINNING.HOR_BIN=1
indi_pylibcamera.CCD_BINNING.VER_BIN=1
indi_pylibcamera.CCD_TEMPERATURE.CCD_TEMPERATURE_VALUE=0
indi_pylibcamera.CCD_INFO.CCD_MAX_X=4056
indi_pylibcamera.CCD_INFO.CCD_MAX_Y=3040
indi_pylibcamera.CCD_INFO.CCD_PIXEL_SIZE=1.55
indi_pylibcamera.CCD_INFO.CCD_PIXEL_SIZE_X=1.55
indi_pylibcamera.CCD_INFO.CCD_PIXEL_SIZE_Y=1.55
indi_pylibcamera.CCD_INFO.CCD_BITSPERPIXEL=12
indi_pylibcamera.CCD_COMPRESSION.CCD_COMPRESS=Off
indi_pylibcamera.CCD_COMPRESSION.CCD_RAW=On
indi_pylibcamera.CCD_FRAME_TYPE.FRAME_LIGHT=On
indi_pylibcamera.CCD_FRAME_TYPE.FRAME_BIAS=Off
indi_pylibcamera.CCD_FRAME_TYPE.FRAME_DARK=Off
indi_pylibcamera.CCD_FRAME_TYPE.FRAME_FLAT=Off
indi_pylibcamera.UPLOAD_MODE.UPLOAD_CLIENT=On
indi_pylibcamera.UPLOAD_MODE.UPLOAD_LOCAL=Off
indi_pylibcamera.UPLOAD_MODE.UPLOAD_BOTH=Off
indi_pylibcamera.UPLOAD_SETTINGS.UPLOAD_DIR=/home/ut1
indi_pylibcamera.UPLOAD_SETTINGS.UPLOAD_PREFIX=IMAGE_XXX
indi_pylibcamera.CCD_FAST_TOGGLE.INDI_ENABLED=Off
indi_pylibcamera.CCD_FAST_TOGGLE.INDI_DISABLED=On
indi_pylibcamera.CCD_FAST_COUNT.FRAMES=1
indi_pylibcamera.CCD_GAIN.GAIN=5.0
indi_pylibcamera.APPLY_CONFIG.CONFIG1=On
indi_pylibcamera.APPLY_CONFIG.CONFIG2=Off
indi_pylibcamera.APPLY_CONFIG.CONFIG3=Off
indi_pylibcamera.APPLY_CONFIG.CONFIG4=Off
indi_pylibcamera.APPLY_CONFIG.CONFIG5=Off
indi_pylibcamera.APPLY_CONFIG.CONFIG6=Off
indi_pylibcamera.CONFIG_NAME.CONFIG_NAME=
indi_pylibcamera.CONFIG_PROCESS.CONFIG_LOAD=Off
indi_pylibcamera.CONFIG_PROCESS.CONFIG_SAVE=Off
indi_pylibcamera.CONFIG_PROCESS.CONFIG_DEFAULT=Off
indi_pylibcamera.CONFIG_PROCESS.CONFIG_PURGE=Off
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
    def gain(self):
        self.process_events()
        gain = self.get_float(self.driver, "CCD_GAIN", "GAIN")
        return gain

    @gain.setter
    def gain(self,f):
        if f >=0 and f <=100:
            self.set_and_send_float(self.driver, 'CCD_GAIN', 'GAIN', f) 
            self.process_events()
            
    @property
    def HDUComment(self):
        """
        Return: tag HDUL comment
        """
        return 'Raspicam imx477 V1 for astronomy'

    @property
    def compress(self):
        """
        Turn CCD_COMPRESSION.CCD_COMPRESS=On 
        """
        self.set_and_send_text(self.driver, "CCD_COMPRESSION", "CCD_RAW", "Off")
        self.set_and_send_text(self.driver, "CCD_COMPRESSION", "CCD_COMPRESS", "On")

    @property
    def uncompress(self):
        """
        Turn CCD_COMPRESSION.CCD_RAW=On 
        """
        self.set_and_send_text(self.driver, "CCD_COMPRESSION", "CCD_COMPRESS", "Off")
        self.set_and_send_text(self.driver, "CCD_COMPRESSION", "CCD_RAW", "On")

    @property
    def rgb(self):
        """
        Turn CCD_CAPTURE_FORMAT.INDI_RGB=On
        """
        self.set_and_send_switchvector_by_elementlabel(self.driver, "CCD_CAPTURE_FORMAT", "RGB")

    @property
    def raw(self):
        """
        Turn CCD_CAPTURE_FORMAT.INDI_RAW=On
        """
        self.set_and_send_switchvector_by_elementlabel(self.driver, "CCD_CAPTURE_FORMAT", "RAW")

    @property
    def mono(self):
        """
        Turn CCD_CAPTURE_FORMAT.RAW_MONO=On
        """
        self.set_and_send_switchvector_by_elementlabel(self.driver, "CCD_CAPTURE_FORMAT", "RAW_MONO")
        self.set_and_send_text(self.driver, "CCD_CAPTURE_FORMAT", "RAW_MONO", "On")
    
    @property
    def default(self):
        """
        Configure camera to full frame and 1x1 binning and raw
        """
        ccdinfo = self.ccd_info
        self.raw
        framedict = {
            'X': 0,
            'Y': 0,
            'width': int(ccdinfo['CCD_MAX_X']),
            'height': int(ccdinfo['CCD_MAX_Y'])
        }
        self.frame = framedict
        self.rgbframe(False)
        self.binning1
        self.ctrl = 0
        self.client
        self.gain = 5

    @property
    def binning2(self):
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
    def binning1(self):
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
    def local(self):
        """
        Turn UPLOAD_MODE.UPLOAD_LOCAL=On
        """
        self.set_and_send_switchvector_by_elementlabel(self.driver, 'UPLOAD_MODE', 'Local')

    @property
    def client(self):
        """
        Turn UPLOAD_MODE.UPLOAD_CLIENT=On
        """
        self.set_and_send_switchvector_by_elementlabel(self.driver, 'UPLOAD_MODE', 'Client')

    def dir(self, string):
        """
        Set UPLOAD_SETTINGS.UPLOAD_DIR
        """
        if len(string) > 0:
            self.set_and_send_text(self.driver, 'UPLOAD_SETTINGS', 'UPLOAD_DIR', string)
     
    def prefix(self, string):
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
        

