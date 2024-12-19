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
import matplotlib.patches as patches
import matplotlib.patheffects as patheffects
# Astropy mods
from astropy.table import Table
from astropy import wcs
from astropy import units as u
from astropy.visualization.wcsaxes import SphericalCircle, Quadrangle, add_scalebar
from astropy.coordinates import SkyCoord



class component():
    
        def __init__(self,table):
            self.data = table
            self.title = 'Cursor'
            self.size = 2.0
            self.color = 'blue'
            self.alpha = 0.8
         
        def properties(self,style=dict()):
            """
            set properties
            """
            self.size = style['size']
            self.color = style['color']
            self.alpha = style['alpha']
       
        @property
        def get(self):
            """
            Return title and table data
            """
            return {'title': self.title, 'data': self.data}

        @property
        def catalog(self):
            """
            Return title
            """
            return self.title


class marker(component):

        def plot(self, axe):
            """
            Plot database
            """
            ra = self.data['ra']
            dec = self.data['dec']
            angle = self.data['angle']/120
            c = SphericalCircle((ra * u.degree, dec * u.degree), 
                                angle * u.degree, 
                                edgecolor='black', 
                                ls='dotted', 
                                linewidth=self.size, 
                                facecolor=self.color, 
                                alpha=self.alpha, 
                                transform=axe.get_transform('icrs')
                               )
            axe.add_patch(c)

class constellations(component):

        def plot(self,axe):
            """
            Plot database
            """
            axe.scatter(self.data['ra'], 
                        self.data['dec'], 
                        transform=axe.get_transform('icrs'), s=2, 
                        edgecolor=self.color, 
                        facecolor=self.color, 
                        alpha=self.alpha)



class cursor(component):

        def plot(self,axe):
            """
            Plot database
            """
            ra = self.data['ra']
            dec = self.data['dec']
            angle = self.data['angle']/120
            c = SphericalCircle((ra * u.degree, dec * u.degree), 
                                angle * u.degree, 
                                edgecolor='red', 
                                linewidth=self.size, 
                                facecolor='none', 
                                alpha=self.alpha, 
                                transform=axe.get_transform('icrs')
                               )
            axe.add_patch(c)
           

class stars(component):

        def plot(self, axe):
            """
            Plot database
            """
            axe.scatter(self.data['RA'], 
                        self.data['DEC'], 
                        transform=axe.get_transform('icrs'), 
                        s=self.data['MARKER'],
                        edgecolor=self.color, 
                        facecolor=self.color, 
                        alpha=self.alpha)


class opencluster(component):

        def plot(self, axe):
            """
            Plot database
            """
            for value in self.data:
                masked = str(value['GALDIM_MAJAXIS'])
                if '-' in masked :
                    size = (1 / 120) * u.degree
                else:
                    size = (value['GALDIM_MAJAXIS'] / 120) * u.degree
                coords = SkyCoord(ra=value['RA'], 
                                  dec=value['DEC'], 
                                  unit=(u.h, u.deg), frame='icrs')
                ra = coords.ra.value
                dec = coords.dec.value
                c = SphericalCircle((ra * u.degree, dec * u.degree), 
                                    size, 
                                    edgecolor='black', ls='dotted',
                                    linewidth=self.size, 
                                    facecolor=self.color, 
                                    alpha=self.alpha, 
                                    transform=axe.get_transform('icrs')
                                   )
                axe.add_patch(c)
                

class globularcluster(component):

        def plot(self, axe):
            """
            Plot database
            """
            for value in self.data:
                masked = str(value['GALDIM_MAJAXIS'])
                if '-' in masked :
                    size = (1 / 120) * u.degree
                else:
                    size = (value['GALDIM_MAJAXIS'] / 120) * u.degree
                coords = SkyCoord(ra=value['RA'], 
                                  dec=value['DEC'], 
                                  unit=(u.h, u.deg), 
                                  frame='icrs')
                ra = coords.ra.value
                dec = coords.dec.value
                c = SphericalCircle((ra * u.degree, dec * u.degree), 
                                    size, 
                                    edgecolor='black', ls='-',
                                    linewidth=self.size, 
                                    facecolor=self.color, 
                                    alpha=self.alpha, 
                                    transform=axe.get_transform('icrs')
                                   )
                axe.add_patch(c)
 
            
class galaxy(component):

        def plot(self, axe):
            """
            Plot database
            """
            for value in self.data:
                masked = str(value['GALDIM_MAJAXIS'])
                if '-' in masked :
                    size = (1 / 120) * u.degree
                else:
                    size = (value['GALDIM_MAJAXIS'] / 120) * u.degree
                coords = SkyCoord(ra=value['RA'], 
                                  dec=value['DEC'], 
                                  unit=(u.h, u.deg), 
                                  frame='icrs')
                ra = coords.ra.value
                dec = coords.dec.value
                c = SphericalCircle((ra * u.degree, dec * u.degree), 
                                    size, edgecolor='black', 
                                    linewidth=self.size, 
                                    facecolor=self.color, 
                                    alpha=self.alpha,
                                    transform=axe.get_transform('icrs')
                                   )
                axe.add_patch(c)


class planetarynebula(component):

        def plot(self, axe):
            """
            Plot database
            """
            for value in self.data:
                masked = str(value['GALDIM_MAJAXIS'])
                if '-' in masked :
                    size = (1 / 120) * u.degree
                else:
                    size = (value['GALDIM_MAJAXIS'] / 120) * u.degree
                coords = SkyCoord(ra=value['RA'], 
                                  dec=value['DEC'], 
                                  unit=(u.h, u.deg), 
                                  frame='icrs')
                ra = coords.ra.value
                dec = coords.dec.value
                c = SphericalCircle((ra * u.degree, dec * u.degree), 
                                    size, 
                                    edgecolor='black', 
                                    ls='dotted',
                                    linewidth=self.size, 
                                    facecolor=self.color, 
                                    alpha=self.alpha, 
                                    transform=axe.get_transform('icrs')
                                   )
                axe.add_patch(c)
            

class brightnebula(component):

        def plot(self, axe):
            """
            Plot database
            """
            for value in self.data:
                masked = str(value['GALDIM_MAJAXIS'])
                if '-' in masked :
                    size = (9 / 120) * u.degree
                else:
                    size = (value['GALDIM_MAJAXIS'] / 120) * u.degree
                coords = SkyCoord(ra=value['RA'], 
                                  dec=value['DEC'], 
                                  unit=(u.h, u.deg), 
                                  frame='icrs')
                ra = coords.ra.value
                dec = coords.dec.value
                r = Quadrangle((ra * u.degree, dec * u.degree), 
                               size, 
                               size, 
                               edgecolor='black', 
                               ls='dotted',
                               linewidth=self.size, 
                               facecolor=self.color, 
                               alpha=self.alpha,
                               transform=axe.get_transform('icrs')
                              )             
                axe.add_patch(r)


class label(component):

        def rotation(self, angle=0):
            """
            set angle
            """   
            self.angle = angle
           
        def plot(self,axe):
            """
            Plot database
            """
            fontstyle = 'normal'
            if self.data['angle'].value[0] == 1:
                fontstyle = 'italic'             
            label = str(self.data['main_id'].value[0]) 
            ra = self.data['ra'].value[0]
            dec = self.data['dec'].value[0]           
            text = plt.text(ra, dec, 
                            s=label, 
                            color='black', 
                            ha='center', 
                            va='center', 
                            alpha=self.alpha, 
                            size=self.size, 
                            fontstyle=fontstyle,
                            rotation=self.angle, 
                            transform=axe.get_transform('icrs'))
            text.set_path_effects([patheffects.Stroke(linewidth=3, 
                                                      foreground='white'), 
                                   patheffects.Normal()])
          
            
class LABEL(component):

        def rotation(self, angle=0):
            """
            set angle
            """   
            self.angle = angle
           
        def plot(self,axe):
            """
            Plot database
            """
            fontstyle = 'normal' 
            if self.data['angle'].value[0] == 1:
                fontstyle = 'italic'              
            label = str(self.data['main_id'].value[0]) 
            ra = self.data['ra'].value[0]
            dec = self.data['dec'].value[0]           
            text = plt.text(ra, dec, 
                            s=label, 
                            color='black', 
                            ha='center', 
                            va='center', 
                            alpha=self.alpha, 
                            size=self.size,
                            fontstyle=fontstyle,
                            fontweight='bold', 
                            rotation=self.angle, 
                            transform=axe.get_transform('icrs'))
            text.set_path_effects([patheffects.Stroke(linewidth=3, 
                                                      foreground='white'), 
                                   patheffects.Normal()])


class i(component):

        def rotation(self, angle=0):
            """
            set angle
            """   
            self.angle = angle
           
        def plot(self,axe):
            """
            Plot database
            """
            label = str(self.data['main_id'].value[0]) 
            ra = self.data['ra'].value[0]
            dec = self.data['dec'].value[0]           
            box=dict(boxstyle="round", 
                     fc=(0.5, 0.5, 1.), 
                     ec=(0.8, 0.8, 1.), 
                     alpha=0.3
                    )          
            text = plt.text(ra, dec, s=label, 
                            color='blue', 
                            ha='center', 
                            va='center', 
                            alpha=self.alpha, 
                            size=self.size,
                            fontstyle='italic',
                            bbox=box, 
                            rotation=self.angle, 
                            transform=axe.get_transform('icrs')
                            )
            text.set_path_effects([patheffects.Stroke(linewidth=2, 
                                                      foreground='white'), 
                                   patheffects.Normal()])


class s(component):

        def rotation(self, angle=0):
            """
            set angle
            """   
            self.angle = angle
           
        def plot(self,axe):
            """
            Plot database
            """
            fontstyle = 'normal'
            if self.data['angle'].value[0] == 1:
                fontstyle = 'italic'             
            label = "$\\" + self.data['main_id'].value[0] + "$"
            ra = self.data['ra'].value[0]
            dec = self.data['dec'].value[0]           
            text = plt.text(ra, dec, 
                            s=label, 
                            color='black', 
                            ha='center', 
                            va='center', 
                            alpha=self.alpha, 
                            size=self.size, 
                            fontstyle=fontstyle,
                            rotation=self.angle, 
                            transform=axe.get_transform('icrs'))
            text.set_path_effects([patheffects.Stroke(linewidth=3, 
                                                      foreground='white'), 
                                   patheffects.Normal()])

    
class red(component):

        def rotation(self, angle=0):
            """
            set angle
            """   
            self.angle = angle
           
        def plot(self,axe):
            """
            Plot database
            """
            label = str(self.data['main_id'].value[0]) 
            ra = self.data['ra'].value[0]
            dec = self.data['dec'].value[0]
            box=dict(boxstyle="circle",
                   ec=(1., 0.5, 0.5),
                   fc=(1., 0.8, 0.8),
                   alpha=0.6
                   )           
            text = plt.text(ra, dec, s=label, 
                            color='white', 
                            ha='center', 
                            va='center', 
                            alpha=self.alpha, 
                            size=self.size, 
                            fontstyle='italic' , 
                            bbox=box, 
                            rotation=self.angle, 
                            transform=axe.get_transform('icrs')
                           )
            text.set_path_effects([patheffects.Stroke(linewidth=2, 
                                                      foreground='red'), 
                                   patheffects.Normal()])


class blue(component):
    
        def rotation(self, angle=0):
            """
            set angle
            """   
            self.angle = angle
           
        def plot(self,axe):
            """
            Plot database
            """
            label = str(self.data['main_id'].value[0]) 
            ra = self.data['ra'].value[0]
            dec = self.data['dec'].value[0]
            size = (self.data['angle'] / 120)          
            c = SphericalCircle((ra * u.degree, dec * u.degree), 
                                size * u.degree, 
                                edgecolor='blue', 
                                ls='-',
                                linewidth=2, 
                                facecolor='none', 
                                alpha=self.alpha, 
                                transform=axe.get_transform('icrs')
                                )
            axe.add_patch(c)
            box=dict(boxstyle="round",
                   ec='white',
                   fc='white',
                   )           
            text = plt.text(ra, dec + size, s=label, 
                            color='blue', 
                            ha='center', 
                            va='center', 
                            alpha=self.alpha, 
                            size=self.size, 
                            bbox=box,
                            rotation=self.angle, 
                            transform=axe.get_transform('icrs')
                           )
            text.set_path_effects([patheffects.Stroke(linewidth=4, 
                                                      foreground='white'), 
                                   patheffects.Normal()])   


class date(component):

        def rotation(self, angle=0):
            """
            set angle
            """   
            self.angle = angle
           
        def plot(self,axe):
            """
            Plot database
            """
            label = str(self.data['main_id'].value[0]) 
            ra = self.data['ra'].value[0]
            dec = self.data['dec'].value[0]
            box=dict(boxstyle="round", 
                     fc=(0.3, 0.3, 0.3), 
                     ec=(0.3, 0.3, 0.3), 
                     alpha=0.15
                    )          
            text = plt.text(ra, dec, s=label, 
                            color='black', 
                            ha='center', 
                            va='center', 
                            alpha=self.alpha, 
                            size=self.size, 
                            bbox=box, 
                            rotation=self.angle, 
                            transform=axe.get_transform('icrs')
                            )
            text.set_path_effects([patheffects.Stroke(linewidth=2, 
                                                      foreground='white'), 
                                   patheffects.Normal()])























