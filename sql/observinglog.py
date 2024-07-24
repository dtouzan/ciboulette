"""
class Observing Log for SQL interface

IN PROGRESS, DO NOT USED
"""

__authors__ = ("Dominique Touzan","ciboulette module")
__contact__ = ("dtouzan@gmail.com","https://github.com/dtouzan/ciboulette")
__copyright__ = "MIT"
__date__ = "2024-03-12"
__version__= "1.0.0"

# User mods
from ciboulette.sql import compoments, interface

class log(interface.interfaces):

    def set(self, observation_id: int):
        label = 'log_' + str(observation_id)
        filename = 'observinglog_' + str(observation_id) + '.txt'
        comment = str(observation_id) + ' observing log file'
        self.observinglog(observation_id, label, filename, comment)

    def default(self, observation_id: int):
        label = 'log_' + str(observation_id)
        filename = 'None'
        comment = 'default'
        self.observinglog(observation_id, label, filename, comment)

# observing_log_alert
# ...