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
        with open(mast_file, 'r', newline='') as file:
            reader = csv.reader(file, delimiter=' ', quotechar=',')
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

    def mast_default(self,observation_id: int, name='UT1', camera='nefertiti3199-imx477', binning_x=1, binning_y=1, aperture=0.030):
        """
        Upgrade default mast information to observation and instrument
        @set: observation_id
        @set: instrument name
        @set: instrument camera
        @set: instrument binning_x
        @set: instrument binning_y
        @set: instrument aperture
        """
        data_in = insertion.insert() 
        data_in.connect
        data_in.mast_observation_upgrade(observation_id)
        data_in.mast_instrument_upgrade(observation_id, name, binning_x, binning_y, aperture)
        data_in.mast_instrument_camera(observation_id, camera)
        data_in.close

    def mast_update(self,observation_id: int, observation_title='Observation with UT1', observation_collection='OT_Library_UT1', target_note='not specified'):
        """
        Update default mast information to observation and target
        @set: observation_id
        @set: observation_title
        @set: observation_collection
        @set: target_note
        """
        data_in = insertion.insert() 
        data_in.connect
        data_in.mast_observation_title(observation_id, observation_title)
        data_in.mast_observation_collection(observation_id, observation_collection)
        data_in.mast_target_note(observation_id, target_note)
        data_in.close
    
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

    @property
    def observation_last_id(self):
        """
        @return: observation last id 
        """
        data_out = selection.select() 
        data_out.connect
        resources = dict()
        dataset = data_out.observation_last_id
        if dataset:
            headers = data_out.observation_header
            for header, value in zip(headers[0].split(';'), dataset):
                resources.setdefault(header, value)  
        data_out.close        
        return resources

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

    def observation_by_collection(self, collection:str):
        """
        @return: observation data by collection (dict)
        @set: observation collection
        """
        data_out = selection.select() 
        data_out.connect
        resources = []
        dataset = data_out.observation_by_collection(collection)
        if dataset:
            headers = data_out.observation_header
            for datatable in dataset:
                datadict = dict()
                for header, value in zip(headers[0].split(';'), datatable):
                    datadict.setdefault(header, value)
                resources.append(datadict)               
        data_out.close
        return resources

    def observation_by_title(self, observation_title:str):
        """
        @return: observation data for the title (dict)
        @set: observation title
        """
        data_out = selection.select() 
        data_out.connect
        resources = []
        dataset = data_out.observation_by_title(observation_title)
        if dataset:
            headers = data_out.observation_header
            for datatable in dataset:
                datadict = dict()
                for header, value in zip(headers[0].split(';'), datatable):
                    datadict.setdefault(header, value)
                resources.append(datadict)               
        data_out.close
        return resources

    def observation_by_scheduling(self, observation_scheduling:str):
        """
        @return: observation data for the scheduling (dict)
        @set: observation scheduling, AAAA-MM-DD
        """
        data_out = selection.select() 
        data_out.connect
        resources = []
        dataset = data_out.observation_by_scheduling(observation_scheduling)
        if dataset:
            headers = data_out.observation_header
            for datatable in dataset:
                datadict = dict()
                for header, value in zip(headers[0].split(';'), datatable):
                    datadict.setdefault(header, value)
                resources.append(datadict)               
        data_out.close
        return resources

    def observation_by_notes(self, observation_notes:str):
        """
        @return: observation data for the notes (dict)
        @set: observation notes
        """
        data_out = selection.select() 
        data_out.connect
        resources = []
        dataset = data_out.observation_by_notes(observation_notes)
        if dataset:
            headers = data_out.observation_header
            for datatable in dataset:
                datadict = dict()
                for header, value in zip(headers[0].split(';'), datatable):
                    datadict.setdefault(header, value)
                resources.append(datadict)               
        data_out.close
        return resources
    

    @property
    def observation_table_header(self):
        """
        @return: observation table header (dict)
        """
        data_out = selection.select() 
        data_out.connect
        resources = []
        dataset = data_out.observation_table_header
        if dataset:
            resources = dataset[0].split(';')
        data_out.close
        return resources
        
    def sequence_by_id(self, id:int):
        """
        @return: sequence data by id (dict)
        @set: sequence id
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

    def instrument_by_id(self, instrument_id:int):
        """
        @return: instrument data by id (dict)
        @set: instrument id
        """
        data_out = selection.select() 
        data_out.connect
        resources = dict()
        dataset = data_out.instrument_by_id(instrument_id)
        if dataset:
            headers = data_out.instrument_header
            for header, value in zip(headers[0].split(';'), dataset):
                resources.setdefault(header, value)  
        data_out.close
        return resources
        
    def instrument_by_name(self, instrument_name:str):
        """
        @return: instrument data by name (dict)
        @set: instrument name
        """
        data_out = selection.select() 
        data_out.connect
        resources = []
        dataset = data_out.instrument_by_name(instrument_name)
        if dataset:
            headers = data_out.instrument_header
            for datatable in dataset:
                datadict = dict()
                for header, value in zip(headers[0].split(';'), datatable):
                    datadict.setdefault(header, value)
                resources.append(datadict)               
        data_out.close
        return resources

    def instrument_by_filter(self, instrument_filter:str):
        """
        @return: instrument data by filter (dict)
        @set: instrument filter
        """
        data_out = selection.select() 
        data_out.connect
        resources = []
        dataset = data_out.instrument_by_filter(instrument_filter)
        if dataset:
            headers = data_out.instrument_header
            for datatable in dataset:
                datadict = dict()
                for header, value in zip(headers[0].split(';'), datatable):
                    datadict.setdefault(header, value)
                resources.append(datadict)               
        data_out.close
        return resources

    def instrument_by_disperser(self, instrument_disperser:str):
        """
        @return: instrument data by disperser (dict)
        @set: instrument disperser
        """
        data_out = selection.select() 
        data_out.connect
        resources = []
        dataset = data_out.instrument_by_disperser(instrument_disperser)
        if dataset:
            headers = data_out.instrument_header
            for datatable in dataset:
                datadict = dict()
                for header, value in zip(headers[0].split(';'), datatable):
                    datadict.setdefault(header, value)
                resources.append(datadict)               
        data_out.close
        return resources

    def instrument_by_camera(self, instrument_camera:str):
        """
        @return: instrument data by camera (dict)
        @set: instrument camera
        """
        data_out = selection.select() 
        data_out.connect
        resources = []
        dataset = data_out.instrument_by_camera(instrument_camera)
        if dataset:
            headers = data_out.instrument_header
            for datatable in dataset:
                datadict = dict()
                for header, value in zip(headers[0].split(';'), datatable):
                    datadict.setdefault(header, value)
                resources.append(datadict)               
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

    def target_by_name(self, name:str):
        """
        @return: target data by name 
        """
        data_out = selection.select() 
        data_out.connect
        data_collection = list()
        dataset = data_out.target_by_name(name)
        if dataset:
            headers = data_out.target_header
            for data in dataset:
                resources = dict()
                for header, value in zip(headers[0].split(';'), data):
                    resources.setdefault(header, value)  
                data_collection.append(resources)
        data_out.close
        return data_collection

    def target_by_notes(self, notes:str):
        """
        @return: target data by notes 
        """
        data_out = selection.select() 
        data_out.connect
        data_collection = list()
        dataset = data_out.target_by_notes(notes)
        if dataset:
            headers = data_out.target_header
            for data in dataset:
                resources = dict()
                for header, value in zip(headers[0].split(';'), data):
                    resources.setdefault(header, value)  
                data_collection.append(resources)
        data_out.close
        return data_collection

    def target_coordinates(self, target:str):
        """
        @Return: target coordinates RA,DEC
        """
        RA = DEC = 0
        resources = list()
        dataset = self.target_by_name(target)
        if dataset:
            for data in dataset:
                RA = data['RA']
                DEC = data['DEC']
                resources.append((RA,DEC))
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

    def camera_by_name(self, camera_name: str):
        """
        @return: camera info
        @set:  camera name
        """
        data_out = selection.select() 
        data_out.connect
        resources = dict()
        dataset = data_out.camera_by_name(camera_name)
        if dataset:
            headers = data_out.camera_header
            for header, value in zip(headers[0].split(';'), dataset):
                resources.setdefault(header, value)  
        data_out.close
        return resources

    def filter_by_name(self, filter_name: str):
        """
        @return: filter info
        @set:  filter name
        """
        data_out = selection.select() 
        data_out.connect
        resources = dict()
        dataset = data_out.filter_by_name(filter_name)
        if dataset:
            headers = data_out.filter_header
            for header, value in zip(headers[0].split(';'), dataset):
                resources.setdefault(header, value)  
        data_out.close
        return resources

    def filter_data_iso(self, filter_data:str):
        """
        @return: filter_data_iso header
        @set: filter data
        """
        data_out = selection.select() 
        data_out.connect
        resources = dict()
        dataset = filter_data
        headers = data_out.filter_data_iso_header
        if headers:
            for header, value in zip(headers[0].split(';'), dataset.split(';')):
                resources.setdefault(header, value)  
        data_out.close
        return resources

    def disperser_by_name(self, disperser_name: str):
        """
        @return: disperser info
        @set:  disperser name
        """
        data_out = selection.select() 
        data_out.connect
        resources = dict()
        dataset = data_out.disperser_by_name(disperser_name)
        if dataset:
            headers = data_out.disperser_header
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

    def instrument(self, observation_id:int, name='imx219', filter='IR-CUT', disperser='Nan', camera='imx219', exposure_time=10, 
                    position_angle=0,binning_x=1, binning_y=1, focal=0.085, aperture=0.06):
        """
        View SQL insert instrument
        """
        data_in = insertion.insert() 
        data_in.connect
        data_in.instrument(observation_id, name, filter, disperser, camera, exposure_time, position_angle,binning_x, binning_y, focal, aperture)
        data_in.close

    def observation(self, science_program_id:int, title='default', collection='OT_Library_UT1', proposal_pi='dtouzan@gmail.com',
                    priority=3, status=1, scheduling='1900-01-01T00:00:00', fits_file='default.fits', note_file='fits', calibration='1'):
        """
        View SQL insert observation
        """
        observation_id = 1
        data_out = selection.select() 
        data_out.connect
        id = data_out.observation_last_id[observation_id] + 1
        data_out.close
        data_in = insertion.insert() 
        data_in.connect
        data_in.observation(science_program_id, id, title, collection, proposal_pi, priority, status, scheduling, fits_file, note_file, calibration)
        data_in.close

    def collection_update(self, OT_library='OT_library_UT1', target_class='star'):
        """
        SQL function: function_collection
        Update OT library with target class
        @set: OT_library
        @set: target_class
        """
        data_in = insertion.insert() 
        data_in.connect
        data_in.function_library(OT_library, target_class)
        data_in.close       
        
    def observation_print(self,observation_id:int):
        """
        Print observation text type
        @set: observation_id
        """
        data_out = selection.select() 
        data_out.connect
        observation_data = data_out.observation_by_id(observation_id)
        scienceprogramp_id = observation_data[0]
        scienceprogram_data = data_out.scienceprogram_by_id(scienceprogramp_id)
        instrument_data = data_out.instrument_by_id(observation_id)
        target_data = data_out.target_by_id(observation_id)
        observingconditions_data = data_out.observingconditions_by_id(observation_id)
        observinglog_data = data_out.observinglog_by_id(observation_id)
        sequence_data = data_out.sequence_by_id(observation_id)
        # Header
        scienceprogram_header = data_out.scienceprogram_header[0].split(';')
        observation_header = data_out.observation_header[0].split(';')
        instrument_header = data_out.instrument_header[0].split(';')
        target_header = data_out.target_header[0].split(';')
        observingconditions_header = data_out.observingconditions_header[0].split(';')
        observinglog_header = data_out.observinglog_header[0].split(';')
        sequence_header = data_out.sequence_header[0].split(';')
        data_out.close
        
        print('# Science Program')
        for header, data in zip(scienceprogram_header, scienceprogram_data):
            if len(header) <= 7:
                tab = '\t\t\t'
            else:
                if len(header) < 15:
                    tab = '\t\t'
                else:
                    tab = '\t' 
            print(f'\t{header}{tab}: {data}')

        print('\t+ Observation')
        for header, data in zip(observation_header, observation_data):
            if header != scienceprogram_header[0]:
                if len(header) <= 7:
                    tab = '\t\t' 
                else:
                    tab = '\t'
                print(f'\t\t{header}{tab}: {data}')

        print('\t- Instrument: ')
        for header, data in zip(instrument_header, instrument_data):
            if header != observation_header[1]:
                if len(header) <= 7:
                    tab = '\t\t' 
                else:
                    tab = '\t'
                print(f'\t\t{header}{tab}: {data}')

        print('\t- Target: ')
        for header, data in zip(target_header, target_data):
            if header != observation_header[1]:
                if len(header) <= 7:
                    tab = '\t\t' 
                else:
                    tab = '\t'
                print(f'\t\t{header}{tab}: {data}')

        print('\t- Observing conditions')
        if observingconditions_data != None:
            for header, data in zip(observingconditions_header, observingconditions_data):
                if header != observation_header[1]:
                    if len(header) <= 7:
                        tab = '\t\t\t'
                    else:
                        if len(header) < 17:
                            tab = '\t\t'
                        else:
                            tab = '\t' 
                    print(f'\t\t{header}{tab}: {data}')

        print('\t- Observing log')
        if observinglog_data != None:
            for header, data in zip(observinglog_header, observinglog_data):
                if header != observation_header[1]:
                    if len(header) <= 7:
                        tab = '\t\t' 
                    else:
                        tab = '\t'
                    print(f'\t\t{header}{tab}: {data}')

        for sequence_line in sequence_data:
            header_line = '\t- Sequence'
            for header, data in zip(sequence_header,sequence_data[0]):
                if header != observation_header[1]:
                    header_line = header_line+'\t'+header+': '+str(data)
            print(header_line)
                




















