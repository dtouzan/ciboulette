"""
class Observing Conditions for SQL interface

IN PROGRESS, DO NOT USED
"""

__authors__ = ("Dominique Touzan","ciboulette module")
__contact__ = ("dtouzan@gmail.com","https://github.com/dtouzan/ciboulette")
__copyright__ = "MIT"
__date__ = "2024-03-12"
__version__= "1.0.0"

# User mods
from ciboulette.sql import compoments, interface

class conditions(interface.interfaces):

    def set(self, observation_id: int, sky_background=100, cloud_cover=20, image_quality=80, water_vapor=60, elevation_constraint=30, timming_window='night'):
        self.observingconditions(observation_id, sky_background, cloud_cover, image_quality, water_vapor, elevation_constraint, timming_window)

    def default(self, observation_id: int):
        sky_background = 90
        cloud_cover = 5
        image_quality = 90
        water_vapor = 60
        elevation_constraint = 20
        timming_window = 'night'
        self.observingconditions(observation_id, sky_background, cloud_cover, image_quality, water_vapor, elevation_constraint, timming_window)

# observing_condition_alert
# ...