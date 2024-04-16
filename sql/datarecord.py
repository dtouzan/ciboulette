"""
class data record for SQL interface

IN PROGRESS, DO NOT USED
"""

__authors__ = ("Dominique Touzan","ciboulette module")
__contact__ = ("dtouzan@gmail.com","https://github.com/dtouzan/ciboulette")
__copyright__ = "MIT"
__date__ = "2024-03-12"
__version__= "1.0.0"

# Globals mods
import math
# User mods
from ciboulette.sql import compoments, interface

class datarecords(interface.interfaces):
    filter_names = ['scienceprogram', 'observation', 'instrument', 'target', 'sequence', 'ObservingConditions', 'Observinglog']

# datarecord.put avoir toutes les valeurs et faire les fonction
#                     sienceprogram,observation,instrument,target,sequence,observingconditions,observinglog
# datarecord.get en fonction du filter editer la valeur
# calcul du champ en recherchant et en prenant INSTRUMENT/CAMERA (à rechercher dans TABLE/camera)    

    def __init__(self):
        self.filters = datarecords.filter_names[1]
        self.header = 'id'
        self.values = '1'
    
    @property
    def edit(self):
        """
        Print observation text type
        """
        if type(self.values) == 'string' or type(self.values) != '':
            
            if self.filters == datarecords.filter_names[1]:
                if self.header == 'id':
                    self.observation_print(int(self.values))
                    
                if self.header == 'collection':
                    for data in self.observation_by_collection(self.values):
                        self.observation_print(data['observation_id'])
                    
                if self.header == 'title':
                    for data in self.observation_by_title(self.values):
                        self.observation_print(data['observation_id'])
                    
                if self.header == 'scheduling':
                    for data in self.observation_by_scheduling(self.values):
                        self.observation_print(data['observation_id'])
        
            if self.filters == datarecords.filter_names[2]:
                if self.header == 'name':
                    for data in self.instrument_by_name(self.values):
                        self.observation_print(data['observation_id'])

                if self.header == 'filter':
                    for data in self.instrument_by_filter(self.values):
                        self.observation_print(data['observation_id'])

                if self.header == 'disperser':
                    for data in self.instrument_by_disperser(self.values):
                        self.observation_print(data['observation_id'])

                if self.header == 'camera':
                    for data in self.instrument_by_camera(self.values):
                        self.observation_print(data['observation_id'])

            if self.filters == datarecords.filter_names[3]:
                if self.header == 'name':
                    for data in self.target_by_name(self.values):
                        self.observation_print(data['observation_id'])


    def observation_table(self, observation_id: str):
        """
        @return: instrument and field of observation ID
        @set: observation ID
        """
        dataset = []
        resources = dict()
        data_target = self.target_by_id(int(observation_id))
        dataset.append(data_target['name'])
        
        data_instrument = self.instrument_by_id(int(observation_id))
        dataset.append(data_instrument['camera'])
        dataset.append(data_instrument['focal'])
        dataset.append(round(data_instrument['focal']/data_instrument['aperture'], 1))
               
        data_camera = self.camera_by_name(data_instrument['camera'])
        
        sampling = (2*math.atan((data_camera['size_pixel']/1000)/(2*data_instrument['focal']*1000)))*216000
        dataset.append(round(sampling, 2))
        
        field_ccd = data_camera['size_x']*data_camera['size_pixel']/1000 
        field_x = 2 * math.atan(field_ccd/(2*data_instrument['focal']*1000))*3600
        dataset.append(round(field_x, 2))

        field_ccd = data_camera['size_y']*data_camera['size_pixel']/1000 
        field_y = 2 * math.atan(field_ccd/(2*data_instrument['focal']*1000))*3600
        dataset.append(round(field_y, 2))
        
        dataset.append(round(math.log10(data_instrument['aperture']*1000)*5+7.2, 2))

        headers = self.observation_table_header
        if dataset:
            for header, value in zip(headers, dataset):
                    resources.setdefault(header, value)
        return resources        































            
