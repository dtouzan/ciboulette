"""
AAVSO datadownload class
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

class load(object):
    """
    Class for AAVSO for data download (https://www.aavso.org/data-download).
    @fileinput: datadownload.csv
    @filtername: Vis|B|V|R|I|TG|CV
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
        @return: filter
        """
        if filtername in  ['Vis.','I','R','B','V','CV','TG']:
            f = filtername
        else:
            f = 'Vis.'
        return f

    @property
    def read(self):
        """
        @return: table of observation
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
        @return: filter
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
        @return: period JD
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
        @return: observations table
        """
        if self.observation:
            return self.observation

    @property
    def JDMinMax(self):
        """
        @return: min and max JD in observations table
        """
        if self.observation:
            return self.observation['JD'][0],self.observation['JD'][len(self.observation)-1]

    @property
    def magnitudeMinMax(self):
        """
        @return: min and max of magnitude in observations table
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
        @return: JD table
        """
        return self.JDline.JulianDay

    @JulianDay.setter
    def JulianDay(self,JDtable):
        """
        Create JD table
        """
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

class _JDline(object):
    """
    Class line Julian Day
    """

    def __init__(self):
        self.JDtable = []

    @property
    def JulianDay(self):
        """
        @return: JD table
        """
        return self.JDtable

    @JulianDay.setter
    def JulianDay(self,JDtable):
        """
        Add JD's
        """
        if len(JDtable) > 0:
            for number in JDtable:
                self.JDtable.append(number)
        else:
            self.JDtable.clear()


    def plot(self):
        """
        Plot line of JD's
        """
        plt.vlines(self.JDtable, -30,30 , linestyles = 'solid', colors = 'grey', alpha = 0.1)