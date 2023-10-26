"""
AAVSO WebObs class
https://www.aavso.org/
"""

__authors__ = ("Dominique Touzan","ciboulette module")
__contact__ = ("dtouzan@gmail.com","https://github.com/dtouzan/ciboulette")
__copyright__ = "MIT"
__date__ = "2023-10-24"
__version__= "1.0.0"

# Globals mods
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import os
import io
import wget
import requests

# Astropy mods
from astropy.table import Table
from astropy import units as u
from astropy.coordinates import SkyCoord

# Users mods
from ciboulette.aavso.compoments import compoment

class web_obs(compoment):
    """
    Class for AAVSO web observation.
    @fileouput: aavso.html
    @fileinput: filtername {vis|ccd}
    """

    def __init__(self, nameID, filtername='Vis', fileoutput='aavso.html'):
        self.nameID = nameID
        self.filter = filtername
        self.fileoutput = fileoutput
        self.titlename = ''
        self.comment = ''
        self.html = BeautifulSoup()
        self.filter = self.isfilter(filtername)
        self.read

    @property
    def read(self):
        """
        @return: HTML of observation
        Ex:  wget --no-check-certificate 'https://app.aavso.org/webobs/results/?star=' -O aavso.html
        """
        if os.path.exists(self. fileoutput) :
            os.remove(self.fileoutput)

        if ' ' in self.nameID:
            nameID = self.nameID.replace(' ','%20') # HTML symbol
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
            self._title
            self._comments
            self._table

    @property
    def _title(self):
        """
        @return: Title of HTML
        """
        self.titlename = self.html.title.contents[0] + ' -- ' + self.nameID
        return self.titlename

    @property
    def _comments(self):
        """
        @return: Comments of HTML
        """
        comment = self.html.find(id='obsinfo').contents[0].string
        comment = comment + self.html.find(id='obsinfo').contents[1].string
        comment = comment + self.html.find(id='obsinfo').contents[2].string.replace('\n  \n','').replace('\n','').replace('  ',' ')
        comment = comment + self.html.find(id='obsinfo').contents[3].string
        comment = comment + self.html.find(id='obsinfo').contents[4].string.replace('\n  \n  \n  \n ','')
        comment = comment + self.html.find(id='obsinfo').contents[5].string
        comment = comment + self.html.find(id='obsinfo').contents[6].string.replace('\n  \n  \n  \n  \n  ','')
        self.comment = comment
        return self.comment

    def isfilter(self, filtername='vis'):
        """
        @return: filter
        """
        if filtername in  ['Vis','I','R','B','V']:
            f = filtername
        else:
            f = 'Vis'
        return f

    @property
    def isccd(self):
        """
        @return: true if in ccd filter
        """
        if self.filter in ['I','R','B','V']:
            return True
        else:
            return False

    @property
    def _data(self):
        """
        @return: data of html file observations
        """
        data = []
        data = self.html.table.contents[3].get_text().replace('\n','|').\
                    replace('Details...|||||||||Comp Star|Check Star|Transformed|Chart|Comment Codes|Notes|||||','').\
                    replace('|||||||||','<>').\
                    replace('|||||||','').\
                    replace('|||','').\
                    replace('|             (','(').\
                    replace('|            ','').split('<>')
        return data

    @property
    def _table(self):
        """
        @return: Table of html file observations
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

        for ligne in self._data:
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
            self.dataset = Table([Star,JD,Calendar_Date,Magnitude,Error,Filter,Observer,Comp_Star,Check_Star,Transformed,Chart,Comment_Codes,Notes],
                      names=['Star', 'JD', 'Calendar Date', 'Magnitude', 'Error', 'Filter', 'Observer', 'Comp Star', 'Check Star', 'Transformed', 'Chart', 'Comment Codes', 'Notes'])
        else:
            return False

    @property
    def period(self):
        """
        @return: period JD or 0
        """
        if self.dataset:
            return self.dataset['JD'][0] - self.dataset['JD'][-1]
        else:
            return 0

    @property
    def JDMinMax(self):
        """
        @return: min and max JD in observations table
        """
        if self.available:
            return self.dataset['JD'][-1],self.dataset['JD'][0]
        else:
            return 0, 0

    @property
    def magnitudeMinMax(self):
        """
        @return: min and max of magnitude in observations table
        """
        if self.available:
            return min(self.dataset['Magnitude']),max(self.dataset['Magnitude'])
        else:
            return False, False

    def plot(self):
        """
        Plot observations table
        """
        if self.available:
            jd_min,jd_max = self.JDMinMax
            mv_min,mv_max = self.magnitudeMinMax

            x = []
            for value in self.dataset:
                x.append(value['JD']-jd_min)
            y = self.dataset['Magnitude']

            mymodel = np.poly1d(np.polyfit(x, y, 5))
            myline = np.linspace(0, jd_max-jd_min, 2000)

            plt.xlim(-.5,round(jd_max-jd_min)+.5)
            plt.ylim(round(mv_min)-0.5,round(mv_max)+0.5)
            plt.gca().invert_yaxis()
            plt.scatter(x, y, c = 'black', s = 2, alpha = 0.5)
            plt.plot(myline, mymodel(myline))
            plt.title(self.titlename, loc='center')
            plt.xlabel(f'{int(jd_min)} JD', fontsize = 12)
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

