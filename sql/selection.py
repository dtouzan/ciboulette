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

    @property
    def mast(self):
        """
        MAST                  DB UT1
        -------------------   -------------------------
        intentType            scienceprogram.type
        obs_collection        observation.collection
        instrument_name       instrument.name
        filters               instrument.filter
        disperser             instrument.disperser
        target_name           target.name
        target_classification target.class
        obs_id                observation.observation_id
        s_ra                  target.ra
        s_dec                 target.dec
        proposal_pi           observation.proposal_pi
        dataproduct_type      sequence.type
        calib_level           observation.calibration
        scheduling            observation.scheduling
        t_min                 sequence.timeline_min
        t_max                 sequence.timeline_max
        t_exptime             instrument.exposure_time
        obs_title             observation.title
        focal                 instrument.camera
        format                observation.note_file
        url                   observation.fits_file
        """
        self.cursor = self.connection.cursor()
        resources = self.cursor.execute("SELECT * FROM mast_select").fetchall()
        self.cursor.close()
        return resources
