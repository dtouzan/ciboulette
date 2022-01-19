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
        self.select = '*'
        self.go = 2010
        self.end = 2030
     
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
                if self.select in self.object_name(file) or self.select == '*':
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
        number = 1
        if 'x' in exp:
            number = float(exp.split('x')[0])
            time = float(exp.split('x')[1])
        else:
            time = float(exp)
        e = number * time
        return e             
        
    def header(self,filename):
        """
        Return header of file with index line
        """
        hdu = fits.open(self.directory+'/'+filename+'.fits')[0]
        return hdu.header 
    
    @property
    def maxJD(self):
        """
        Return max Julian Day
        """
        return max(self.dataset['JD'])
    
    @property
    def minJD(self):
        """
        Return min Julian Day
        """ 
        return min(self.dataset['JD'])
    
    @property
    def period(self):
        """
        Return period of base
        """
        return self.maxJD-self.minJD
    
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

    @property
    def start(self):
        """
        Return go value
        """
        return self.go
    
    @start.setter
    def start(self,start_value):
        """
        Set go value
        """
        if start_value < 2000:
            start_value = 2000
        if start_value > 2999:
            start_value = 2999
        if start_value > self.end:
            start_value = self.end - 1
        self.go = start_value
    
    @property
    def stop(self):
        """
        Return end value
        """
        return self.end

    @stop.setter
    def stop(self,end_value):
        """
        Set end value
        """
        if end_value < 2000:
            end_value = 2000
        if end_value > 2999:
            end_value = 2999
        if end_value < self.go:
            end_value = self.go + 1
        self.end = end_value  

    def plot(self):
        """
        Plot JD planning
        """
        summer = []
        new_year = []
        years_data = []
        if self.go >= self.end:
            self.go = self.end - 1
        for years in range(self.go,self.end+1):
            date = str(years) + '-01-01T00:00:00'
            years_data.append(self.JulianDay(date))           
        for years in range(self.go,self.end):
            period = _summer(year = years)
            summer.append(period)
            period = _year(year = years)
            new_year.append(period)
    
        plt.ylim(0,1)
        plt.xlim(min(years_data),max(years_data))
        for database_period in summer:
            database_period.plot()   
        for database_period in new_year:
            database_period.plot()
        plt.vlines(self.dataset['JD'], 0,1 , colors = 'black', alpha = 0.3)
        plt.yticks([])
        plt.xlabel(constant.JD_label)
        plt.show()

class _summer(object):
    """
    Plot summer class
    """
    
    def __init__(self, year = 2021):
        date = str(year) + constant.summer[0]
        time = Time(date)
        self.go = time.jd
        date = str(year) + constant.summer[1]
        time = Time(date)
        self.end = time.jd
        self.y = [0,1]
        self.color = 'blue'
        self.alpha = 0.25
    
    def plot(self):
        plt.fill_betweenx(self.y,self.go,self.end, color=self.color, alpha=self.alpha)
        plt.text(self.go+int((self.end-self.go)/2),0.5,'SUMMER', horizontalalignment='center', verticalalignment='center', fontsize=12, color='w', fontweight='bold')

class _year(object):
    """
    Plot year class
    """
    
    def __init__(self, year = 2021):
        date = str(year) + '-01-01T00:00:00'
        time = Time(date)
        self.go = time.jd
        date = str(year) + '-01-31T00:00:00'
        time = Time(date)
        self.end = time.jd     
        self.label = str(year)
        self.y = [0,1]
        self.color = 'red'
        self.alpha = 0.25
    
    def plot(self):
        plt.fill_betweenx(self.y,self.go,self.end, color=self.color, alpha=self.alpha)
        plt.text(self.go+int((self.end-self.go)/2),0.5,self.label, rotation='vertical', horizontalalignment='center', verticalalignment='center', fontsize=12, color='w', fontweight='bold')
        plt.vlines(self.go, 0,1 , colors = 'red', linewidths=3, alpha = 0.5)