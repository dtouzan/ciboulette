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
        self.comment = ''
        self.observation = Table()
        self.html = BeautifulSoup()
        self.available = False
        self._period = 0
        if self.filter not in ['vis','ccd']:
            self.filter = 'vis'
        self.read 

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
        else:
            nameID = self.nameID
        url = 'https://app.aavso.org/webobs/results/?star=' + nameID + '&num_results=200' + '&obs_types=' + self.filter
        filedownload = wget.download(url,out=self.fileoutput,bar=None)  
        with open(filedownload) as fp:
            self.html = BeautifulSoup(fp, 'html.parser')

        if self.noerror == 0 :
            self.available = True
            self.title
            self.comments
            self.table
        else:
            self.available = False

    @property
    def title(self):
        self.titlename = self.html.title.contents[0] + ' -- ' + self.nameID
        return self.titlename
       
    @property
    def comments(self):
        if self.available:
            comment = self.html.find(id='obsinfo').contents[0].string
            comment = comment + self.html.find(id='obsinfo').contents[1].string
            comment = comment + self.html.find(id='obsinfo').contents[2].string.replace('\n  \n','').replace('\n','').replace('  ',' ')
            comment = comment + self.html.find(id='obsinfo').contents[3].string
            comment = comment + self.html.find(id='obsinfo').contents[4].string.replace('\n  \n  \n  \n ','')
            comment = comment + self.html.find(id='obsinfo').contents[5].string
            comment = comment + self.html.find(id='obsinfo').contents[6].string.replace('\n  \n  \n  \n  \n  ','')
            self.comment = comment
        return self.comment
            
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
        if self.available:
            jd_min,jd_max = self.JDMinMax
            mv_min,mv_max = self.magnitudeMinMax

            xlabel = []
            for i in range(int(jd_min),int(jd_max)+1):
                line = str(i)
                xlabel.append(line[-2:])
        
            x = []
            for value in self.observations:
                x.append(value['JD']-jd_min)
            y = self.observations['Magnitude']        

            mymodel = np.poly1d(np.polyfit(x, y, 3))
            myline = np.linspace(0, jd_max-jd_min, 100)

            plt.xlim(-.5,round(jd_max-jd_min)+.5)
            plt.ylim(round(mv_min)-0.5,round(mv_max)+0.5)
            plt.gca().invert_yaxis()
            plt.scatter(x, y, c = 'black', s = 5, alpha = 0.5)
            plt.plot(myline, mymodel(myline))
            plt.gca().xaxis.set_ticks(range( (round(jd_max)-round(jd_min))))
            plt.gca().set_xticklabels(xlabel)
            plt.title(self.title, loc='center')
            plt.xlabel(str(int(jd_min))+'   JD', fontsize = 12)
            if self.filter == 'vis':
                plt.ylabel(r'$m_v$', fontsize = 12)
            else:
                plt.ylabel('Magnitude', fontsize = 12)
            plt.show()
        else:
            print(self.comment)
        
    @property
    def noerror(self):
        """
        Error handling
        """
        error_code = 0       
        if 'errors' in self.html.p.get_text():
                error_code = 404
                self.comment = 'The star ' + self.nameID + ' cannot be found in our database.' 
        else:
            if 'no results' in self.html.p.get_text():
                error_code = 404
                self.comment = 'The star ' + self.nameID + ' cannot be found in our database.' 
        return error_code