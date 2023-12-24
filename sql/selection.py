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



