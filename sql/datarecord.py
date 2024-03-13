"""
class SQLite3 select for archivage, Mast modules
"""

__authors__ = ("Dominique Touzan","ciboulette module")
__contact__ = ("dtouzan@gmail.com","https://github.com/dtouzan/ciboulette")
__copyright__ = "MIT"
__date__ = "2024-03-12"
__version__= "1.0.0"

# User mods
from ciboulette.sql import compoments, interface

class datarecords(interface.interfaces):
    filter_names = ['scienceprogram', 'observation', 'instrument', 'target', 'sequence', 'ObservingConditions', 'Observinglog']
# faire class datarecord pour la création d'une observation complète (héritage interface)
# datarecord.edit visualise les infos en fonction du filtre
# datarecord.filter paramettrer le filtre de recherche (target,observation,scienprogram....)
# datarecord.find en fonction du filter editer l'observation(s)
# datarecord.put avoir toutes les valeurs et faire les fonction
#                     sienceprogram,observation,instrument,target,sequence,observingconditions,observinglog
# datarecord.get en fonction du filter editer la valeur
# calcul du champ en recherchant et en prenant INSTRUMENT/CAMERA (à rechercher dans TABLE/camera)    
    def __init__(self):
        self.filters = datarecords.filter_names[1]
        self.value = '' # String 
    
    @property
    def edit(self):
        """
        Print observation text type
        """
        if type(self.value) == 'string' or type(self.value) != '':
            
            if self.filters == datarecords.filter_names[1]:
                self.observation_print(int(self.value))
        
            if self.filters == datarecords.filter_names[3]:
                for data in self.target_by_name(self.value):
                    self.observation_print(data['observation_id'])


