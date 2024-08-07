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
# Astropy mods
from astropy.time import Time
# User mods
from ciboulette.sql import compoments, interface

class datarecords(interface.interfaces):
    filter_names = ['scienceprogram', 'observation', 'instrument', 'target', 'sequence', 'ObservingConditions', 'Observinglog']

# datarecord.put avoir toutes les valeurs et faire les fonction
#                     sienceprogram,observation,instrument,target,sequence,observingconditions,observinglo
# faire une classe observing_condition(value default.... , 50%, 20%)
# faire une classe observing_log(value default None, pdf, notebook)
    

    def __init__(self):
        self.filters = datarecords.filter_names[1]
        self.header = 'id'
        self.values = '1'

    
    @property
    def edit(self):
        """
        Print observation id
        """
        self.observation_print(int(self.values))
    
    @property
    def find(self):
        """
        Find observation, instrument or target text type. Return observation id list
        """
        resources = list()
        if type(self.values) == 'string' or type(self.values) != '':
            
            if self.filters == datarecords.filter_names[1]:                  
                if self.header == 'collection':
                    for data in self.observation_by_collection(self.values):
                        #self.observation_print(data['observation_id'])
                        resources.append(data['observation_id'])
                    
                if self.header == 'title':
                    for data in self.observation_by_title(self.values):
                        #self.observation_print(data['observation_id'])
                        resources.append(data['observation_id'])
                    
                if self.header == 'scheduling':
                    if ";" in self.values:
                        min, max = self.values.split(";")
                        jd_min = Time(min)
                        jd_max = Time(max)
                        for data in range(1, int(self.observation_last_id['observation_id'])+1):
                            scheduling = self.observation_by_id(data)['scheduling']   
                            jd_scheduling = Time(scheduling)
                            if jd_min < jd_scheduling < jd_max:
                                resources.append(data)
                    else:
                        for data in self.observation_by_scheduling(self.values):
                            resources.append(data['observation_id'])

                if self.header == 'notes':
                    for data in self.observation_by_notes(self.values):
                        #self.observation_print(data['observation_id'])
                        resources.append(data['observation_id'])
        
            if self.filters == datarecords.filter_names[2]:
                if self.header == 'name':
                    for data in self.instrument_by_name(self.values):
                        resources.append(data['observation_id'])

                if self.header == 'filter':
                    for data in self.instrument_by_filter(self.values):
                        resources.append(data['observation_id'])

                if self.header == 'disperser':
                    for data in self.instrument_by_disperser(self.values):
                        resources.append(data['observation_id'])

                if self.header == 'camera':
                    for data in self.instrument_by_camera(self.values):
                        resources.append(data['observation_id'])

            if self.filters == datarecords.filter_names[3]:
                if self.header == 'name':
                    for data in self.target_by_name(self.values):
                        resources.append(data['observation_id'])

                if self.header == 'notes':
                    for data in self.target_by_notes(self.values):
                        resources.append(data['observation_id'])
        return resources

    @property
    def settings(self):
        """
        @return: instrument and field of observation ID
        @set: observation ID
        """
        observation_id = int(self.values)
        dataset = []
        resources = dict()

        # Get target
        data_target = self.target_by_id(int(observation_id))
        dataset.append(data_target['name'])

        # Get scheduling 
        data_observation = self.observation_by_id(int(observation_id))
        dataset.append(data_observation['scheduling'])

        # Get instrument data
        data_instrument = self.instrument_by_id(int(observation_id))
        dataset.append(data_instrument['camera'])
        dataset.append(data_instrument['focal'])
        dataset.append(round(data_instrument['focal']/data_instrument['aperture'], 1))

        # Get camera data
        data_camera = self.camera_by_name(data_instrument['camera'])

        # Get sampling
        sampling = (2*math.atan((data_camera['size_pixel']/1000)/(2*data_instrument['focal']*1000)))*216000
        dataset.append(round(sampling, 2))

        # Get field x, y
        field_ccd = data_camera['size_x']*data_camera['size_pixel']/1000 
        field_x = 2 * math.atan(field_ccd/(2*data_instrument['focal']*1000))*3600
        dataset.append(round(field_x, 2))

        field_ccd = data_camera['size_y']*data_camera['size_pixel']/1000 
        field_y = 2 * math.atan(field_ccd/(2*data_instrument['focal']*1000))*3600
        dataset.append(round(field_y, 2))

        # Get magnitude
        dataset.append(round(math.log10(data_instrument['aperture']*1000)*5+7.2, 2))

        # Get Filter data
        data_filter = self.filter_by_name(data_instrument['filter'])
        dataset.append(data_filter['name'] + " [" + str(data_filter['min']) + ":" + str(data_filter['max']) + "]nm")
        dataset.append(data_filter['data'])
        data_filter_iso = self.filter_data_iso(data_filter['data'])
        dataset.append(data_filter_iso['spectral axis'])
        dataset.append(data_filter_iso['flux'])

        # Get disperser if exist
        data_disperser = data_instrument['disperser']
        if data_disperser:
            data_of_disperser = self.disperser_by_name(data_disperser)
            dataset.append(data_of_disperser['name'])
            dataset.append(data_of_disperser['line'])
            dataset.append(data_of_disperser['grism angle'])
        
        headers = self.observation_table_header
        if dataset:
            for header, value in zip(headers, dataset):
                    resources.setdefault(header, value)
        return resources        

























            
