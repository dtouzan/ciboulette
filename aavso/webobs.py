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
    
    def __init__(self, nameID='', filtername='vis', fileoutput='aavso.html'):  
        self.nameID = nameID
        self.filter = filtername
        self.fileoutput = fileoutput
        self.titlename = ''
        self.header = Table()
        self.observation = Table()
        self.html = BeautifulSoup()
        self.available = False
        self._period = 0
        self.read   

    @property
    def read(self):
        """
        Return table of observation
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
            data = self.html.table.contents[3].get_text().replace('\n',',').replace('Details...,,,,,,,,,Comp Star,Check Star,Transformed,Chart,Comment Codes,Notes,,,,,','').replace(',,,,,,,,,',';').replace(',,,,,,,','').replace(',,,','').replace(',             (','(').replace(',            ','').replace(', ','-').split(';')
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
                data = ligne.split(',')
                Star.append(data[0])
                JD.append(data[1])
                Calendar_Date.append(data[2])
                Magnitude.append(data[3])
                Error.append(data[4])
                Filter.append(data[5])
                Observer.append(data[6])
                Comp_Star.append(data[7])
                Check_Star.append(data[8])
                Transformed.append(data[9]) 
                Chart.append(data[10]) 
                Comment_Codes.append(data[11])
                Notes.append(data[12])

        table = Table([Star,JD,Calendar_Date,Magnitude,Error,Filter,Observer,Comp_Star,Check_Star,Transformed,Chart,Comment_Codes,Notes],
                      names=['Star', 'JD', 'Calendar Date', 'Magnitude', 'Error', 'Filter', 'Observer', 'Comp Star', 'Check Star', 'Transformed', 'Chart', 'Comment Codes', 'Notes'])
        
        self._period = float(table['JD'][0]) - float(table['JD'][len(table)-1])
        return table
    
    @property
    def period(self):
        """
        Return period JD
        """
        if self.available:
            return self._period