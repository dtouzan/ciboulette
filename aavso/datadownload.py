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
import os
import wget
import requests

# Astropy mods
from astropy.table import Table
from astropy import units as u
from astropy.coordinates import SkyCoord

# Users mods
from ciboulette.aavso.compoments import compoment

class load(compoment):
    """
    Class for AAVSO for data download (https://www.aavso.org/data-download).
    @fileinput: datadownload.csv
    @filtername: Vis|B|V|R|I|TG|CV
    """

    def __init__(self, filtername='Vis.', fileinput='aavsodata.csv'):
        self.nameID = ''
        self.fileinput = fileinput
        self.titlename = ''
        self.comment = ''
        self.JDline = _JDline()
        self.filter = self.isfilter(filtername)
        self.read

    def isfilter(self, filtername='Vis.'):
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
        self.dataset = Table.read(self.fileinput, format='ascii.csv')
        if len(self.dataset) > 0:
            self._title
            self.period
            self._comments
        else:
            return False

    def filtername(self, filtername='Vis.'):
        """
        Init filter
        @input: filtername
        """
        self.filter = self.isfilter(filtername)

    @property
    def Vis(self):
        """
        Init filter Vis.
        """
        self.filter = self.isfilter('Vis.')

    @property
    def I(self):
        """
        Init filter I
        """
        self.filter = self.isfilter('I')

    @property
    def R(self):
        """
        Init filter R
        """
        self.filter = self.isfilter('R')

    @property
    def V(self):
        """
        Init filter V
        """
        self.filter = self.isfilter('V')

    @property
    def B(self):
        """
        Init filter B
        """
        self.filter = self.isfilter('B')

    @property
    def CV(self):
        """
        Init filter CV
        """
        self.filter = self.isfilter('CV')

    @property
    def TG(self):
        """
        Init filter TG
        """
        self.filter = self.isfilter('TG')

    @property
    def period(self):
        """
        @return: period JD
        """
        if self.available:
            return self.dataset['JD'][-1] - self.dataset['JD'][0]
        else:
            return 0

    @property
    def _title(self):
        """
        @return: title name
        """
        if self.available:
            self.titlename = 'AAVSO -- data-download -- ' + self.dataset['Star Name'][0]
            return self.titlename
        else:
            return False   

    @property
    def _comments(self):
        """
        @return: comments
        """
        if self.available:
            observers = []
            for i in self.dataset['Observer Code'] :
                if i not in observers:
                    observers.append(i)
            comment = 'Showing ' + str(len(self.dataset)) + ' observations for ' + self.dataset['Star Name'][0] + ' from ' + str(len(observers)) + ' observers'
            self.comment = comment
            return self.comment
        else:
            return False

    @property
    def JDMinMax(self):
        """
        @return: min and max JD in observations table
        """
        if self.available:
            return self.dataset['JD'][0],self.dataset['JD'][-1]
        else:
            return 0, 0

    @property
    def magnitudeMinMax(self):
        """
        @return: min and max of magnitude in observations table
        """
        if self.available:
            mv = []
            for value in self.dataset:
                if self.filter == value['Band']:
                    if '<' not in value['Magnitude']:
                        mv.append(float(value['Magnitude']))
            return min(mv),max(mv)
        else:
            return False, False

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
            for value in self.dataset:
                if self.filter == value['Band']:
                    if '<' not in value['Magnitude']:
                        x.append(value['JD'])
                        y.append(float(value['Magnitude']))

            plt.xlim(round(jd_min)-5,round(jd_max)+5)
            plt.ylim(round(mv_min)-1,round(mv_max)+1)
            plt.gca().invert_yaxis()
            #plt.scatter(x, y, c = 'blue', s = 2, alpha = 0.4)
            plt.plot(x, y , linewidth=2, color='blue', alpha=0.7)
            self.JDline.plot()
            plt.title(self.titlename, loc='center')
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
        plt.vlines(self.JDtable, -30,30 , linestyles = '--', colors = 'red', alpha = 0.3)