"""
Archive class
"""

import os
import matplotlib.pyplot as plt
from astropy.table import Table
from astropy import units as u
from astropy.time import Time
from astropy.io import fits
from astropy.utils.data import get_pkg_data_filename
from ciboulette.base import constant

class Archive(object):
    
    def __init__(self, archive_table = 'dataset/archives'):
        self.directory = archive_table
        self.dataset = []
        self.go = 2017
        self.end = 2021
     
    @property
    def read(self):
        """
        Return table of archive of the fits files in the directory
        Format fits or OBJECT-AAAAMMDD-HHMM-EXPOSTIME-FOCAL.fits
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
        filename = []
        arch = os.listdir(self.directory)   
        for file in arch:
            if '.fit' in file:
                hdu = fits.open(self.directory+'/'+file)[0]
                header = hdu.header   
                
                object_name.append(self.object_name(file))
                 
                if 'OBSERVER' in header:
                    observer.append(header['OBSERVER'])    
                else:
                    observer.append('Nan')    
                    
                if 'INSTRUME' in header:
                    instrument.append(header['INSTRUME']) 
                else:
                    instrument.append('Nan') 
                
                if 'TELESCOP' in header:
                    telescope.append(header['TELESCOP'])
                else:
                    telescope.append('Nan')
                
                if 'FRAMEID' in header:
                    frameid.append(header['FRAMEID'])
                else:
                    frameid.append('Nan')
                
                if 'FRAME' in header:
                    frame.append(header['FRAME'])
                else:
                    frame.append('Nan')
                
                if 'DATATYPE' in header:
                    datatype.append(header['DATATYPE'])
                else:
                    datatype.append('Nan')
                
                if 'FILTERS' in header:
                    filter_name.append(header['FILTERS'])
                else:
                    if 'FILTER' in header:
                        filter_name.append(header['FILTER'])
                    else:
                        filter_name.append('Nan')
                
                if 'FOCALLEN' in header:
                    focal.append(header['FOCALLEN'])
                else:
                    focal.append(self.focal(file))
                
                if 'DATE-OBS' in header:
                    date_obs.append(header['DATE-OBS'])
                else:
                    date_obs.append(self.date(file))   
                                  
                if 'JD-OBS' in header:
                    jd.append(header['JD-OBS'])
                else:          
                    if 'JD' in header:
                        jd.append(header['JD'])
                    else:
                        if 'DATE-OBS' in header:
                            jd.append(self.JulianDay(header['DATE-OBS']))
                        else:
                            jd.append(self.JulianDay(self.date(file)))
                
                if 'x' in file:
                    exptime.append(self.exptime(file))
                else:
                    exptime.append(header['EXPTIME'])
                
                if 'RA' in header:
                    ra.append(header['RA'])
                else:
                    ra.append('Nan')
                    
                if 'DEC' in header:    
                    dec.append(header['DEC']) 
                else:
                    dec.append('Nan') 
                    
                filename.append(file.replace('.fits',''))
             
        self.dataset = Table([object_name,observer,instrument,telescope,frameid,frame,datatype,filter_name,focal,exptime,date_obs,jd,ra,dec,filename], 
                             names=['ID','OBSERVER','INSTRUME','TELESCOP','FRAMEID','FRAME','DATATYPE','FILTER','FOCALLEN','EXPTIME','DATE-OBS','JD','RA','DEC','FILE'])

    def observations(self):
        """
        Return header of list files
        """
        return self.dataset
    
    def JulianDay(self,string):
        """
        Return JD od DATE
        """
        time = Time(string)
        return time.jd
    
    def object_name(self,string):
        """
        Return object name of first word of filename
        """    
        return string.split('-')[0]
    
    def focal(self,string):
        """
        Return focal of last word of filename
        """   
        return string.replace('.fits','').split('-')[4].replace('f','')

    def date(self,string):
        """
        Return date end time of word of filename
        """  
        d = string.replace('.fits','').split('-')[1]
        t = string.replace('.fits','').split('-')[2]
        d = d[:4] + '-' + d[4:6] + '-' + d[6:8] + 'T' + t[:2] + ':' + t[2:4] + ':00'
        return d                  
 
    def exptime(self,string):      
        """
        Return exposition time of word of filename
        """  
        exp = string.replace('.fits','').split('-')[3].replace('s','')
        number = float(exp.split('x')[0])
        time = float(exp.split('x')[1])
        e = number * time
        return e             
        
    def header(self,filename):
        """
        Return header of file with index line
        """
        hdu = fits.open(self.directory+'/'+filename+'.fits')[0]
        return hdu.header 
    
    @property
    def period(self):
        """
        Return period of base
        """
        return max(self.dataset['JD'])-min(self.dataset['JD'])
    
    @property
    def exptimes(self):
        """
        Return period of base
        """
        return sum(self.dataset['EXPTIME'])

    def find(self,string):
        """
        Return the object found
        """
        mask = self.dataset['ID'] == string
        r = self.dataset[mask]
        return r
        
    def plot(self):
        """
        Plot JD planning
        """
        summer = []
        years_data = []
        for years in range(self.go,self.end+1):
            date = str(years) + '-01-01T00:00:00'
            years_data.append(self.JulianDay(date))
            period_plot = _summer(year = years)
            summer.append(period_plot)
            
        plt.ylim(0,1)
        plt.xlim(min(years_data),max(years_data))
        for database_period in summer:
            database_period.plot()   
        plt.vlines(years_data, 0,1 , colors = 'red', alpha = 0.2, lw=15)
        plt.vlines(self.dataset['JD'], 0,1 , colors = 'black', alpha = 0.3)
        plt.xlabel(constant.JD_label)
        plt.show()

class _summer(object):
    
    def __init__(self, year = 2021):
        date = str(year) + constant.summer[0]
        time = Time(date)
        self.go = time.jd
        date = str(year) + constant.summer[1]
        time = Time(date)
        self.end = time.jd
        self.y = [0,1]
        self.color = 'blue'
        self.alpha = 0.1
    
    def plot(self):
        plt.fill_betweenx(self.y,self.go,self.end, color=self.color, alpha=self.alpha)
