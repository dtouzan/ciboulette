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
        self.cursor = self.connection.cursor()
        resources = self.cursor.execute("SELECT * FROM mast_select").fetchall()
        self.cursor.close()
        return resources

    @property
    def mast_header(self):
        """
        SQL view mast_header
        @return: data of mast header
        """
        self.cursor = self.connection.cursor()
        resources = self.cursor.execute("SELECT * FROM mast_header").fetchone()
        self.cursor.close()        
        return resources

    @property
    def filter_header(self):
        """
        SQL view filter_header
        @return: data of filter header
        """
        self.cursor = self.connection.cursor()
        resources = self.cursor.execute("SELECT * FROM filter_header").fetchone()
        self.cursor.close()        
        return resources