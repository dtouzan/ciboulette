"""
class interface for SQLite3 to archivage, Mast modules
"""

__authors__ = ("Dominique Touzan","ciboulette module")
__contact__ = ("dtouzan@gmail.com","https://github.com/dtouzan/ciboulette")
__copyright__ = "MIT"
__date__ = "2023-12-08"
__version__= "1.0.0"

# Globals mods
import csv
# User mods

from ciboulette.sql import compoments, insertion, selection

class interfaces(compoments.compoment):

    def mast_in(self,scienceprogram_title: str, mast_file='mast_for_sql.csv'):
        """
        Import mast file to database
        @set: scienceprogram_title
        @set: mast_file
        """
        data_in = insertion.insert() 
        data_in.connect
        with open(mast_file, 'r') as file:
            reader = csv.reader(file, delimiter='\n')
            for row in reader:
                print(row[0])
                data_in.mast(scienceprogram_title, row[0])
        data_in.close

    @property
    def mast_out(self):
        """
        Export vue mast_select for table
        """
        data_out = selection.select() 
        data_out.connect   
        resources = data_out.mast
        data_out.close
        return resources

    @property
    def mast_last_id(self):
        """
        Export vue mast_last_id 
        """
        data_out = selection.select() 
        data_out.connect   
        resources = data_out.mast_last_id
        data_out.close
        return resources[1]

    
    @property
    def scienceprogram_type_header(self):
        """
        @return: types list of sciencprogram
        """
        data_out = selection.select() 
        data_out.connect
        resources = data_out.scienceprogram_type_header       
        data_out.close
        return resources[0].split(';')

    def scienceprogram_observing_time(self, scienceprogram_title: str):
        """
        @return: observing time of sciencprogram
        """
        result = 0.0
        data_out = selection.select() 
        data_out.connect
        resources = data_out.scienceprogram_observing_time(scienceprogram_title)
        for resource in resources:
            result = result+(resource[1]-resource[0])
        data_out.close
        return result

    @property
    def scienceprogram_title(self):
        """
        @return: sciencprogram title list
        """
        data_out = selection.select() 
        data_out.connect
        dataset = data_out.scienceprogram_title   
        data_out.close
        resources = []
        for value in dataset:
            resources.append(value[0])
        return resources

    def scienceprogram_by_title(self, scienceprogram_title:str):
        """
        @return: scienceprogram data for the title (dict)
        @set: scienceprogram title
        """
        data_out = selection.select() 
        data_out.connect
        dataset = data_out.scienceprogram_by_title(scienceprogram_title)
        headers = data_out.scienceprogram_header
        data_out.close
        resources = dict()
        for header, value in zip(headers[0].split(';'), dataset):
            resources.setdefault(header, value)          
        return resources

    @property
    def collection(self):
        """
        @return: collections list of observation
        """
        data_out = selection.select() 
        data_out.connect
        dataset = data_out.collection
        data_out.close
        resources = []
        for value in dataset:
            resources.append(value[0])
        return resources
       
    def instrument_exposure_time(self, scienceprogram_title: str):
        """
        @return: exposure time of instrument
        """
        result = 0.0
        data_out = selection.select() 
        data_out.connect
        resources = data_out.instrument_exposure_time(scienceprogram_title)
        for resource in resources:
            result = result+(resource[0])
        data_out.close
        return result

    def observation_by_id(self, id:int):
        """
        @return: observation data by id (dict)
        @set: observation id
        """
        data_out = selection.select() 
        data_out.connect
        resources = dict()
        dataset = data_out.observation_by_id(id)
        if dataset:
            headers = data_out.observation_header
            for header, value in zip(headers[0].split(';'), dataset):
                resources.setdefault(header, value)  
        data_out.close
        return resources

    def sequence_by_id(self, id:int):
        """
        @return: observation data by id (dict)
        @set: observation id
        """
        data_out = selection.select() 
        data_out.connect
        resources = []
        dataset = data_out.sequence_by_id(id)
        if dataset:
            headers = data_out.sequence_header
            for datatable in dataset:
                datadict = dict()
                for header, value in zip(headers[0].split(';'), datatable):
                    datadict.setdefault(header, value)
                resources.append(datadict)               
        data_out.close
        return resources

    def instrument_by_id(self, id:int):
        """
        @return: instrument data by id (dict)
        @set: observation id
        """
        data_out = selection.select() 
        data_out.connect
        resources = dict()
        dataset = data_out.instrument_by_id(id)
        if dataset:
            headers = data_out.instrument_header
            for header, value in zip(headers[0].split(';'), dataset):
                resources.setdefault(header, value)  
        data_out.close
        return resources

    def target_by_id(self, id:int):
        """
        @return: target data by id (dict)
        """
        data_out = selection.select() 
        data_out.connect
        resources = dict()
        dataset = data_out.target_by_id(id)
        if dataset:
            headers = data_out.target_header
            for header, value in zip(headers[0].split(';'), dataset):
                resources.setdefault(header, value)  
        data_out.close
        return resources

    def observinglog_by_id(self, id:int):
        """
        @return: observinglog data by id (dict)
        @set: observinglog id
        """
        data_out = selection.select() 
        data_out.connect
        resources = dict()
        dataset = data_out.observinglog_by_id(id)
        if dataset:
            headers = data_out.observinglog_header
            for header, value in zip(headers[0].split(';'), dataset):
                resources.setdefault(header, value)  
        data_out.close
        return resources

    def observingconditions_by_id(self, id:int):
        """
        @return: observingconditions data by id (dict)
        @set: observingconditions id
        """
        data_out = selection.select() 
        data_out.connect
        resources = dict()
        dataset = data_out.observingconditions_by_id(id)
        if dataset:
            headers = data_out.observingconditions_header
            for header, value in zip(headers[0].split(';'), dataset):
                resources.setdefault(header, value)  
        data_out.close
        return resources

    def scienceprogram(self, title: str, status=1, contact='dtouzan@gmail.com', observing_time=0, type_SP='science', dataset='dataset/archives'):
        """
        View SQL insert scienceprogram
        """
        data_in = insertion.insert() 
        data_in.connect
        data_in.scienceprogram(title, status, contact, observing_time, type_SP, dataset)
        data_in.close

        
    def sequence(self, observation_id: int, title='sequence', label='001', type='light', timeline_min=0, timeline_max=0, compoment='None'):
        """
        View SQL insert sequence
        """
        data_in = insertion.insert() 
        data_in.connect
        data_in.sequence(observation_id, title, label, type, timeline_min, timeline_max, compoment)
        data_in.close

    def target(self, observation_id:int, name='default', class_type='default', RA=0.0, DEC=0.0, notes='default'):
        """
        View SQL insert target
        """
        data_in = insertion.insert() 
        data_in.connect
        data_in.target(observation_id, name, class_type, RA, DEC, notes)
        data_in.close

    def observinglog(self, observation_id:int, label='default', filename='default_observinglog.txt', comment='default observing log file'):
        """
        View SQL insert observinglog
        """
        data_in = insertion.insert() 
        data_in.connect
        data_in.observinglog(observation_id, label, filename, comment)
        data_in.close

    def observingconditions(self, observation_id:int, sky_background=100, cloud_cover=20, image_quality=80, water_vapor=60, elevation_constraint=30, timming_window='night'):
        """
        View SQL insert observingconditions
        """
        data_in = insertion.insert() 
        data_in.connect
        data_in.observingconditions(observation_id, sky_background, cloud_cover, image_quality, water_vapor, elevation_constraint, timming_window)
        data_in.close