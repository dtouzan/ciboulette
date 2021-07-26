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
            plt.scatter(x, y, c = 'black', s = 5, alpha = 0.5)
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
    
    def __init__(self, filtername='Vis', fileinput='aavsodata.csv'):  
        self.nameID = ''
        self.filter = filtername
        self.fileinput = fileinput
        self.titlename = ''
        self.comment = ''
        self.observation = Table()
        self.available = False
        self._period = 0
        self.filter = self.isfilter(filtername)
        self.read 

    def isfilter(self,filtername='vis'):
        """
        Return filter
        """
        if filtername in  ['Vis','I','R','B','V','CV','TG']:
            f = filtername
        else:
            f = 'Vis'            
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
    
    def filtername(self, filtername='Vis'):
        """
        Update filter
        """
        if self.available:
            self.filter = self.isfilter(filtername)

    @property
    def Vis(self):
        if self.available:
            self.filter = self.isfilter('Vis')    

    @property
    def I(self):
        if self.available:
            self.filter = self.isfilter('I')    

    @property
    def R(self):
        if self.available:
            self.filter = self.isfilter('R')   
                        
    @property
    def V(self):
        if self.available:
            self.filter = self.isfilter('V')    
            
    @property
    def B(self):
        if self.available:
            self.filter = self.isfilter('B')    
            
    @property
    def CV(self):
        if self.available:
            self.filter = self.isfilter('CV')    
            
    @property
    def TG(self):
        if self.available:
            self.filter = self.isfilter('TG')    

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
                if self.filter in value['Band']:
                    if '<' not in value['Magnitude']:
                        mv.append(float(value['Magnitude']))           
            return min(mv),max(mv)

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
                if self.filter in value['Band']:
                    if '<' not in value['Magnitude']:
                        x.append(value['JD']-jd_min)
                        y.append(float(value['Magnitude'])) 

            plt.xlim(-.5,round(jd_max-jd_min)+.5)
            plt.ylim(round(mv_min)-0.5,round(mv_max)+0.5)
            plt.gca().invert_yaxis()
            plt.scatter(x, y, c = 'black', s = 5, alpha = 0.2)
            plt.title(self.title, loc='center')
            plt.xlabel(str(int(jd_min))+'\nJD', fontsize = 12)
            if self.filter == 'Vis':
                plt.ylabel(r'$m_v$', fontsize = 12)
            else:
                plt.ylabel(self.filter, fontsize = 12)
            plt.show()

class vsx(object):
    """
    Class AAVSO VSX, return VOTABLE
    """

    def __init__(self, nameID, fileoutput='vsx.html'):  
        self.nameID = nameID
        self.vsx_table = Table()
        self.available = False

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
        j = self.data
        if self.available:
            name = [j["VSXObject"]["Name"]]
            auid = [j["VSXObject"]["AUID"]]
            ra2000 = [j["VSXObject"]["RA2000"]]
            dec2000 = [j["VSXObject"]["Declination2000"]]
            vartype = [j["VSXObject"]["VariabilityType"]]
            period = [j["VSXObject"]["Period"]]
            epoch = [j["VSXObject"]["Epoch"]]
            maxmag = [j["VSXObject"]["MaxMag"]]
            minmag = [j["VSXObject"]["MinMag"]]
            discover = [j["VSXObject"]["Discoverer"]]
            category = [j["VSXObject"]["Category"]]
            oid = [j["VSXObject"]["OID"]]
            constellation = [j["VSXObject"]["Constellation"]]
            self.vsx_table = Table([name,auid,ra2000,dec2000,vartype,period,epoch,maxmag,minmag,discover,category,oid,constellation],
                                   names=['Name', 'AUID', 'RA2000', 'Declination2000', 'VariabilityType', 'Period', 'Epoch', 'MaxMag', 'MinMagr', 'Discoverer', 'Category', 'OID', 'Constellation'])         
            
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
