"""
class SQLite3 select for archivage, Mast modules
"""

__authors__ = ("Dominique Touzan","ciboulette module")
__contact__ = ("dtouzan@gmail.com","https://github.com/dtouzan/ciboulette")
__copyright__ = "MIT"
__date__ = "2023-12-08"
__version__= "1.0.0"

# User mods
from ciboulette.sql import compoments


class select(compoments.compoment):
    """
    SQL select class
    """

    def _selectall(self, sql_request: str):
        self.cursor = self.connection.cursor()
        resources = self.cursor.execute(sql_request).fetchall()
        self.cursor.close()
        return resources

    def _selectone(self, sql_request: str):
        self.cursor = self.connection.cursor()
        resources = self.cursor.execute(sql_request).fetchone()
        self.cursor.close()
        return resources


    @property
    def mast(self):
        """
        SQL view mast_select
        @return: mast records
        
        MAST                  DB UT1
        -------------------   -------------------------
        intentType            scienceprogram.type          0
        obs_collection        observation.collection       1
        instrument_name       instrument.name              2  
        filters               instrument.filter            3  
        disperser             instrument.disperser         4
        target_name           target.name                  5
        target_classification target.class                 6
        obs_id                observation.observation_id   7
        s_ra                  target.ra                    8
        s_dec                 target.dec                   9
        proposal_pi           observation.proposal_pi      10  
        dataproduct_type      sequence.type                11 
        calib_level           observation.calibration      12
        scheduling            observation.scheduling       13 
        t_min                 sequence.timeline_min        14  
        t_max                 sequence.timeline_max        15 
        t_exptime             instrument.exposure_time     16
        obs_title             observation.title            17
        focal                 instrument.camera            18 
        format                observation.note_file        19 
        url                   observation.fits_file        20  
        """
        resources = self._selectall("SELECT * FROM mast_select")
        return resources

    @property
    def mast_last_id(self):
        """
        Export vue mast_last_id 
        """
        resources = self._selectone("SELECT * FROM observation_last_id") 
        return resources
    
    @property
    def mast_header(self):
        """
        SQL view mast_header
        @return: data of mast header
        """
        resources = self._selectone("SELECT * FROM mast_header")    
        return resources

    @property
    def filter_header(self):
        """
        SQL view filter_header
        @return: data of filter header
        """
        resources = self._selectone("SELECT * FROM filter_header")
        return resources

    @property
    def camera_header(self):
        """
        SQL view camera_header
        @return: data of camera header
        """
        resources = self._selectone("SELECT * FROM camera_header")
        return resources

    @property
    def observation_table_header(self):
        """
        SQL view observation_table_header
        @return: data of observation table header
        """
        resources = self._selectone("SELECT * FROM observation_table_header")
        return resources

    @property
    def scienceprogram(self):
        """
        SQL view scienceprogram_select
        @return: data of scienceprogram
        """
        resources = self._selectall("SELECT * FROM scienceprogram_select")
        return resources

    @property
    def collection(self):
        """
        SQL view collection_select
        @return: data of collection
        """
        resources = self._selectall("SELECT * FROM collection_select")
        return resources

    @property
    def scheduling_last(self):
        """
        SQL view date_last
        @return: last date of observation
        """
        resources = self._selectall("SELECT * FROM scheduling_last")
        return resources

    @property
    def scienceprogram_type_header(self):
        """
        SQL view scienceprogram_type_header
        @return: scienceprogram type header
        """
        resources = self._selectone("SELECT * FROM scienceprogram_type_header")
        return resources

    @property
    def scienceprogram_header(self):
        """
        SQL view scienceprogram_header
        @return: scienceprogram header
        """
        resources = self._selectone("SELECT * FROM scienceprogram_header")
        return resources
    
    def scienceprogram_observing_time(self, scienceprogram_title:str):
        """
        @return: all sequences of scienceprogram title
        @set: science program title
        """
        self.cursor = self.connection.cursor()
        science_program_id = self.cursor.execute("SELECT science_program_id FROM scienceprogram WHERE title=?", (scienceprogram_title,)).fetchone()
        if science_program_id:
            sql_request = "SELECT timeline_min,\
                                  timeline_max \
                                  FROM sequence,observation \
                                  WHERE observation.observation_id=sequence.observation_id \
                                  AND observation.science_program_id=? \
                                  ORDER BY sequence.timeline_min"
            resources = self.cursor.execute(sql_request, science_program_id).fetchall()
        self.cursor.close()
        return resources

    @property
    def scienceprogram_title(self):
        """
        SQL view scienceprogram_title
        @return: sciencprogram title list
        """
        resources = self._selectall("SELECT * FROM scienceprogram_title")
        return resources

    def scienceprogram_by_id(self, science_program_id:int):
        """
        @return: scienceprogram data for science program id
        @set: science_program_id
        """
        self.cursor = self.connection.cursor()
        resources = self.cursor.execute("SELECT * FROM scienceprogram WHERE science_program_id=?", (science_program_id,)).fetchone()
        self.cursor.close()
        return resources

    def scienceprogram_by_title(self, scienceprogram_title:str):
        """
        @return: scienceprogram data for the title
        @set: scienceprogram title
        """
        self.cursor = self.connection.cursor()
        resources = self.cursor.execute("SELECT * FROM scienceprogram WHERE title=?", (scienceprogram_title,)).fetchone()
        self.cursor.close()
        return resources

    def instrument_exposure_time(self, scienceprogram_title:str):
        """
        @return: scienceprogram sum exposure time
        @set: scienceprogram title
        """
        self.cursor = self.connection.cursor()
        science_program_id = self.cursor.execute("SELECT science_program_id FROM scienceprogram WHERE title=?", (scienceprogram_title,)).fetchone()
        if science_program_id:
            sql_request = "SELECT exposure_time FROM instrument,observation \
                                  WHERE observation.observation_id=instrument.observation_id \
                                  AND observation.science_program_id=?"
            resources = self.cursor.execute(sql_request, science_program_id).fetchall()
        self.cursor.close()
        return resources

    @property
    def observation_last_id(self):
        """
        @return: observation last id 
        """
        resources = self._selectone("SELECT * FROM observation_last_id")
        return resources
        
    def observation_by_id(self, id:int):
        """
        @return: observation data by id (dict)
        @set: observation id
        """
        self.cursor = self.connection.cursor()
        resources = self.cursor.execute("SELECT * FROM observation WHERE observation_id=?", (id,)).fetchone()
        self.cursor.close()
        return resources

    def observation_by_collection(self, collection:str):
        """
        @return: observation data by collection (dict)
        @set: collection name
        """
        resources = list()
        dataset = self.collection
        self.cursor = self.connection.cursor()
        for data in dataset:
            if collection in data[0]:
                 resources = self.cursor.execute("SELECT * FROM observation WHERE collection=?", (data[0],)).fetchall()
        self.cursor.close()
        return resources

    def observation_by_title(self, observation_title:str):
        """
        @return: observation data by title (dict)
        @set: observation title
        """
        resources = list()
        title = '%' + observation_title + '%'
        self.cursor = self.connection.cursor()
        resources = self.cursor.execute("SELECT * FROM observation WHERE title LIKE ?", (title,)).fetchall()
        self.cursor.close()
        return resources

    def observation_by_scheduling(self, observation_scheduling:str):
        """
        @return: observation data by scheduling (dict)
        @set: observation scheduling, AAAA-MM-DD 
        """
        resources = list()
        scheduling = '%' + observation_scheduling + '%'
        self.cursor = self.connection.cursor()
        resources = self.cursor.execute("SELECT * FROM observation WHERE scheduling LIKE ?", (scheduling,)).fetchall()
        self.cursor.close()
        return resources

    def observation_by_notes(self, observation_notes:str):
        """
        @return: observation data by notes (dict)
        @set: observation notes
        """
        resources = list()
        notes = '%' + observation_notes + '%'
        self.cursor = self.connection.cursor()
        resources = self.cursor.execute("SELECT * FROM observation WHERE note_file LIKE ?", (notes,)).fetchall()
        self.cursor.close()
        return resources

    @property
    def observation_header(self):
        """
        SQL view observation_header
        @return: observation header
        """
        resources = self._selectone("SELECT * FROM observation_header")
        return resources

    def sequence_by_id(self, id:int):
        """
        @return: sequence data by id (dict)
        @set: sequence id
        """
        self.cursor = self.connection.cursor()
        resources = self.cursor.execute("SELECT * FROM sequence WHERE observation_id=?", (id,)).fetchall()
        self.cursor.close()
        return resources

    @property
    def sequence_header(self):
        """
        SQL view sequence_header
        @return: sequence header
        """
        resources = self._selectone("SELECT * FROM sequence_header")
        return resources

    def instrument_by_id(self, id:int):
        """
        @return: instrument data by id (dict)
        @set: instrument id
        """
        self.cursor = self.connection.cursor()
        resources = self.cursor.execute("SELECT * FROM instrument WHERE observation_id=?", (id,)).fetchone()
        self.cursor.close()
        return resources

    def instrument_by_name(self, instrument_name:str):
        """
        @return: instrument data by name (dict)
        @set: instrument name
        """
        self.cursor = self.connection.cursor()
        resources = self.cursor.execute("SELECT * FROM instrument WHERE name=?", (instrument_name,)).fetchall()
        self.cursor.close()
        return resources

    def instrument_by_filter(self, instrument_filter:str):
        """
        @return: instrument data by filter (dict)
        @set: instrument filter
        """
        self.cursor = self.connection.cursor()
        resources = self.cursor.execute("SELECT * FROM instrument WHERE filter=?", (instrument_filter,)).fetchall()
        self.cursor.close()
        return resources

    def instrument_by_disperser(self, instrument_disperser:str):
        """
        @return: instrument data by disperser (dict)
        @set: instrument disperser
        """
        self.cursor = self.connection.cursor()
        resources = self.cursor.execute("SELECT * FROM instrument WHERE disperser=?", (instrument_disperser,)).fetchall()
        self.cursor.close()
        return resources

    def instrument_by_camera(self, instrument_camera:str):
        """
        @return: instrument data by camera (dict)
        @set: instrument camera
        """
        self.cursor = self.connection.cursor()
        resources = self.cursor.execute("SELECT * FROM instrument WHERE camera=?", (instrument_camera,)).fetchall()
        self.cursor.close()
        return resources

    @property
    def instrument_header(self):
        """
        SQL view instrument_header
        @return: instrument header
        """
        resources = self._selectone("SELECT * FROM instrument_header")
        return resources

    def target_by_id(self, id:int):
        """
        @return: target data by id (dict)
        @set: target id
        """
        self.cursor = self.connection.cursor()
        resources = self.cursor.execute("SELECT * FROM target WHERE observation_id=?", (id,)).fetchone()
        self.cursor.close()
        return resources

    def target_by_name(self, name:str):
        """
        @return: target data by name (dict)
        @set: target id
        """
        term = (f'%{name}%',)
        self.cursor = self.connection.cursor()
        resources = self.cursor.execute("SELECT * FROM target WHERE name LIKE ?", term).fetchall()
        self.cursor.close()
        return resources

    def target_by_notes(self, notes:str):
        """
        @return: target data by bnotes (dict)
        @set: target notes
        """
        term = (f'%{notes}%',)
        self.cursor = self.connection.cursor()
        resources = self.cursor.execute("SELECT * FROM target WHERE notes LIKE ?", term).fetchall()
        self.cursor.close()
        return resources

    @property
    def target_header(self):
        """
        SQL view target_header
        @return: target header
        """
        resources = self._selectone("SELECT * FROM target_header")
        return resources

    def observinglog_by_id(self, id:int):
        """
        @return: observinglog data by id (dict)
        @set: observinglog id
        """
        self.cursor = self.connection.cursor()
        resources = self.cursor.execute("SELECT * FROM observinglog WHERE observation_id=?", (id,)).fetchone()
        self.cursor.close()
        return resources

    @property
    def observinglog_header(self):
        """
        SQL view observinglog_header
        @return: observinglog header
        """
        resources = self._selectone("SELECT * FROM observinglog_header")
        return resources

    def observingconditions_by_id(self, id:int):
        """
        @return: observingconditions data by id (dict)
        @set: observingconditions id
        """
        self.cursor = self.connection.cursor()
        resources = self.cursor.execute("SELECT * FROM observingconditions WHERE observation_id=?", (id,)).fetchone()
        self.cursor.close()
        return resources

    @property
    def observingconditions_header(self):
        """
        SQL view observingconditions_header
        @return: observingconditions header
        """
        resources = self._selectone("SELECT * FROM observingconditions_header")
        return resources

    def camera_by_name(self, camera_name:str):
        """
        @return: camera data by camera (dict)
        @set: camera name
        """
        self.cursor = self.connection.cursor()
        resources = self.cursor.execute("SELECT * FROM camera WHERE name=?", (camera_name,)).fetchone()
        self.cursor.close()
        return resources

    def filter_by_name(self, filter_name:str):
        """
        @return: filter data by filter (dict)
        @set: filter name
        """
        self.cursor = self.connection.cursor()
        resources = self.cursor.execute("SELECT * FROM filter WHERE name=?", (filter_name,)).fetchone()
        self.cursor.close()
        return resources

    @property
    def filter_data_iso_header(self):
        """
        SQL view filter_data_iso_header
        @return: filter_data_iso header
        """
        resources = self._selectone("SELECT * FROM filter_data_iso_header")
        return resources

    def disperser_by_name(self, disperser_name:str):
        """
        @return: disperser data by disperser (dict)
        @set: disperser name
        """
        self.cursor = self.connection.cursor()
        resources = self.cursor.execute("SELECT * FROM disperser WHERE name=?", (disperser_name,)).fetchone()
        self.cursor.close()
        return resources

    @property
    def disperser_header(self):
        """
        SQL view disperser_header
        @return: disperser header
        """
        resources = self._selectone("SELECT * FROM disperser_header")
        return resources

    @property
    def skychart_header(self):
        """
        SQL view skychart_header
        @return: skychart header
        """
        resources = self._selectone("SELECT * FROM skychart_header")
        return resources

    @property
    def skychart_values(self):
        """
        SQL view skychart_value
        @return: target list and observation.title list 
        """
        resources = self._selectall("SELECT * FROM skychart_values")
        return resources














        