"""
WebObs class
"""

from astropy.table import Table
from astropy import units as u
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import os
import wget


class WebObs(object):
    """
    Class for AAVSO web observation.
    fileoutput = aavso.html
    filtername = vis|ccd
    """
    
    def __init__(self, nameID, filtername='vis', fileoutput='aavso.html'):  
        self.nameID = nameID
        self.filter = filtername
        self.fileoutput = fileoutput
        self.titlename = ''
        self.observation = Table()
        self.html = BeautifulSoup()
        self.available = False
        self._period = 0
        if self.filter not in ['vis','ccd']:
            self.filter = 'vis'
        self.read 
        self.table

    @property
    def read(self):
        """
        Return html of observation
        Ex:  wget --no-check-certificate 'https://app.aavso.org/webobs/results/?star=' -O aavso.html    
        """
        if os.path.exists(self.fileoutput) :
            os.remove(self.fileoutput)
        
        if ' ' in self.nameID:
            nameID = self.nameID.replace(' ','%20')
        url = 'https://app.aavso.org/webobs/results/?star=' + nameID + '&num_results=200' + '&obs_types=' + self.filter
        filedownload = wget.download(url,out=self.fileoutput,bar=None)  
        with open(filedownload) as fp:
            self.html = BeautifulSoup(fp, 'html.parser')

        if len(self.html) > 0:
            self.available = True
            self.titlename = self.html.title.contents[0] + ' -- ' + self.nameID
        else:
            self.available = False

    @property
    def title(self):
        return self.titlename
            
    @property
    def data(self):
        """
        Return data of html file observations
        """
        data = []
        if self.available:
            data = self.html.table.contents[3].get_text().replace('\n','|').replace('Details...|||||||||Comp Star|Check Star|Transformed|Chart|Comment Codes|Notes|||||','').replace('|||||||||','<>').replace('|||||||','').replace('|||','').replace('|             (','(').replace('|            ','').split('<>')
        return data

    @property
    def table(self):
        """
        Return Table of html file observations
        """
        Star = []
        JD = []
        Calendar_Date = []
        Magnitude = []
        Error = []
        Filter = []
        Observer = []
        Comp_Star = []
        Check_Star = []
        Transformed = []
        Chart = []
        Comment_Codes = []
        Notes = []
                
        if self.available:
            for ligne in self.data:
                data = ligne.split('|')
                Star.append(data[0])
                JD.append(float(data[1]))
                Calendar_Date.append(data[2])
                if isinstance(data[3], int) or isinstance(data[3], float):
                    Magnitude.append(float(data[3]))
                else:
                    Magnitude.append(float(data[3].replace('<','')))
                Error.append(data[4])
                Filter.append(data[5])
                Observer.append(data[6])
                Comp_Star.append(data[7])
                Check_Star.append(data[8])
                Transformed.append(data[9]) 
                Chart.append(data[10]) 
                Comment_Codes.append(data[11])
                Notes.append(data[12])

        self.observation = Table([Star,JD,Calendar_Date,Magnitude,Error,Filter,Observer,Comp_Star,Check_Star,Transformed,Chart,Comment_Codes,Notes],
                      names=['Star', 'JD', 'Calendar Date', 'Magnitude', 'Error', 'Filter', 'Observer', 'Comp Star', 'Check Star', 'Transformed', 'Chart', 'Comment Codes', 'Notes'])
        
        self._period = self.observation['JD'][0] - self.observation['JD'][len(self.observation)-1]
        return self.observation
    
    @property
    def period(self):
        """
        Return period JD
        """
        if self.observation:
            return self._period

    @property
    def observations(self):
        """
        Return observations table
        """
        if self.observation:
            return self.observation

    @property
    def JDMinMax(self):
        """
        Return min and max JD in observations table
        """
        if self.observation:
            return self.observation['JD'][len(self.observation)-1],self.observation['JD'][0]

    @property
    def magnitudeMinMax(self):
        """
        Return min and max of magnitude in observations table
        """
        if self.observation:
            return min(self.observation['Magnitude']),max(self.observation['Magnitude'])
    
    def plot(self):
        """
        Plot observations table
        """
        jd_min,jd_max = self.JDMinMax
        mv_min,mv_max = self.magnitudeMinMax
        plt.xlim(round(jd_min)-0.5,round(jd_max)+0.5)
        plt.ylim(round(mv_min)-0.5,round(mv_max)+0.5)
        plt.gca().invert_yaxis()
        plt.scatter(self.observations['JD'], self.observations['Magnitude'], c = 'black', s = 5, alpha = 0.5)
        plt.title(self.title, loc='center')
        plt.xlabel(r'$JD$', fontsize = 14)
        if self.filter == 'vis':
            plt.ylabel(r'$m_v$', fontsize = 14)
        else:
            plt.ylabel('Magnitude', fontsize = 14)
        plt.show()