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


class insert(compoments.compoment):
    """
    SQL insert class
    """

    def mast(self,scienceprogram_title: str, mast_dataset: str):
        """
        SQL update
        @set: scienceprogram title
        @set: mast data line        
        """
        self.cursor = self.connection.cursor()
        science_program_id = self.cursor.execute("SELECT science_program_id FROM scienceprogram WHERE title=?", (scienceprogram,)).fetchone()
        if science_program_id:
            # Scienceprogram resources
            SP_id = science_program_id[0]
            resources = dataset.split(',')
            # Observation resources
            observation_id = int(resources[7])
            collection = resources[1]
            proposal_pi = resources[10]
            calib_level = int(resources[12])
            scheduling = resources[13]
            obs_title = resources[17]
            format = resources[19]
            url = resources[20]
            # Instrument resources
            instrument_name = resources[2]  
            filters = resources[3]  
            disperser = resources[4]
            exposure_time = float(resources[16])
            camera = resources[18] 
            # Target resources
            target_name = resources[5]
            target_class = resources[6]
            s_ra = float(resources[8])
            s_dec = float(resources[9])
            # Sequence resources
            sequence_type = resources[11] 
            timeline_min = float(resources[14])
            timeline_max = float(resources[15]) 
    
            # SQL INSERT observatoire
            sql = """INSERT INTO observation(science_program_id,observation_id,collection,proposal_pi,calibration,scheduling,title,note_file,fits_file) VALUES(?,?,?,?,?,?,?,?,?);"""
            dataresources = (SP_id, observation_id, collection, proposal_pi, calib_level, scheduling, obs_title, format, url)
            self.cursor.execute(sql, dataresources) 

            # SQL INSERT instrument
            sql = """INSERT INTO instrument(observation_id,name,filter,disperser,camera,exposure_time) VALUES(?,?,?,?,?,?);"""
            dataresources = (observation_id, instrument_name, filters, disperser, camera, exposure_time)
            self.cursor.execute(sql, dataresources) 

            # SQL INSERT target
            sql = """INSERT INTO target(observation_id,name,class,ra,dec) VALUES(?,?,?,?,?);"""
            dataresources = (observation_id, target_name, target_class, s_ra, s_dec)
            self.cursor.execute(sql, dataresources) 

            # SQL INSERT sequence
            sql = """INSERT INTO sequence(observation_id,type,timeline_min,timeline_max) VALUES(?,?,?,?);"""
            dataresources = (observation_id, sequence_type, timeline_min, timeline_max)
            self.cursor.execute(sql, dataresources) 

            # SQL commit to database
            self.connection.commit()           
        self.cursor.close()

    def scienceprogram(self, title: str, status=1, contact='dtouzan@gmail.com', observing_time=0, type='science', dataset='dataset/archives'):
        """
        SQL insert scienceprogram
        @set: scienceprogram title
        @set: mast data line        
        """
        self.cursor = self.connection.cursor()
        science_program_id = self.cursor.execute("SELECT science_program_id FROM scienceprogram WHERE title=?", (title,)).fetchone()
        if not science_program_id:
            # SQL INSERT scienceprogram
            sql = """INSERT INTO scienceprogram(title,status,contact,observing_time,type,dataset) VALUES(?,?,?,?,?,?);"""
            dataresources = (title,status,contact,observing_time,type,dataset)
            self.cursor.execute(sql, dataresources) 
            
            # SQL commit to database
            self.connection.commit()
        else:
            return False

    def sequence(self, observation_id: int, title='sequence', label='001', type='light', timeline_min=0, timeline_max=0, compoment='None'):
        """
        SQL insert sequence
        @set: observation_id
        @set: title
        @set: label
        @set: type
        @set: timeline_min
        @set: timeline_max
        @set: compoment       
        """
        self.cursor = self.connection.cursor()
        observation = self.cursor.execute("SELECT observation_id FROM observation WHERE observation_id=?", (observation_id,)).fetchone()
        if observation:
            # Observation_id resources
            OBS_id = observation[0]
            # SQL INSERT sequence
            sql = """INSERT INTO sequence(observation_id,title,label,type,timeline_min,timeline_max,compoment) VALUES(?,?,?,?,?,?,?);"""
            dataresources = (OBS_id, title, label, type, timeline_min, timeline_max, compoment)
            self.cursor.execute(sql, dataresources) 

            # SQL commit to database
            self.connection.commit()           
        self.cursor.close()
        

















