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

    def _insert_for_observation(self, sql_request:str, dataresources):
        """
        SQL insert for observation elements
        """
        self.cursor = self.connection.cursor()
        observation = self.cursor.execute("SELECT observation_id FROM observation WHERE observation_id=?", (dataresources[0],)).fetchone()
        if observation:
            # Observation_id resources
            OBS_id = observation[0]
            # SQL INSERT sequence
            self.cursor.execute(sql_request, dataresources) 
            # SQL commit to database
            self.connection.commit()           
        self.cursor.close()
        
    def mast(self,scienceprogram_title: str, mast_dataset: str):
        """
        SQL update
        @set: scienceprogram title
        @set: mast data line        
        """
        self.cursor = self.connection.cursor()
        science_program_id = self.cursor.execute("SELECT science_program_id FROM scienceprogram WHERE title=?", (scienceprogram_title,)).fetchone()
        if science_program_id:
            # Scienceprogram resources
            SP_id = science_program_id[0]
            resources = mast_dataset.split(',')
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
            focal = resources[18] 
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
            dataresources = (observation_id, instrument_name, filters, disperser, focal, exposure_time)
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

    def mast_observation_upgrade(self, observation_id: int, priority=0, statut=0, calibration=1):
        """
        SQL insert priority, statut and calibration observation for id observation
        @set: priority, statut and calibration observation      
        """
        sql_request = """UPDATE observation SET priority=?,statut=?,calibration=? WHERE observation_id=?;"""
        dataresources = (priority, statut, calibration, observation_id)
        self._insert_for_observation(sql_request, dataresources)

    def mast_observation_title(self, observation_id: int, title_observation='Observation with UT1'):
        """
        SQL insert title observation for id observation
        @set: title observation   
        """
        sql_request = """UPDATE observation SET title=?  WHERE observation_id=?;"""
        dataresources = (title_observation, observation_id)
        self._insert_for_observation(sql_request, dataresources)

    def mast_target_note(self, observation_id: int, notes=''):        
        """
        SQL insert note target for id observation
        @set: note target   
        """
        sql_request = """UPDATE target SET notes=?  WHERE observation_id=?;"""
        dataresources = (notes, observation_id)
        self._insert_for_observation(sql_request, dataresources)

    def mast_instrument_upgrade(self, observation_id: int, binning_x=1, binning_y=1, aperture=0.30):        
        """
        SQL insert binning and aperture for id observation
        @set: binning, aperture    
        """
        sql_request = """UPDATE instrument SET binning_x=?,binning_y=?,aperture=? WHERE observation_id=?;"""
        dataresources = (binning_x, binning_y, aperture, observation_id)
        self._insert_for_observation(sql_request, dataresources)

    def mast_instrument_camera(self, observation_id: int, camera='nefertiti3199-imx477'):        
        """
        SQL insert camera for id observation
        @set: camera name
        """ 
        sql_request = """UPDATE instrument SET camera=?  WHERE observation_id=?;"""
        dataresources = (camera, observation_id)
        self._insert_for_observation(sql_request, dataresources)
        
    def scienceprogram(self, title: str, status=1, contact='dtouzan@gmail.com', observing_time=0, type_SP='science', dataset='dataset/archives'):
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
            dataresources = (title,status,contact,observing_time,type_SP,dataset)
            self.cursor.execute(sql, dataresources)             
            # SQL commit to database
            self.connection.commit()
            self.cursor.close()
        else:
            self.cursor.close()
            return False

    def close_scienceprogram(self, scienceprogram_title: str):
        """
        SQL close science program, status = 0
        @set: scienceprogram_title
        """
        self.cursor = self.connection.cursor()
        science_program_id = self.cursor.execute("SELECT science_program_id FROM scienceprogram WHERE title=?", (scienceprogram_title,)).fetchone()
        if science_program_id:
            # SQLupdate scienceprogram status
            sql = """UPDATE scienceprogram SET status=0  WHERE science_program_id=?;"""
            dataresources = science_program_id
            self.cursor.execute(sql, dataresources)          
            # SQL commit to database
            self.connection.commit()
            self.cursor.close()
        else:
            self.cursor.close()
            return False        

    def sequence(self, observation_id: int, title='sequence', label='001', sequence_type='light', timeline_min=0, timeline_max=0, compoment='None'):
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
        sql_request = """INSERT INTO sequence(observation_id,title,label,type,timeline_min,timeline_max,compoment) VALUES(?,?,?,?,?,?,?);"""
        dataresources = (observation_id, title, label, sequence_type, timeline_min, timeline_max, compoment)
        self._insert_for_observation(sql_request, dataresources)
               
    def target(self, observation_id:int, name:'default', class_type:'default', RA=0.0, DEC=0.0, notes='default'):
        """
        SQL insert target
        @set: observation_id
        @set: name
        @set: class_type
        @set: RA
        @set: DEC
        @set: notes     
        """
        sql_request = """INSERT INTO target(observation_id,name,class,RA,DEC,notes) VALUES(?,?,?,?,?,?);"""
        dataresources = (observation_id, name, class_type, RA, DEC, notes)
        self._insert_for_observation(sql_request, dataresources)
        
    def observinglog(self, observation_id:int, label='default', filename='default_observinglog.txt', comment='default observing log file'):
        """
        SQL insert observinglog
        @set: observation_id
        @set: label
        @set: filename
        @set: comment  
        """
        sql_request = """INSERT INTO observinglog(observation_id,label,filename,comment) VALUES(?,?,?,?);"""
        dataresources = (observation_id, label, filename, comment)
        self._insert_for_observation(sql_request, dataresources)

    def observingconditions(self, observation_id:int, sky_background=100, cloud_cover=20, image_quality=80, water_vapor=60, elevation_constraint=30, 
                            timming_window='night'):
        """
        SQL insert observingconditions
        @set: observation_id
        @set: sky_background
        @set: cloud_cover
        @set: image_quality
        @set: water_vapor
        @set: elevation_constraint
        @set: timming_window
        """
        sql_request = """INSERT INTO observingconditions(observation_id,sky_background,cloud_cover,image_quality,\
                                    water_vapor,elevation_constraint,timming_window) VALUES(?,?,?,?,?,?,?);"""
        dataresources = (observation_id, sky_background, cloud_cover, image_quality, water_vapor, elevation_constraint, timming_window)
        self._insert_for_observation(sql_request, dataresources)

    def instrument(self, observation_id:int, name:str, instrument_filter:str, disperser:str, camera:str, exposure_time:float, 
                    position_angle:float,binning_x:int, binning_y:int, focal:float, aperture:float):
        """
        SQL insert instrument
        @set: observation_id
        @set: name
        @set: filter
        @set: disperser
        @set: camera
        @set: exposure_time
        @set: position_angle
        @set: binning_x
        @set: binning_y
        @set: focal
        @set: aperture
        """
        sql_request = """INSERT INTO instrument(observation_id,name,filter,disperser,\
                                    camera,exposure_time,position_angle,binning_x,\
                                    binning_y,focal,aperture) VALUES(?,?,?,?,?,?,?,?,?,?,?);"""
        dataresources = (observation_id, name, instrument_filter, disperser, camera, exposure_time, position_angle, binning_x, binning_y, focal, aperture)
        self._insert_for_observation(sql_request, dataresources)
 
    def observation(self, science_program_id:int, observation_id:int, title='default', collection='OT_Library_UT1', proposal_pi='dtouzan@gmail.com',
                    priority=3, status=1, scheduling='1900-01-01T00:00:00', fits_file='default.fits', note_file='fits', calibration='1'):
        """
        SQL insert observation
        @set: science_program_id
        @set: observation_id
        @set: title
        @set: collection
        @set: proposal_pi
        @set: priority
        @set: status
        @set: scheduling
        @set: fits_file
        @set: note_file
        @set: calibration
        """
        sql_request = """INSERT INTO observation(science_program_id,observation_id,title,collection,proposal_pi,\
                                    priority,status,scheduling,fits_file,note_file,calibration) VALUES(?,?,?,?,?,?,?,?,?,?,?);"""
        dataresources = (science_program_id, observation_id, title, collection, proposal_pi, priority, status, scheduling, fits_file, note_file, calibration)
        self.cursor = self.connection.cursor()
        self.cursor.execute(sql_request, dataresources)             
        # SQL commit to database
        self.connection.commit()
        self.cursor.close()

    def function_library(self, OT_library='OT_library_UT1', target_class='star'):
        """
        SQL function: select function_library(OT_library,target_class)
            update observation set collection=? where observation.observation_id in 
            (select observation.OBSERVATION_ID from target join observation where target.OBSERVATION_ID=observation.OBSERVATION_ID and target.CLASS=?)
        @set: OT_library
        @set: target_class
        """
        sql_request = """update observation set collection=? where observation.observation_id in\
                        (select observation.OBSERVATION_ID from target join observation where\
                        target.OBSERVATION_ID=observation.OBSERVATION_ID and target.CLASS=?)"""
        dataresources = (OT_library, target_class)
        self.cursor = self.connection.cursor()
        self.cursor.execute(sql_request, dataresources)
        self.connection.commit()
        self.cursor.close()







