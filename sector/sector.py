"""
Sector class
"""

import os
from astropy.table import Table
from astropy.io import fits
from astroquery.vizier import Vizier
from astropy.coordinates import SkyCoord, Angle
from astropy import units as u
from astropy import wcs
from astroquery.imcce import Miriade, MiriadeClass
from ciboulette.base import constent

class Sector:
    
    def __init__(self):
        
        self.data = []
        

    def readarchives(self,data_arch):
        """
        Return table of archive, sector name, frame ID, data type, ra, dec of the fits files in the directory      
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
        """
        Returns the table of RA, DEC and markers        
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
                                height=Angle(angle_height, "deg"), catalog=catalog_name,column_filters={'Gmag':mag_format}) 
        if mag <= 14 :
            stars = constent.starslow
        else:
            stars = constent.starshight         
        for table_name in result.keys():
            table = result[table_name]
            for line in table:
                ra = float(line[0])
                dec = float(line[1])
                mv = float(line[2])
                if mv != 'masked' :
                    marker_size = stars[int(mv)+stars[0]]
                    table_ra.append(ra)
                    table_dec.append(dec)
                    table_marker.append(marker_size)              
            return Table([table_ra,table_dec,table_marker], names=['RA', 'DEC', 'MARKER'])

    def miriadeincatalog(self,target,epoch,epoch_step,epoch_nsteps,coordtype,location):     
        """
        Returns the table of RA, DEC and markers with Miriade calulator
        Attributes:
                target (string)         : target
                epoch (Time)            : epoch
                epoch_step (string)     : Miriade definition
                epoch_nsteps (int)      : Iteration Number
                coordtype (int)         : Miriade definition
                location (string)       : Miriade definition
        """
        eph = Miriade.get_ephemerides(target, epoch=epoch, epoch_step=epoch_step, epoch_nsteps=epoch_nsteps, coordtype=coordtype, location=location)
        table_ra = []
        table_dec = []
        table_marker = []    
        for line in eph:
            table_ra.append(line['RA'])
            table_dec.append(line['DEC'])
            table_marker.append(int(line['V']))                        
        return Table([table_ra,table_dec,table_marker], names=['RA', 'DEC', 'MARKER'])        
        
    def WCS(self,ra,dec,naxis1,naxis2,binXY,pixelXY,focal):
        """
        Return WSC for sector
        """    
        # Element for CRPIX
        crpix1 = int(naxis1)/2
        crpix2 = int(naxis2)/2
        # Element for CDELT
        cdelt1 = (206*int(pixelXY)*int(binXY)/focal)/3600
        cdelt2 = (206*int(pixelXY)*int(binXY)/focal)/3600
        # Header WCS
        w = wcs.WCS(naxis=2)
        w.wcs.ctype = ["RA---TAN", "DEC--TAN"]
        # CRVAL 
        w.wcs.crval = [ra * 15, dec] 
        # CRPIX Vecteur à 2 éléments donnant les coordonnées X et Y du pixel de référence 
        # (def = NAXIS / 2) dans la convention FITS (le premier pixel est 1,1)
        w.wcs.crpix = [crpix1, crpix2]
        # CDELT Vecteur à 2 éléments donnant l'incrément physique au pixel de référence
        w.wcs.cdelt = [-cdelt1, cdelt2]      
        return w