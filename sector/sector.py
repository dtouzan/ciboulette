"""Sector class

"""

import os
from astropy.table import Table
from astropy.io import fits
from astroquery.vizier import Vizier
from astropy.coordinates import SkyCoord, Angle
from astropy import units as u


class Sector:
    
    def __init__(self):
        
        self.data = []
        

    def readarchives(self,data_arch):
        """Return table of archive, sector name, frame ID, data type, ra, dec of the fits files in the directory
        
        Attributes:
                data_arch (str): directory name.
                
        """

        t_object = []
        t_frameid = []
        t_datatype = []
        t_RA = []
        t_DEC = []
    
        arch = os.listdir(data_arch)
    
        for file in arch:

            fits_file = get_pkg_data_filename(data_arch+'/'+file)

            hdu = fits.open(fits_file)[0]
            header = hdu.header
            h_object = header['OBJECT']
            h_frameid = header['FRAMEID']
            h_datatype = header['DATATYPE']
            h_RA =  header['CRVAL1']
            h_DEC =  header['CRVAL2']
        
            protocol = h_object.split('R')[0]
        
            if protocol == 'SECTO':
                t_object.append(h_object)
                t_frameid.append(h_frameid)
                t_datatype.append(h_datatype)
                t_RA.append(h_RA)
                t_DEC.append(h_DEC)
    
        return Table([t_object,t_frameid,t_datatype,t_RA,t_DEC], names=['SECTOR','FRAMEID','DATATYPE','RA','DEC'])

    
    def regionincatalog(self,astre_ra,astre_dec,angle_width,angle_height,mag,catalog_name,field_ra,field_dec,field_mag):
        """Returns the table of RA, DEC and markers
        
        Attributes:
                astre_ra (float)        : RA
                astre_dec (float)       : DEC
                angle_width (float)     : Degrees
                angle_height (float)    : Degrees
                mag (float)             : Maximun magnitude
                catalog_name (str)      : Catalog Vizier name
                field_ra (float)        : field of RA
                field_dec (float)       : Field of DEC,
                field_mag (float)       : Field maximun magnitude
        
        """
        
        table_ra = []
        table_dec = []
        table_marker = []
    
        # Recherche dans le catalog 
        # Field catalog : _RAJ2000, _DEJ2000, Vmag, r'mag, Gmag ...
        v = Vizier(columns=[field_ra, field_dec, field_mag])
    
        # Nombre limite de recherche
        v.ROW_LIMIT = 500000
    
        # Recherche et création de la table
        mag_format = '<'+str(mag)
        result = v.query_region(SkyCoord(ra=astre_ra, dec=astre_dec, unit=(u.deg, u.deg),frame='icrs'), width=Angle(angle_width, "deg"), 
                                height=Angle(angle_height, "deg"), catalog=catalog_name,column_filters={'Vmag':mag_format})
        
        for table_name in result.keys():
            table = result[table_name]
            for line in table:
                ra = float(line[0])
                dec = float(line[1])
                Mv = float(line[2])
                if Mv != 'masked' :
                    marker_size = 1
                    if Mv < 12:
                        marker_size = 1
                    if Mv < 11:
                        marker_size = 1    
                    if Mv < 10:
                        marker_size = 3  
                    if Mv < 9:
                        marker_size = 5
                    if Mv < 8:
                        marker_size = 8
                    if Mv < 7:
                        marker_size = 20
                    if Mv < 6:
                        marker_size = 35
                    if Mv < 5:
                        marker_size = 50
                        
                    table_ra.append(ra)
                    table_dec.append(dec)
                    table_marker.append(marker_size)
                
                else :
                    table_ra.append(ra)
                    table_dec.append(dec)
                    table_Marker.append(0)
        
            return Table([table_ra,table_dec,table_marker], names=['RA', 'DEC', 'MARKER'])