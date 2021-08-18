"""
WebObs class
"""

from astropy.table import Table
from astropy import units as u
from astropy.coordinates import SkyCoord
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import os
import io
import wget
import requests


class WebObs(object):
    """
    Class for AAVSO web observation.
    fileoutput = aavso.html
    filtername = vis|ccd
    """
    
    def __init__(self, nameID, filtername='Vis', fileoutput='aavso.html'):  
        self.nameID = nameID
        self.filter = filtername
        self.fileoutput = fileoutput
        self.titlename = ''
        self.comment = ''
        self.observation = Table()
        self.html = BeautifulSoup()
        self.available = False
        self._period = 0
        self.filter = self.isfilter(filtername)
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
        if self.isccd:
            filtername = 'ccd'
        else:
            filtername = 'vis'
        
        url = 'https://app.aavso.org/webobs/results/?star=' + nameID + '&num_results=200' + '&obs_types=' + filtername
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
    
    def isfilter(self,filtername='vis'):
        """
        Return filter
        """
        if filtername in  ['Vis','I','R','B','V']:
            f = filtername
        else:
            f = 'Vis'            
        return f
    
    @property
    def isccd(self):
        """
        Return true if in ccd filter
        """
        if self.filter in ['I','R','B','V']:
            return True
        else:
            return False       
            
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
                if self.filter in data[5]:
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
        
        if len(Star) > 0:
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
        
            x = []
            for value in self.observations:
                x.append(value['JD']-jd_min)
            y = self.observations['Magnitude']        

            mymodel = np.poly1d(np.polyfit(x, y, 7))
            myline = np.linspace(0, jd_max-jd_min, 2000)
            
            plt.xlim(-.5,round(jd_max-jd_min)+.5)
            plt.ylim(round(mv_min)-0.5,round(mv_max)+0.5)
            plt.gca().invert_yaxis()
            plt.scatter(x, y, c = 'black', s = 2, alpha = 0.5)
            plt.plot(myline, mymodel(myline))
            plt.title(self.title, loc='center')
            plt.xlabel(str(int(jd_min))+'\nJD', fontsize = 12)
            if self.filter == 'Vis':
                plt.ylabel(r'$m_v$', fontsize = 12)
            else:
                plt.ylabel(self.filter, fontsize = 12)
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
    
class datadownload(object):
    """
    Class for AAVSO for data download (https://www.aavso.org/data-download).
    fileinput = datadownload.csv
    filtername = Vis|B|V|R|I|TG|CV
    """
    
    def __init__(self, filtername='Vis.', fileinput='aavsodata.csv'):  
        self.nameID = ''
        self.filter = filtername
        self.fileinput = fileinput
        self.titlename = ''
        self.comment = ''
        self.observation = Table()
        self.JDline = _JDline()
        self.available = False
        self._period = 0
        self.filter = self.isfilter(filtername)
        self.read 

    def isfilter(self,filtername='Vis.'):
        """
        Return filter
        """
        if filtername in  ['Vis.','I','R','B','V','CV','TG']:
            f = filtername
        else:
            f = 'Vis.'            
        return f

    @property
    def read(self):
        """
        Return table of observation
        """       
        self.observation = Table.read(self.fileinput, format='ascii.csv')   
        if len(self.observation) > 0:
            self.available = True
            self.title
            self.period
            self.comments
        else:
            self.available = False
    
    def filtername(self, filtername='Vis.'):
        """
        Update filter
        """
        if self.available:
            self.filter = self.isfilter(filtername)

    @property
    def Vis(self):
        if self.available:
            self.filter = 'Vis.'   

    @property
    def I(self):
        if self.available:
            self.filter = 'I' 

    @property
    def R(self):
        if self.available:
            self.filter = 'R'  
                        
    @property
    def V(self):
        if self.available:
            self.filter = 'V'    
            
    @property
    def B(self):
        if self.available:
            self.filter = 'B'    
            
    @property
    def CV(self):
        if self.available:
            self.filter = 'CV'    
            
    @property
    def TG(self):
        if self.available:
            self.filter = 'TG'    

    @property
    def period(self):
        """
        Return period JD
        """
        if self.available:
            self._period = self.observation['JD'][len(self.observation)-1] - self.observation['JD'][0]
            return self._period

    @property
    def title(self):
        if self.available:
            self.titlename = 'AAVSO -- data-download -- ' + self.observation['Star Name'][0]
        return self.titlename

    @property
    def comments(self):
        if self.available:
            observers = [] 
            for i in self.observation['Observer Code'] : 
                if i not in observers: 
                    observers.append(i)                      
            comment = 'Showing ' + str(len(self.observation)) + ' observations for ' + self.observation['Star Name'][0] + ' from ' + str(len(observers)) + ' observers'
            self.comment = comment
        return self.comment

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
            return self.observation['JD'][0],self.observation['JD'][len(self.observation)-1]

    @property
    def magnitudeMinMax(self):
        """
        Return min and max of magnitude in observations table
        """
        if self.observation:
            mv = []
            for value in self.observations:
                if self.filter == value['Band']:
                    if '<' not in value['Magnitude']:
                        mv.append(float(value['Magnitude']))           
            return min(mv),max(mv)
    
    @property
    def JulianDay(self):
        """
        Return JD table
        """
        return self.JDline.JulianDay
    
    @JulianDay.setter
    def JulianDay(self,JDtable):
        """
        Create JD table
        """
        if JDtable:
            self.JDline.JulianDay = JDtable        

    def plot(self):
        """
        Plot observations table
        """
        if self.available:
            jd_min,jd_max = self.JDMinMax
            mv_min,mv_max = self.magnitudeMinMax
        
            x = []
            y = []                     
            for value in self.observations:
                if self.filter == value['Band']:
                    if '<' not in value['Magnitude']:
                        x.append(value['JD'])
                        y.append(float(value['Magnitude'])) 

            plt.xlim(round(jd_min)-5,round(jd_max)+5)
            plt.ylim(round(mv_min)-1,round(mv_max)+1)
            plt.gca().invert_yaxis()
            plt.scatter(x, y, c = 'black', s = 2, alpha = 0.2)
            self.JDline.plot()
            plt.title(self.title, loc='center')
            plt.xlabel('JD', fontsize = 12)
            if self.filter == 'Vis':
                plt.ylabel(r'$m_v$', fontsize = 12)
            else:
                plt.ylabel(self.filter, fontsize = 12)
            plt.show()

class vsx(object):
    """
    Class AAVSO VSX, return TABLE
    """

    def __init__(self, nameID):  
        self.nameID = nameID
        self.vsx_table = Table()
        self.available = False
        self.read

    @property
    def read(self):
        """
        Return TABLE of Variable
        """
        self.table

    @property
    def data(self):
        """
        Return JSON data
        Source : https://www.aavso.org/direct-web-query-vsxvsp
        """
        if ' ' in self.nameID:
            nameID = self.nameID.replace(' ','%20')
        else:
            nameID = self.nameID

        url = "http://www.aavso.org/vsx/index.php"
        params = {}
        params['view']='api.object'
        params['format']='json'
        params['ident']=self.nameID
        response = requests.get(url,params=params)
        if (response.status_code > 400):
            self.available = False
        else:
            self.available = True
            return response.json()
    
    @property
    def table(self):
        """
        Return data table
        """
        result = self.data['VSXObject']
        header = []
        value = []
        types = []
        for item in result:
            value.append(result[item])
            header.append(item)
            types.append('str')
    
        self.vsx_table = Table(names = header, dtype = types) 
        self.vsx_table.add_row(value)
            
    @property
    def observations(self):
        """
        Return vsx table
        """
        if self.available:
            return self.vsx_table
    
    @property
    def name(self):
        """
        Return vsx name
        """
        if self.available:
            return self.vsx_table['Name'][0]
    
    @property
    def coordinates(self):
        """
        Return vsx RA,DEC (degree,degree)
        """
        if self.available:
            return float(self.vsx_table['RA2000']), float(self.vsx_table['Declination2000'])

    @property
    def hourdegree(self):
        """
        Return vsx RA,DEC (Hour,Degree)
        """
        if self.available:
            c = SkyCoord(ra=float(self.vsx_table['RA2000'])*u.degree, dec=float(self.vsx_table['Declination2000'])*u.degree)                       
            return c.ra.hour, c.dec.degree
    
class _JDline(object):
    """
    Class line Julian Day 
    """

    def __init__(self):  
        self.JDtable = []

    @property
    def JulianDay(self):
        """
        Return JD table
        """
        return self.JDtable
    
    @JulianDay.setter
    def JulianDay(self,JDtable):
        """
        Add JD's
        """
        self.JDtable = JDtable
    

    def plot(self):
        """
        Plot line of JD's
        """
        plt.vlines(self.JDtable, -30,30 , linestyles = 'dashed', colors = 'red', alpha = 0.4)