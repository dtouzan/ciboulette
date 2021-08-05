"""
Archive class
"""


class Archive(object):
    
    def __init__(self, archive_table = 'dataset/archives'):
        self.directory = archive_table
        self.dataset = []       
     
    @property
    def read(self):
        """
        Return table of archive of the fits files in the directory      
        """
        object_name = []
        observer = []
        instrument = []
        telescope = []
        frameid = []
        frame = []
        datatype = []
        filter_name = []
        focal =[]
        exptime =[]
        date_obs =[]
        jd = []
        ra = []
        dec = []    
        arch = os.listdir(self.self.directory)   
        for file in arch:
            fits_file = get_pkg_data_filename(self.directory)
            hdu = fits.open(fits_file)[0]
            header = hdu.header             
            object_name.append(header['OBJECT'])
            observer.append(header['OBSERVER'])     
            instrument.append(header['INSTRUME']) 
            telescope.append(header['TELESCOP'])
            frameid.append(header['FRAMEID'])
            frame.append(header['FRAME'])
            datatype.append(header['DATATYPE'])
            filter_name.append(header['FILTER'])
            focal.append(header['FOCALLEN'])
            exptime.append(header['EXPTIME'])
            date_obs.append(header['DATE-OBS'])
            jd.append(header['JD-OBS'])
            ra.append(header['CRVAL1'])
            dec.append(header['CRVAL2'] )    
             
        self.dataset = Table([object_name,observer,instrument,telescope,frameid,frame,datatype,filter_name,focal,exptime,date_obs,jd,ra,dec], 
                             names=['ID','OBSERVER','INSTRUME','TELESCOP','FRAMEID','FRAME','DATATYPE','FILTER','FOCALLEN','EXPTIME','DATE-OBS','JD-OBS','RA','DEC'])

