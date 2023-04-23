"""
Mast class
File id google 12QY7fQLqnoySHFnEoLMWQbqYjHmaDpGn

       Name             Type                 Variable name
-----------------     --------         -----------------------
Observation Type       string           intentType
Mission                string           obs_collection
Instrument             string           instrument_name
Detector               string           detector
Project                string           project
Filters                string           filters
Waveband               string           wavelength_region
Target Name            string           target_name
Target Classification  string           target_classification
Observation ID         string           obs_id
RA                     float            s_ra
Dec                    float            s_dec
Proposal ID            string           proposal_id
Principal Investigator string           proposal_pi
Product Type           string           dataproduct_type
Calibration Level      int              calib_level
Start Time             float            t_min              
End Time               float            t_max
Exposure Length        float            t_exptime
Min. Wavelength        float            em_min
Max. Wavelength        float            em_max
Observation Title      string           obs_title
Release Date           float            t_obs_release
Proposal Type          string           proposal_type
Sequence Number        int              sequence_number
Region                 string           s_region
Focale                 float            focal
Format                 float            format
Seeing                 float            seeing
Moon                   float            moon
jpegURL                string           jpeg_url
url                    string           url

"""

import time
from astropy.table import Table, unique, vstack
from astropy import units as u
import os
import wget
from ciboulette.base import constant
from collections import Counter, OrderedDict


class Mast(object):
    
    def __init__(self, idgoogledrive='12QY7fQLqnoySHFnEoLMWQbqYjHmaDpGn', fileoutput='mast.csv'):
        self.idgoogledrive = idgoogledrive
        self.fileoutput = fileoutput
        self.observation = Table()
        self.header = Table()     
        self.available = False      
        
    @property
    def create(self):
        """
        @return: True if exist, False if nul
        """
        if len(self.observation) > 0:
            return True
        else:
            return False
    
    @property
    def read(self):
        """
        @return:  A boolean representing available (True is table create, False Otherwise)       
                  Read your MAST type file
                  Read your MAST header type file
                  Ex:  wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=12QY7fQLqnoySHFnEoLMWQbqYjHmaDpGn' -O mast.csv  
        """
        if os.path.exists(self.fileoutput) :
            os.remove(self.fileoutput)
        url = 'https://docs.google.com/uc?export=download&id='+self.idgoogledrive
        filedownload = wget.download(url,out=self.fileoutput,bar=None)      
        # For MAST data_start=3
        self.header = Table.read('mast_header.csv', format='ascii.csv',header_start=2,data_start=3)
        self.observation = Table.read(self.fileoutput, format='ascii.csv',header_start=2,data_start=3)   
        self.observations['obs_title'].mask = [False]
        self.observations['obs_id'].mask = [False]
        
        if len(self.observation) > 0:
            self.available = True
        else:
            self.available = False
        return self.available

    @property
    def idfiledrive(self):
        """
        @return:  A sting representing ID google drive file
        """     
        return self.idgoogledrive    
    
    @idfiledrive.setter
    def idfiledrive(self,idgoogledrive):
        """
        @set: Set ID google drive file
        @idgoogledrive: A string representing ID google drive file.csv  
        """     
        self.idgoogledrive = idgoogledrive                 

    @property
    def output(self):
        """
        @return: Fileoutput.csv name
        """     
        return self.fileoutput

    @output.setter
    def output(self,fileoutput):
        """
        Set table of exposures with google drive 
        @fileoutput: A string representing file.csv output
        """
        self.fileoutput = fileoutput

    def ha(self,observation):
        """
        @return:  A float  representing RA of observation. Format: Hours H.HHHH
        @observation:  A class representing observation 
        """           
        if self.available:
            return float(observation['s_ra'])/15

    def ra(self,observation):
        """
        @return:  A float representing RA of observation. Format: Hours D.DDDD
        @observation:   A class representing observation
        """           
        if self.available:
            return float(observation['s_ra'])

    def dec(self,observation):
        """
        @return:  A float representing DEC of observation. Format: Degrees D.DDDD
        @observation:  A class representing observation
        """    
        if self.available:
            return float(observation['s_dec']) 

    def coordinates(self,observation):
        """
        @return:  A float,float representing Coordinates RA,DEC
        @observation:  A class representing observation
        """
        if self.available:
            return self.ra(observation), self.dec(observation)

    @property
    def observations(self):
        """
        @return:  A table representing Observations
        """
        if len(self.observation) > 0:
            return self.observation

    @property
    def header_names(self):
        """
        @return:  A table representing Names headers
        """
        return self.header.colnames

    @property
    def projects(self):
        """
        @return:  A table representing Pojects
        """
        if len(self.observation) > 0:
            words = unique(self.observation, keys='project')
            return words['project']

    @property
    def targets(self):
        """
        @return:  A table representing Targets
        """
        if len(self.observation) > 0:
            words = unique(self.observation, keys='target_name')
            return words['target_name']

    @property
    def filters(self):
        """
        @return:  A table representing filters
        """
        if len(self.observation) > 0:
            words = unique(self.observation, keys='filters')
            return words['filters']

    @property
    def target_classification(self):
        """
        @return:  A table representing targets classifications
        """
        if len(self.observation) > 0:
            words = unique(self.observation, keys='target_classification')
            return words['target_classification']
        
    def query_project(self, projet_name = 'HII'):
        """
        @return:  A table representing observations projects
        @projet_name: A string representing a project name
        """
        return self._query_all('project', projet_name)

    def query_target(self, target_name = 'M31'):
        """
        @return:  A table representing observations targets
        @target_name: A string representing a target name
        """
        return self._query_all('target_name', target_name)
        
    def query_filters(self, filter_name = 'L'):
        """
        @return:  A table representing observations filtes
        @filter_name: A string representing a filter name
        """
        return self._query_all('filters', filter_name)
    
    def query_target_classification(self, target_classification = 'Galaxy'):
        """
        @return:  A table representing observations target classification
        @target_classification:  A string representing a target classification
        """
        return self._query_all('target_classification', target_classification)

    def query_header(self, header_name='intentType', name='archive'):
        """
        @return:  A table representing header name
        @header_name:  A string representing header name 
        @name:  A string representing name in header
        """
        return self._query_all(header_name, name)

 
    def _query_all(self, name = 'target_name', target = 'M31'):
        """
        @return:  A table representing observations find in table
        @name:  A string representing name
        @target:  A string representing target find
        """
        if len(self.observation) > 0:
            observations = self.header
            unique_by_name = unique(self.observation, keys= name)
            if len(unique_by_name) > 0:
                matches = [match for match in unique_by_name[name] if target in match]
                if len(matches) > 0:
                    for targets in matches:
                        mask = self.observation[name] == targets
                        observations = vstack([self.observation[mask], observations])  
                
                    observations = observations[0:len(observations)-1]
                    return observations
                else:
                    return 'No target'
            else:
                return 'No name'
        else:
            return 'No observations'
