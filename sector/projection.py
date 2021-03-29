"""
Projection class
"""

from astropy.time import Time
from astropy.table import Table
from astropy.coordinates import SkyCoord, Angle
from astropy import units as u
from astropy import wcs
import matplotlib.pyplot as plt
from ciboulette.sector import sector as Sct

class Projection(object):
        
    def __init__(self):
            self.data = []
            
    def projections(self,RA,DEC,archives,latitude,longitude,elevation):
        """
        Displays the archived sectors, RA and DEC on an aitoff projection
        """
        sct = Sct.Sector()      
        sector_arch = sct.readarchives(archives)
        # Read archive table
        value_quadran_ra = []
        value_quadran_dec = []   
        for line in sector_arch:        
            c = SkyCoord(ra = line['RA'], dec = line['DEC'], unit = (u.deg, u.deg), frame='icrs')
            value_quadran_ra.append(-c.ra.wrap_at(180 * u.deg).radian)
            value_quadran_dec.append(c.dec.radian)
         
        milkyway = sct.MilkyWay
        milkyway_ra = []
        milkyway_dec = []
        for line in milkyway:
            c = SkyCoord(ra = line['RA'], dec = line['DEC'], unit = (u.deg, u.deg), frame='icrs')
            milkyway_ra.append(-c.ra.wrap_at(180 * u.deg).radian)
            milkyway_dec.append(c.dec.radian)
 
        lmc = sct.lmc
        lmc_ra = []
        lmc_dec = []
        for line in lmc:
            c = SkyCoord(ra = line['RA'], dec = line['DEC'], unit = (u.deg, u.deg), frame='icrs')
            lmc_ra.append(-c.ra.wrap_at(180 * u.deg).radian)
            lmc_dec.append(c.dec.radian)
 
        smc = sct.smc
        smc_ra = []
        smc_dec = []
        for line in smc:
            c = SkyCoord(ra = line['RA'], dec = line['DEC'], unit = (u.deg, u.deg), frame='icrs')
            smc_ra.append(-c.ra.wrap_at(180 * u.deg).radian)
            smc_dec.append(c.dec.radian) 
            
        opc = sct.opencluster16
        opc_ra = []
        opc_dec = []
        for line in opc:
            c = SkyCoord(ra = line['RA'], dec = line['DEC'], unit = (u.deg, u.deg), frame='icrs')
            ra = c.ra*15
            opc_ra.append(-ra.wrap_at(180 * u.deg).radian)
            opc_dec.append(c.dec.radian)
        
        location = str(longitude) + ' ' + str(latitude) + ' ' + str(elevation)
        moon = sct.miriademoon(location)
        moon_ra = []
        moon_dec = []
        for line in moon:
            c = SkyCoord(ra = line['RA'], dec = line['DEC'], unit = (u.deg, u.deg), frame='icrs')
            moon_ra.append(-c.ra.wrap_at(180 * u.deg).radian)
            moon_dec.append(c.dec.radian)
            moon_v = line['MARKER']
                            
        title =''    
        # RA and DEC in degrees
        ra=float(RA)*15*u.deg
        dec=float(DEC)*u.deg
        # ICRS configuration
        c = SkyCoord(ra, dec, frame='icrs', unit=(u.deg, u.deg))
        # RA and DEC in radian
        value_ra = -c.ra.wrap_at(180 * u.deg).radian
        value_dec= c.dec.radian
        title = 'Open cluster less than 16 Mv\n'
        # Display configuration
        fig = plt.figure(figsize=(15,15))
        # Configuration de la projecion cartographique du titre et grille 
        ax = fig.add_subplot(111,projection='aitoff')
        plt.grid(True,axis='both',linestyle='--')
        # Projection drawing
        plt.plot(milkyway_ra, milkyway_dec, color='blue', lw=1, alpha=0.2)
        plt.fill_between(milkyway_ra,milkyway_dec, color='blue', alpha=0.1)  
        
        plt.plot(smc_ra, smc_dec, color='blue', lw=1, alpha=0.2)
        plt.fill_between(smc_ra,smc_dec, color='blue', alpha=0.1)        

        plt.plot(lmc_ra, lmc_dec, color='blue', lw=1, alpha=0.2)
        plt.fill_between(lmc_ra,lmc_dec, color='blue', alpha=0.1)        

        plt.plot(opc_ra, opc_dec, 'o', color='blue', markersize=2, alpha=0.25)
        
        plt.plot(moon_ra, moon_dec, 'o', color='black', markersize=moon_v, alpha=0.15)
        
        if len(sector_arch) > 0:
            plt.plot(value_quadran_ra, value_quadran_dec, 's', color='green', markersize=5, alpha=0.2)   
        plt.plot(value_ra, value_dec, 's', color='red', markersize=5, alpha=0.4)
        # Modification of labels in hours
        ax.set_xticklabels(['10h','08h','06h','04h','02h','0h','22h','20h','18h','16h','14h'],alpha=0.4)
        ax.set_title(title, fontsize = 12)
        # Display
        plt.show()