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
        with open(mast_file, 'r') as file:
            reader = csv.reader(file, delimiter='\n')
            for row in reader:
                print(row[0])
                data_in.mast(scienceprogram_title, row[0])
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
       
        
                