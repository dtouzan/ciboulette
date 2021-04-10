"""
Sector class
"""

import os
from astropy.table import Table
from astropy.io import fits
from astroquery.vizier import Vizier
from astroquery.simbad import Simbad
from astropy.coordinates import SkyCoord, Angle
from astropy import units as u
from astropy import wcs
from astropy.time import Time
from astropy.io import ascii
from astroquery.imcce import Miriade, MiriadeClass
from ciboulette.base import constent

class Sector(object):
    
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
        ra = []
        dec = []
        marker = []    
        for line in eph:
            ra.append(line['RA'])
            dec.append(line['DEC'])
            marker.append(int(line['V']))                        
        return Table([ra,dec,marker], names=['RA', 'DEC', 'MARKER'])        
    
    def miriademoon(self,epoch,location):     
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
        eph = Miriade.get_ephemerides('p:moon', epoch=epoch, epoch_step='1m', epoch_nsteps=1, coordtype=1, location=location)
        ra = []
        dec = []
        marker = []    
        for line in eph:
            ra.append(line['RA'])
            dec.append(line['DEC'])
            if line['V'] < -1:
                marker.append(-int(line['V']))
            else: 
                marker.append(1)                   
        return Table([ra,dec,marker], names=['RA', 'DEC', 'MARKER']) 
     
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

    @property
    def MilkyWay(self):
        """
        Return Table of MilkyWay
        """
        name_id = ['Mu. Vel','Psi Vel','Gam Pyx','16 Pup','Alp Mon','Del Mon','Zet Gem','The Gem','The Aur','Alp Aur',
                   'Mu. Per','Alp Per','Tau Per','Eta Per','HD21291','Eps Cas','Kap Cas','M 52','Iot Cep','Ksi Cep',
                   'Del Cyg','Gam Lyr','111 Her','Bet Oph','Nu. Oph','Eta Oph','Del Sco','HD148703','Eps Lup','Alp Lup','Eps Cen',
                   'HD116458','HD145689','Eps01 Ara','Mu. Ara','Eps CrA','Rho01 Sgr','Nu. Aql','HD193472','Zet Cyg',
                   '2 Lac','Lam And','HD4222','Phi Per','Kap Per','Eps Per','HD28503','4 Aur','Bet Tau','Zet Tau',
                   '111 Tau','Alp Ori','HD44333','HD43318','Bet Mon','Iot CMa','HD61899','Gam Vel','Iot Car','HD91375','Mu. Vel']

        ra = [161.69312,142.67338,132.63212,122.25673,115.31136,107.96608,106.02718,103.19723,89.93061,79.17297,63.72448,
              51.08093,43.56441,42.67439,52.26719,28.59928,8.25001,351.20167,342.41911,330.95067,296.24402,284.73591,
              281.75573,265.86789,269.75658,257.59477,240.08330,247.84547,230.67016,220.48213,204.97176,
              201.45860,244.27182,254.89605,266.03613,284.67976,290.41800,291.62953,305.00080,318.23408,335.25664,354.39237,
              11.32126,25.91539,47.37553,59.46357,67.85040,74.81455,81.57312,84.41120,81.10765,88.79310,95.35725,
              93.89185,97.20445,104.03425,114.94940,122.38307,139.27231,157.58439,161.69312]
        
        dec= [-49.42058,-40.46628,-27.70933,-19.24505,-9.55125,-0.49273,20.57028,33.96098,37.21215,45.99548,48.40923,
              49.86102,52.76245,55.89541,59.94033,63.66999,62.93177,61.59317,66.19967,64.62850,45.13109,32.68957,
              18.18221,4.56823,-9.77431,-15.72432,-22.62193,-34.70447,-44.68977,-47.38834,-53.46646,
              -70.62725,-67.94178,-53.16031,-51.83518,-37.10798,-17.84707,0.33854,13.54804,30.22661,46.53658,46.45567,
              55.22137,50.68865,44.85667,40.01008,40.01010,37.88967,28.60643,21.14243,17.38349,7.40713,2.26840,-0.51347,
              -7.03323,-17.05423,-38.26060,-47.33652,-59.27516,-71.99297,-49.42058]

        return Table([name_id,ra,dec], names=['MAIN_ID', 'RA', 'DEC'])     
    
    @property
    def smc(self):
        """
        Return Table of SMC
        """
        name_id = ['smc01','smc02','smc03','smc04','smc05','smc06','smc07','smc08','smc09',
                   'smc10','smc11','smc12','smc13','smc14','smc15','smc16','smc17','smc18','smc19']
    
        ra = [15.71412,13.35367,12.35204,11.46044,11.04552,10.56770,10.59704,11.87215,13.35488,
              14.05924,14.38190,14.35466,14.39971,14.53188,14.85369,15.78852,16.07202,16.09278,15.71412]
        
        dec= [-71.80571,-72.10860,-72.42878,-72.64489,-72.83957,-73.22119,-73.38194,-73.59739,-73.66183,-73.57383,
              -73.36562,-73.03905,-72.74186,-72.57571,-72.41027,-72.25918,-72.17162,-72.06272,-71.80571] 
       
        return Table([name_id,ra,dec], names=['MAIN_ID', 'RA', 'DEC'])
            
    @property
    def lmc(self):
        """
        Return Table of LMC
        """
        name_id = ['lmc01','lmc02','lmc03','lmc04','lmc05','lmc06','lmc07','lmc08','lmc09','lmc10','lmc11',
                   'lmc12','lmc13','lmc14','lmc15','lmc16','lmc17','lmc18','lmc19','lmc20','lmc21','lmc22',]
    
        ra = [76.93533,75.85622,75.06883,75.18691,77.14843,78.95547,80.53301,83.01741,84.75381,85.35961,85.67452,85.75220,
              85.60654,85.26041,84.61699,83.88328,83.12758,82.58079,81.56873,79.37675,77.83528,76.93533]
        
        dec= [-68.29889,-68.75113,-69.14459,-69.37773,-69.68735,-69.96248,-70.27100,-70.44125,-70.41966,-70.35244,-70.12480,-69.58027,
              -69.21964,-68.97936,-68.95427,-69.08469,-69.34739,-69.48988,-69.42599,-68.93654,-68.53427,-68.29889] 
       
        return Table([name_id,ra,dec], names=['MAIN_ID', 'RA', 'DEC']) 

    @property
    def constellation(self):
        """
        Return Table of cygnus constellation
        """
        name_id = ['cyg01','cyg02','cyg03','cyg04','cyg05','cyg06','cyg04','cyg08','cyg09','cyg10','cyg11','cyg12','cyg13','cyg014',
                   'cyg15','cyg16','cyg17','cyg18','cyg19','cyg20','cyg21','cyg22','cyg23','cyg24','cyg25','cyg26','cyg27','cyg28']
    
        ra = [290.27454,296.37044,296.37566,315.01756,315.16620,327.28906,327.35796,329.40071,329.51316,330.69816,330.75935,309.92472,309.58739,308.39034,
              308.26438,297.17667,297.16272,291.68812,292.00975,287.00677,287.17769,288.31124,288.40571,292.07598,292.18753,291.54741,290.09924,290.27454]
        
        dec= [27.75807,27.71632,29.32198,29.43792,28.47269,28.59526,36.61681,36.69658,44.43569,44.73737,55.48212,55.37129,61.32503,61.36405,
              59.92392,59.63124,58.21273,58.31922,55.67147,55.67877,47.82238,47.67719,43.67811,43.72546,36.82807,30.33083,30.21923,27.75807]
       
        return Table([name_id,ra,dec], names=['MAIN_ID', 'RA', 'DEC'])

    @property
    def opencluster(self):
        """
        Return Table of Open Cluster, constraints Vmag < 18.1
        """
        result = Simbad.query_criteria('Vmag<18.1',maintype='OpC')
        ra = []
        dec = []
        main_id = []    
        for line in result:
            ra.append(line['RA'])
            dec.append(line['DEC'])
            main_id.append(line['MAIN_ID'])                        
        return Table([main_id,ra,dec], names=['MAIN_ID', 'RA', 'DEC'])        

    @property
    def HerbigAeBeStars(self):
        """
        Return Table of HerbigAeBeStars
        Catalog Title: Herbig Ae/Be accretion rates & mechanisms (Wichittanakom+ 2020)
        Accretion properties of Herbig Ae/Be stars in Vioque et al. (2018, Cat. J/A+A/620/A128)
        J/MNRAS/493/234
        """
        v = Vizier(catalog="J/MNRAS/493/234", columns=['_RAJ2000', '_DEJ2000', '*'])
        v.ROW_LIMIT = 50000
        result = v.query_constraints()        
        ra = []
        dec = []
        main_id = []    
        for table_name in result.keys():
            table = result[table_name]
            for line in table:
                ra.append(line[0])
                dec.append(line[1])
                main_id.append('Herbig Ae/Be')                        
        return Table([main_id,ra,dec], names=['MAIN_ID', 'RA', 'DEC'])        

    @property
    def CepheidStars(self):
        """
        Return Table of Cepheid
        Catalog Title: I/345/cepheid       
        """
        v = Vizier(catalog="I/345/cepheid", columns=['_RAJ2000', '_DEJ2000', '*'])
        v.ROW_LIMIT = 50000
        result = v.query_constraints()        
        ra = []
        dec = []
        main_id = []    
        for table_name in result.keys():
            table = result[table_name]
            for line in table:
                ra.append(line[0])
                dec.append(line[1])
                main_id.append(line[2])                        
        return Table([main_id,ra,dec], names=['MAIN_ID', 'RA', 'DEC'])  
    
    def aavso(self,string):
        """
        Return AAVSO variable star 
        Catalog Title: B/vsx/vsx       
        """       
        v = Vizier(catalog='B/vsx/vsx', columns=['_RAJ2000', '_DEJ2000', '*'])
        v.ROW_LIMIT = 500000
        result = v.query_constraints(Name = string)        
        for table_name in result.keys():
            table = result[table_name]                       
        return table
