"""
Maps class
"""

__authors__ = ("Dominique Touzan","ciboulette module")
__contact__ = ("dtouzan@gmail.com","https://github.com/dtouzan/ciboulette")
__copyright__ = "MIT"
__date__ = "2024-11-27"
__version__= "1.0.0"

# Global mods
import matplotlib.pyplot as plt
# Astropy mods
from astropy.table import Table
from astropy import wcs
from astropy import units as u
from astropy.visualization.wcsaxes import add_scalebar
#  local mods
from ciboulette.sector import sector, markers 
from ciboulette.base import constant

            
    
class Map(object):
    
    def __init__(self):
        self.size = 5
        self.title = ''
        self.databaselist = []
        self.WCS = wcs
        self.unlimited

    
    def new(self, table=dict()):
        """
        Set data, WCS for display
            table: {'RA': right ascention hour, 
                    'DEC': declination degre, 
                    'naxis1': naxis1, 
                    'naxis2': naxis2, 
                    'binXY': binning, 
                    'pixelXY': pixel size, 
                    'focal': focal, 
                    'projection': 'TAN'}
        """
        if not table:
            table = {'RA': 0, 
                     'DEC': 0, 
                     'naxis1': 4000, 
                     'naxis2': 3000, 
                     'binXY': 1, 
                     'pixelXY': 1.55, 
                     'focal': 85, 
                     'projection': 'TAN'}

        ra = table['RA']
        dec = table['DEC']
        naxis1 = table['naxis1']
        naxis2 = table['naxis2']
        binXY = table['binXY']
        pixelXY = table['pixelXY']
        focal = table['focal']
        projection = table['projection']    
        sct = sector.Sector()
        self.WCS = sct.WCS(ra,
                           dec,
                           naxis1,
                           naxis2,
                           binXY,
                           pixelXY,
                           focal,
                           projection)
        #field_RA = WCS.wcs.cdelt[0]*self.naxis1
        self.size = self.WCS.wcs.cdelt[1]*naxis2
        self.title = ''
        self.databaselist = []


    def into(self, table=dict()):
        """
        Return true if in size
            table: {'ra': right ascention hour, 
                    'dec': declination degre}        
        """
        if not table:
            table = {'ra': 0, 
                     'dec': 0}
        value = False
        field = (self.size/2)
        ra_max = self.WCS.wcs.crval[0]+field
        ra_min = self.WCS.wcs.crval[0]-field
        dec_max = self.WCS.wcs.crval[1]+field
        dec_min = self.WCS.wcs.crval[1]-field
        if ra_min < table['ra'] < ra_max:
            if dec_min < table['dec'] < dec_max:
                value =True        
        return value

    
    @property
    def light(self):
        """
        Set magnitude 6
        """
        self.magnitude = 6

    
    @property
    def medium(self):
        """
        Set magnitude 12
        """
        self.magnitude = 12
        

    @property
    def low(self):
        """
        Set magnitude 18
        """
        self.magnitude = 18


    @property
    def unlimited(self):
        """
        Set magnitude -99
        """
        self.magnitude = -99

    
    def marker(self, table=dict(), style=dict()):
        """
        Set marker
            table: {'ra': 
                    right ascention hour, 
                    'dec':declination degre, 
                    'angle': angle, 
                    'main_id': source_id}
            style: {'color': 
                    'blue', 
                    'size': 1, 
                    'alpha': 0.4}
        """
        if not table:
            table = {'ra': 0, 
                     'dec': 0, 
                     'angle': 6, 
                     'main_id': 'marker'}
        if not style:
            style = {'color': 
                     'blue', 
                     'size': 1, 
                     'alpha': 0.4}

        sct = sector.Sector()
        data = markers.marker(sct.marker(table['ra'], 
                                         table['dec'], 
                                         table['angle'], 
                                         table['main_id']))
        if data.data:
            data.properties(style)
            data.title = 'marker'
            self.databaselist.append(data)      

    
    def constellations(self, table=dict(), style=dict()):
        """
        Set constellations
            table: {'title': 'name'}
            style: {'color': 'green', 
                    'size': 1, 
                    'alpha': 0.4}
        """
        if not table:
            table = {'title': 'CYG'}
        if not style:
            style = {'color': 
                     'green', 
                     'size': 1, 
                     'alpha': 0.4}

        sct = sector.Sector()
        data = markers.constellations(sct.constellations(table['title']))
        if data.data:
            data.properties(style)
            data.title = table['title']
            self.databaselist.append(data)      

            
    def gaiaedr3(self, style=dict()):
        """
        Set gaiaedr3 catalog
            style: {'color': 'black', 
                    'size': 1, 
                    'alpha': 0.4}
        """
        if not style:
            style = {'color': 'black', 
                     'size': 1, 
                     'alpha': 1}
        
        magnitude = 8
        field = self.size

        if field > 5:
            field = 5

        """
        if field <= 5:
            magnitude = 10
        if field <= 3:
            magnitude = 12.5
        if field <= 1.5: 
            magnitude = 14.5
        if field <= 0.75:
            magnitude = 16    
        if field <= 0.30:
            mamagnitudeg = 18  
        """
        if field <= 5:
            magnitude = 14
        if field <= 1.5:
            magnitude = 18  
        if field <= 0.5:
            magnitude = 25  
        
        catalog = 'I/350/gaiaedr3'
        sct = sector.Sector()
        data = markers.stars_gaiaedr3(sct.gaiaedr3(self.WCS.wcs.crval[0], 
                                                         self.WCS.wcs.crval[1],                                                  
                                                         field, 
                                                         field, 
                                                         magnitude))   
        if data.data:
            data.properties(style)
            data.title = 'gaia edr3.CDS.I/350/gaiaedr3'
            self.databaselist.append(data)      

        
    def trajectory(self,target,epoch,epoch_step,epoch_nsteps,latitude,longitude,elevation):
        """
        Set target, WCS and titlefor display
        Attribut:
                target (string)    : Miriade target
                epoch (string)     : Miriade epoch
                epoch_step (string): Miriade epoch_step 
                epoch_nsteps (int) : Miriade epoch_nsteps
                latitude (float)   : Site latitude
                longitude (float)  : Site longitude
                elevation (float)  : Site elevation
        """   
        sct = sector.Sector()
        location = str(longitude) + ' ' + str(latitude) + ' ' + str(elevation)
        self.target = sct.miriadeincatalog(target,epoch,epoch_step,epoch_nsteps,1,location)
        self.title = self.title+target+' | '+epoch.value+'\n'        


    def cursor(self, angle=30, style=dict()):
        """
        Set cursor map
            style: {'color': 'red', 
                    'size': 5, 
                    'alpha': 0.3}
        """
        if not style:
            style = {'color': 'red', 
                     'size': 5, 
                     'alpha': 0.3}

        table = {'ra': self.WCS.wcs.crval[0]/15, 
                 'dec': self.WCS.wcs.crval[1], 
                 'angle': angle, 'source': 'cursor'}
        sct = sector.Sector()
        data = markers.cursor(sct.marker(table['ra'], 
                                         table['dec'], 
                                         table['angle'], 
                                         table['source']))
        if data.data:
            data.properties(style)
            data.title = table['source']
            self.databaselist.append(data)      

    
    def opencluster(self, style=dict()):
        """
        Set open cluster map
            Open star cluster: OpC
            style: {'color': 'yellow', 
                    'size': 1, 
                    'alpha': 0.3}
        """
        if not style:
            style = {'color': 'yellow', 
                     'size': 1, 
                     'alpha': 0.3}

        sct = sector.Sector()
        result = sct.simbad(self.WCS.wcs.crval[0], 
                            self.WCS.wcs.crval[1], 
                            angle=self.size/2, 
                            magnitude=self.magnitude, 
                            otype="'OpC','As*'")
        data = markers.opencluster(result)
        if data.data:
            data.properties(style)
            data.title = 'Simbad.CDS open cluster'           
            self.databaselist.append(data)

    
    def globularcluster(self, style=dict()):
        """
        Set globular cluster map
        Gb = Globular star cluster, usually in the Milky Way Galaxy
            style: {'color': 'yellow', 
                    'size': 1, 
                    'alpha': 0.3}
        """
        if not style:
            style = {'color': 'yellow', 
                     'size': 1, 
                     'alpha': 0.3}

        sct = sector.Sector()
        data = markers.globularcluster(sct.simbad(self.WCS.wcs.crval[0], 
                                                  self.WCS.wcs.crval[1], 
                                                  angle=self.size/2, 
                                                  magnitude=self.magnitude, 
                                                  otype="'GlC'"))
        if data.data:
            data.properties(style)
            data.title = 'Simbad.CDS globular cluster'                   
            self.databaselist.append(data)

    
    def galaxy(self, style=dict()):
        """
        Set galaxy map
        Gx = Galaxy
            style: {'color': 'red', 
                    'size': 1, 
                    'alpha': 0.3}
        """
        if not style:
            style = {'color': 'red', 
                     'size': 1, 
                     'alpha': 0.3}

        sct = sector.Sector()
        data = markers.galaxy(sct.simbad(self.WCS.wcs.crval[0], 
                                         self.WCS.wcs.crval[1],
                                         angle=self.size/2, 
                                         magnitude=self.magnitude, 
                                         otype="'LSB','bCG','SBG','H2G','EmG','AGN','SyG','Sy1','Sy2','rG','LIN','QSO','Bla','BLL','GiC','PaG','GrG','CGG','ClG'"))
        if data.data:
            data.properties(style)
            data.title = 'Simbad.CDS galaxy'           
            self.databaselist.append(data)

    
    def planetarynebula(self, style=dict()):
        """
        Set planeta rynebula map
        Pl = Planetary nebula
            style: {'color': 'green', 
                    'size': 1, 
                    'alpha': 0.3}
        """
        if not style:
            style = {'color': 'green', 
                     'size': 1, 
                     'alpha': 0.3}

        sct = sector.Sector()
        data = markers.planetarynebula(sct.simbad(self.WCS.wcs.crval[0], 
                                                  self.WCS.wcs.crval[1], 
                                                  angle=self.size/2, 
                                                  magnitude=self.magnitude, 
                                                  otype="'PN'"))
        if data.data:
            data.properties(style)
            data.title = 'Simbad.CDS planetary nebula'           
            self.databaselist.append(data)


    def brightnebula(self, style=dict()):
        """
        Set bright nebula map
        Nb = Bright emission or reflection nebula
            style: {'color': 'green', 
                    'size': 1, 
                    'alpha': 0.2}
        """
        if not style:
            style = {'color': 'green', 
                     'size': 1, 
                     'alpha': 0.2}

        sct = sector.Sector()
        data = markers.brightnebula(sct.simbad(self.WCS.wcs.crval[0], 
                                               self.WCS.wcs.crval[1], 
                                               angle=self.size/2,
                                               magnitude=self.magnitude, 
                                               otype="'ISM','Cld','GNe','RNe','MoC','DNe','glb','CGb','HVC','HII','SFR'"))
        if data.data:
            data.properties(style)
            data.title = 'Simbad.CDS bright nebula'           
            self.databaselist.append(data)

    
    def stars(self):
        """
        Set stars map
        """
        sct = sector.Sector()
        data = markers.stars_simbad(sct.simbad(self.WCS.wcs.crval[0], 
                                               self.WCS.wcs.crval[1], 
                                               angle=self.size/2,
                                               magnitude=self.magnitude, 
                                               otype="*"))
        if data.data:
            data.title = 'Simbad.CDS stars'           
            self.databaselist.append(data)   

    
    def J2000(self,axe):
        """
        Draw label RA (J2000) and DEC (J2000)
        """
        ra = axe.coords['ra']
        dec = axe.coords['dec']
        ra.set_axislabel('RA (J2000)')
        dec.set_axislabel('DEC (J2000)')
        

    def minutes(self, axe, minutes=1):
        """
        Set scalebar minutes degree
            minutes: minutes    
        """
        scalebar_angle = minutes/60 * u.degree
        label = f"{minutes}'"
        add_scalebar(axe, 
                     scalebar_angle, 
                     label=label, 
                     color="black")


    def degree(self, axe, degree=1):
        """
        Set scalebar minutes degree
            minutes: minutes    
        """
        scalebar_angle = degree * u.degree
        label = f"{degree}°"
        add_scalebar(axe, 
                     scalebar_angle, 
                     label=label, 
                     color="black")

    
    def _labelvalue(self, table=dict()):
        """
        Set text
            table: {'ra': right ascention hour, 
                    'dec':declination degre, 
                    'main_id': 'None'}
        """
        ra = []
        dec = []
        angle = []
        main_id = []       
        ra.append(table['ra']*15)
        dec.append(table['dec'])
        angle.append(table['angle'])
        main_id.append(table['main_id']) 
        return ra, dec, angle, main_id

    
    def _labelmarker(self, marker, style):
        """
        Set marker component
        """
        marker.properties(style)
        marker.rotation(style['angle'])
        marker.title = 'label'
        self.databaselist.append(marker)      

    
    def label(self, table=dict(), style=dict()):
        """
        Set text normal style
            table: {'ra': right ascention hour, 
                    'dec': declination degre, 
                    'angle': size angle, 
                    'main_id': 'None'}
            style: {'color': 'black', 
                    'size': 10, 
                    'angle': 0, 
                    'alpha':1}
        """
        if not table:
            table: {'ra': 0, 
                    'dec': 0, 
                    'angle': 0, 
                    'main_id': 'None'}
        if not style:
            style = {'color': 
                     'black', 
                     'size': 10, 
                     'angle': 0, 
                     'alpha': 1}

        ra, dec, angle, main_id = self._labelvalue(table)
        marker = markers.label(Table([ra,dec,angle,main_id], names=['ra', 'dec', 'angle', 'main_id']))
        if marker.data:
            self._labelmarker(marker, style)
            

    def s(self, table=dict(), style=dict()):
        """
        Set text symbole style
            table: {'ra': right ascention hour, 
                    'dec': declination degre, 
                    'angle': size angle,  
                    'main_id': 'None'}
            style: {'color': 'black', 
                    'size': 10, 
                    'angle': 0, 
                    'alpha':1}
        """
        if not table:
            table: {'ra': 0, 
                    'dec': 0, 
                    'angle': 0, 
                    'main_id': 'None'}
        if not style:
            style = {'color': 
                     'black', 
                     'size': 10, 
                     'angle': 0, 
                     'alpha': 1}

        ra, dec, angle, main_id = self._labelvalue(table)
        marker = markers.s(Table([ra,dec,angle,main_id], names=['ra', 'dec', 'angle', 'main_id']))
        if marker.data:
            self._labelmarker(marker, style)

            
    def LABEL(self, table=dict(), style=dict()):
        """
        Set text bold style
            table: {'ra': right ascention hour, 
                    'dec': declination degre, 
                    'angle': size angle, 
                    'main_id': 'None'}
            style: {'color': 'black', 
                    'size': 10, 
                    'angle': 0, 
                    'alpha':1}
        """
        if not table:
            table: {'ra': 0, 
                    'dec': 0, 
                    'angle': 0, 
                    'main_id': 'None'}
        if not style:
            style = {'color': 'black', 
                     'size': 10, 
                     'angle': 0, 
                     'alpha': 1}

        ra, dec, angle, main_id = self._labelvalue(table)
        marker = markers.LABEL(Table([ra,dec,angle,main_id], names=['ra', 'dec', 'angle', 'main_id']))
        if marker.data:
            self._labelmarker(marker, style)      
         
    
    def i(self, table=dict(), style=dict()):
        """
        Set text information style
            table: {'ra': right ascention hour, 
                    'dec': declination degre, 
                    'angle': size angle,  
                    'main_id': 'None'}
            style: {'color': 'black', 
                    'size': 8, 'angle': 0, 
                    'alpha':1}
        """
        if not table:
            table: {'ra': 0, 
                    'dec': 0, 
                    'angle': 0, 
                    'main_id': 'None'}
        if not style:
            style = {'color': 'black', 
                     'size': 8, 
                     'angle': 0, 
                     'alpha': 1}

        ra, dec, angle, main_id = self._labelvalue(table)
        marker = markers.i(Table([ra,dec,angle,main_id], names=['ra', 'dec', 'angle', 'main_id']))
        if marker.data:
            self._labelmarker(marker, style)     

    
    def red(self, table=dict(), style=dict()):
        """
        Set text red box style
            table: {'ra': right ascention hour, 
                    'dec': declination degre, 
                    'angle': size angle, 
                    'main_id': 'None'}
            style: {'color': 
                    'black', 
                    'size': 12, 
                    'angle': 0, 
                    'alpha':1}
        """
        if not table:
            table: {'ra': 0, 
                    'dec': 0, 
                    'angle': 0, 
                    'main_id': 'None'}
        if not style:
            style = {'color': 'black', 
                     'size': 12, 
                     'angle': 0, 
                     'alpha': 1}

        ra, dec, angle, main_id = self._labelvalue(table)
        marker = markers.red(Table([ra,dec,angle,main_id], names=['ra', 'dec', 'angle', 'main_id']))
        if marker.data:
            self._labelmarker(marker, style)     

    
    def blue(self, table=dict(), style=dict()):
        """
        Set text blue circle box style
            table: {'ra': right ascention hour, 
                    'dec': declination degre, 
                    'angle': size angle, 
                    'main_id': 'None'}
            style: {'color': 
                    'black', 
                    'size': 5, 
                    'angle': 0, 
                    'alpha':1}
        """
        if not table:
            table: {'ra': 0, 
                    'dec': 0, 
                    'angle': 30, 
                    'main_id': 'None'}
        if not style:
            style = {'color': 'black', 
                     'size': 12, 
                     'angle': 0, 
                     'alpha': 1}

        ra, dec, angle, main_id = self._labelvalue(table)
        marker = markers.blue(Table([ra,dec,angle,main_id], names=['ra', 'dec', 'angle', 'main_id']))
        if marker.data:
            self._labelmarker(marker, style)     

            
    def date(self, table=dict(), style=dict()):
        """
        Set text red box style
            table: {'ra': right ascention hour, 
                    'dec': declination degre, 
                    'angle': size angle,  
                    'main_id': 'None'}
            style: {'color': 'black', 
                    'size': 10, 
                    'angle': 0, 'alpha':1}
        """
        if not table:
            table: {'ra': 0, 
                    'dec': 0, 
                    'angle': 0, 
                    'main_id': 'None'}
        if not style:
            style = {'color': 'black', 
                     'size': 10, 
                     'angle': 0, 
                     'alpha': 1}

        ra, dec, angle, main_id = self._labelvalue(table)
        marker = markers.date(Table([ra,dec,angle,main_id], names=['ra', 'dec', 'angle', 'main_id']))
        if marker.data:
            self._labelmarker(marker, style)


    def titlemap(self,axe):
        """
        Plot title
        """
        axe.set_title(self.title, fontsize=8)

    
    @property
    def catalogs(self):
        """
        Print databaselist catalog
        """
        values=list()
        for value in self.databaselist:
            if value.catalog not in values:
                values.append(value.catalog)
        return values       

    
    def view(self, catalog='all'):
        """
        List data in catalog
        """
        if catalog == 'all':
            values = self.catalogs
        else:
            values = [catalog,]
        number = 1
        for cat in values: 
            title = f'Table {number}: {cat}'
            print(title)
            for value in self.databaselist:
                if value.catalog in cat:
                    value.view
            print()
            number +=1

        
    def plot(self,axe):
        """
        Plot map
        """
        axe.grid(linestyle = '--', 
                 color = 'black', 
                 alpha = 0.40)
        for database in self.databaselist:
            database.plot(axe)    


        
