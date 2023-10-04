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
Focal                  float            focal
Format                 float            format
Seeing                 float            seeing
Moon                   float            moon
jpegURL                string           jpeg_url
url                    string           url

OT Mast class

Name             Type                 Variable name
-----------------     --------         -----------------------
Observation Type       string           intentType
Mission                string           obs_collection
Instrument             string           instrument_name
Filters                string           filters
Disperser              string           disperser
Target Name            string           target_name
Target Classification  string           target_classification
Observation ID         string           obs_id
RA                     float            s_ra
Dec                    float            s_dec
Principal Investigator string           proposal_pi
Product Type           string           dataproduct_type
Calibration Level      int              calib_level
Scheduling             string           scheduling       
Start Time             float            t_min              
End Time               float            t_max
Exposure Length        float            t_exptime
Observation Title      string           obs_title
Focal                  float            focal
Format                 float            format
url                    string           url

"""

__authors__ = ("Dominique Touzan","ciboulette module")
__contact__ = ("dtouzan@gmail.com","https://github.com/dtouzan/ciboulette")
__copyright__ = "MIT"
__date__ = "2023-04-10"
__version__= "1.0.0"

# Globals mods
import time
import os
from collections import Counter, OrderedDict
import wget
from datetime import datetime
# Astropy mods
from astropy.table import Table, unique, vstack
from astropy import units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, Angle, ICRS
from astroquery.simbad import Simbad
from astroquery.mpc import MPC
# User mods
from ciboulette.base import constant



class Mast(object):
    
    def __init__(self, fileoutput='mast.csv'):
        self.fileoutput = fileoutput
        self.observation = Table()
        self.available = True  
        self.disperser = 'SA200'
        self.observation_number = -4 # Header
        
    @property
    def exist(self):
        """
        @return: True if exist, False if nul
        """
        if len(self.observation) > 0:
            return True
        else:
            return False

    def read(self, fileinput):
        """
        @return:  Create observation list if exist
        @fileinput: A string representing the file Mast
        """
        if os.path.exists(fileinput) :

            self.observation = Table.read(fileinput, format='ascii.csv',header_start=2,data_start=3)   
            self.observations['obs_title'].mask = [False]
        return self.exist
    
    def get_number(self, fileinput):
        """
        @return:  A number representing observation ID   
        @fileinput: A string representing the file Mast
        """
        if fileinput == '':
            self.observation_number = 0
        else:
            with open(fileinput, 'r') as file_mast:
                self.observation_number = -4 # Header
                for line in file_mast:
                    self.observation_number += 1  
            
        return self.observation_number
   
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
        @return:  A list representing Names headers
        """
        return self.observations.colnames

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
    
    def query_project(self, projet_name='HII'):
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

 
    def _query_all(self, name='target_name', target='M31'):
        """
        @return:  A table representing observations find in table
        @name:  A string representing name
        @target:  A string representing target find
        """
        if len(self.observation) > 0:
            observations = self.header_names
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

    def split(self, line='name-AAAAMMJJ-HHMM-nxexptimes-ffocale.fits'):
        """
        @return:  A table representing observation fits file
        @line:  A string representing name fits file
        
        '-': Representing split caracter
        
        """
        name = line.split('.')[0]
        return name.split('-')
    
    def files_name(self, directory='dataset'):
        """
        @return:  A table representing observation files name
        @directory:  A string representing the dataset
        """
        return os.listdir(directory) 
    
    def target_name(self, table):
        """
        @return:  A string representing target name
        @table: A table representing a split file name
        """
        return str(table[0])
 
    def exptime(self, table):
        """
        @return:  A string representing Exposure Length
        @table: A table representing a split file name
        """
        line = table[3]
        line = line.split('s')[0]
        line = line.split('x')
        exposition_time = int(line[0]) * int(line[1])
        return str(exposition_time)
    
    def focal(self, table):
        """
        @return:  A string representing focal
        @table: A table representing a split file name
        """
        line = table[4]
        focal = float(line.split('f')[1]) / 1000
        return str(focal)

    def date_format(self, table):
        """
        @return:  A string representing UT date
        @table: A table representing a split file name
        """
        date_line = table[1]
        time_line = table[2]
        date = str(date_line[0:4]) + '-' + str(date_line[4:6]) + '-' + str(date_line[6:8]) + 'T' + str(time_line[0:2]) + ':' + str(time_line[2:4]) + ':' + '00' 
        return date
 
    def target_name_format(self, table):
        """
        @return:  A string representing MAST target_name
        @table: A table representing a split file name
        """
        return self.target_name(table)

    def t_min_format(self, table):
        """
        @return:  A string representing MAST Start time (t_min)
        @table: A table representing a split file name
        """
        t = Time(self.date_format(table), format='isot', scale='utc')
        return str(t.mjd)
 
    def t_max_format(self, table):
        """
        @return:  A string representing MAST End time (t_max)
        @table: A table representing a split file name
        """
        t = Time(self.date_format(table), format='isot', scale='utc')
        exp_date = int(self.exptime(table)) / 86400
        t_max = t.mjd + exp_date
        return str(t_max)
 
    def t_exptime_format(self, table):
        """
        @return:  A string representing MAST exposure Length 'second'
        @table: A table representing a split file name
        """
        return self.exptime(table)

    def intent_type_format(self, string='a'):
        """
        @return:  A string representing MAST observation Type (intentType)
        @string:  A string representing a name type
                  'S': science
                  'A': analysis
                  's': spectrum
                  'a': archive (default)
        """
        match string:
            case 'S':
                itype = 'science'
            case 'A':
                itype = 'analysis'
            case _:
                itype = 'archive'
        return itype
        
    def t_obs_release_format(self, date=''):
        """
        @return: A string representing MAST release date (t_obs_release)
        @table: A table representing a split file name
        """
        if date == '':
            today = datetime.today()        
            date = today.strftime('%Y-%m-%dT%H:%M:%S')
        t = Time(date, format='isot', scale='utc')
        return str(t.mjd)

    @property
    def calib_level(self):
        """
        @return:  A value representing calibration level (1, 2 or 3)
        """
        return 1

    @property
    def obs_collection(self):
        """
        @return:  A value representing observaton collection (UT1, UT2, OT Library)
        """
        return 'OT_Library_UT1'
    
    @property
    def instrument_name(self):
        """
        @return:  A value representing instrument name (UT1, CIBOULETTE_S, CIBOULETTE_V, CIBOULETTE_G, CIBOULETTE_N, ...)
        """
        return 'UT1'

    @property
    def filter_default(self):
        """
        @return:  A value representing filter name
        """
        return 'IR-CUT'

    @property
    def formats(self):
        """
        @return:  A fits extention
        """
        return 'fits'

    @property
    def dataproduct_type(self):
        """
        @return:  A value representing data product type (light, dark, flat, offset)
        """
        return 'light'   

    @property
    def obs_title(self):
        """
        @return:  A value representing observation title
        """
        return 'None'    
    
    @property
    def proposal_pi(self):
        """
        @return:  A value representing proposal principal investigator
        """
        return 'dtouzan@gmail.com'        
    
    def scheduling(self,table):
        """
        @return:  A value representing schediling observation (AAAA-MM-DDTHH:MM:SS)
        """
        return self.date_format(table)
    
    def get_coordinates(self, string, scheduling):
        """
        @return: A string representing RA, DEC, TYPE with astroquery name object and DISPERSER
        """
        catalog = ('M', 'MESSIER', 'IC', 'UGC', 'NGC', 'HD', 'COL', 'LBN', 'V', 'SN', 'ABELL', 'DO', 'KING', 'DWB', 'STOCK', 'CR', 'ATLAS', 'TR')
        supernovae = ('SN', 'ASAS', 'ATLAS')
        comet = ('P_', '_P', 'C_')
        ra = 0
        dec = 0
        otype = 'NaN'
        disperser = 'NaN'

        #For spectrum name
        String = string.upper()
        if String[0] == 'S' and String[1] == '_':
            name_object = String.split('S_')[1]
            disperser = self.disperser
        else:
            name_object = string

        # For asteroid
        try:
            number = int(name_object)
            otype = 'Asteroid'
            ephemerid = MPC.get_ephemeris(target=number, start=scheduling, step=1*u.d, number=1)
            ra = ephemerid['RA'].value[0]
            dec = ephemerid['Dec'].value[0]
        except ValueError:
            otype = otype

        #For super novae
        for c in supernovae:
            if c in name_object.upper():
                otype = 'SN*'
        
        #For comet
        for c in comet:
            if c in name_object.upper():
                otype = 'Comet'
                names = name_object.split('_')
                if c in comet[1]:
                    name = names[0]+names[1]
                else:
                    name = names[0]+'/'+names[1]+' '+names[2]
                ephemerid = MPC.get_ephemeris(name, start=scheduling, step=1*u.d, number=1)
                ra = ephemerid['RA'].value[0]
                dec = ephemerid['Dec'].value[0]

        #For object catalog 
        for c in catalog:        
                if c in name_object.upper():
                    customSimbad = Simbad()
                    customSimbad.add_votable_fields('otype')
                    result_table = customSimbad.query_object(name_object)
                    if result_table:
                        c = SkyCoord(ra=result_table['RA'], dec=result_table['DEC'], unit=(u.deg, u.deg), frame='icrs')
                        ra = c.ra.deg[0]*15    
                        dec = c.dec.deg[0]  
                        otype = result_table['OTYPE'][0]
                            
        return ra, dec, otype, disperser
        
    def create(self, directory='dataset', file='mast.csv'):
        """
        @return:  False or create the Mast file
        @file: A string representing the file Mast
        """       
        if self.available:          
            # create line
            obs_id = self.observation_number
            print(f'Create: observations file index {obs_id}')
            listing = self.files_name(directory)
            with open(file, 'w') as file_mast:
                for name in listing:
                    if '.fits' in name:
                        name_list = self.split(name)
                        obs_id += 1
                        name_object = self.target_name_format(name_list)
                        scheduling = self.scheduling(name_list)
                        print(obs_id, name)
                        intent_type = 'S'
                        ra, dec, otype, disperser = self.get_coordinates(name_object, scheduling)
                        print(f'{self.intent_type_format(intent_type)},'
                                f'{self.obs_collection},'
                                f'{self.instrument_name},'
                                f'{self.filter_default},'
                                f'{disperser},'
                                f'{name_object},'
                                f'{otype},'
                                f'{str(obs_id)},'
                                f'{ra},'
                                f'{dec},'
                                f'{self.proposal_pi},'
                                f'{self.dataproduct_type},'
                                f'{self.calib_level},'
                                f'{scheduling},'
                                f'{self.t_min_format(name_list)},'
                                f'{self.t_max_format(name_list)},'
                                f'{self.t_exptime_format(name_list)},'
                                f'{self.obs_title},'
                                f'{self.focal(name_list)},'
                                f'{self.formats},'
                                f'{name}', file=file_mast)
        else:
            return False