"""
class SQLite3 for archivage, Mast modules
"""

__authors__ = ("Dominique Touzan","ciboulette module")
__contact__ = ("dtouzan@gmail.com","https://github.com/dtouzan/ciboulette")
__copyright__ = "MIT"
__date__ = "2023-12-08"
__version__= "1.0.0"

# Globals mods
import sqlite3

class compoment:
    
    def __init__(self):
        self.db = 'ciboulette/db/UT1.db'
        self.connection = None
        self.cursor = None

    @property
    def connect(self):
        self.connection = sqlite3.connect(self.db)

    @property
    def database(self):
        self.cursor = self.connection.cursor()
        resources = self.cursor.execute("SELECT name,release FROM database").fetchone()
        self.cursor.close()
        return resources
    
    @property
    def close(self):
        self.connection.close()

        