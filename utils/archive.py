"""
Archive class
"""


class Archive(object):
    
    def __init__(self, archive_table = 'dataset/archives'):
        self.archive_table = archive_table
     
    @property
    def readarchives(self):
        """
        Return table of archive of the fits files in the directory      
        """
        object_name = []
        frameid = []
        datatype = []
        RA = []
        DEC = []    
        arch = os.listdir(self.archive_table)   
        for file in arch:
            fits_file = get_pkg_data_filename(data_arch+'/'+file)
            hdu = fits.open(fits_file)[0]
            header = hdu.header
              
            object_name.append(header['OBJECT'])
            frameid.append(header['FRAMEID'])
            datatype.append(header['DATATYPE'])
            RA.append(header['CRVAL1'])
            DEC.append(header['CRVAL2'] )    
            
        return Table([object_name,frameid,datatype,RA,DEC], names=['ID','FRAMEID','DATATYPE','RA','DEC'])

    @property
    def MASTcreate(self)
        """
        Create MAST type file with fits archives file
        """
        return True