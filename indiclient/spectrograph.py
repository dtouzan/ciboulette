# Licensed under GPL3 (see LICENSE)
# coding=utf-8

"""
Classes and utility functions for communicating with spectrograph a the INDI protocol, http://www.indilib.org.
"""

import time
import io

import logging
import logging.handlers

from .indiclient import indiclient
from ciboulette.indiclient.indisa200 import SA200Motor

log = logging.getLogger("")
log.setLevel(logging.INFO)

class SPECTROGRAPHsa200(SA200Motor):
    """
    Wrap SA200, set driver to SA200 motor, and point to localhost by default.
    """
    def __init__(self, host='localhost', port=7624):
        super(SPECTROGRAPHsa200, self).__init__(host, port, driver="SA200")
        self.filter_name = "SA200"
        self.process_events()       
          
    def shemas(self):
        from IPython.display import Image
        display(Image('ciboulette/indiclient/draw/shemas.png'))
        
    def GPIO(self):
        #from IPython.display import Image
        #display(Image('ciboulette/indiclient/draw/rpio_sa200.png'))
        print(' +-----+-----+---------+------+---+----++----+---+------+---------+-----+-----+')
        print(' | BCM | wPi |   Name  | Mode | V | Physical | V | Mode | Name    | wPi | BCM |')
        print(' +-----+-----+---------+------+---+----++----+---+------+---------+-----+-----+')
        print(' |     |     |    3.3v |      |   |  1 || 2  |   |      | 5v      |     |     |')
        print(' |   2 |   8 |   SDA.1 | ALT0 | 1 |  3 || 4  |   |      | 5v      |     |     |')
        print(' |   3 |   9 |   SCL.1 | ALT0 | 1 |  5 || 6  |   |      | 0v      |     |     |')
        print(' |   4 |   7 | GPIO. 7 |   IN | 1 |  7 || 8  | 1 | ALT5 | TxD     | 15  | 14  |')
        print(' |     |     |      0v |      |   |  9 || 10 | 1 | ALT5 | RxD     | 16  | 15  |')
        print(' |  17 |   0 | GPIO. 0 |   IN | 0 | 11 || 12 | 0 | IN   | GPIO. 1 | 1   | 18  |')
        print(' |  27 |   2 | GPIO. 2 |   IN | 0 | 13 || 14 |   |      | 0v      |     |     |')
        print(' |  22 |   3 | GPIO. 3 |   IN | 0 | 15 || 16 | 0 | IN   | GPIO. 4 | 4   | 23  |')
        print(' |     |     |    3.3v |      |   | 17 || 18 | 0 | OUT  | GPIO. 5 | 5  *| 24  |')
        print(' |  10 |  12 |    MOSI | ALT0 | 0 | 19 || 20 |   |      | 0v      |     |     |')
        print(' |   9 |  13 |    MISO | ALT0 | 0 | 21 || 22 | 0 | OUT  | GPIO. 6 | 6  *| 25  |')
        print(' |  11 |  14 |    SCLK | ALT0 | 0 | 23 || 24 | 0 | OUT  | CE0     | 10 *| 8   |')
        print(' |     |     |      0v |      |   | 25 || 26 | 0 | OUT  | CE1     | 11 *| 7   |')
        print(' |   0 |  30 |   SDA.0 |   IN | 1 | 27 || 28 | 1 | IN   | SCL.0   | 31  | 1   |')
        print(' |   5 |  21 | GPIO.21 |   IN | 1 | 29 || 30 |   |      | 0v      |     |     |')
        print(' |   6 |  22 | GPIO.22 |   IN | 1 | 31 || 32 | 0 | IN   | GPIO.26 | 26  | 12  |')
        print(' |  13 |  23 | GPIO.23 |   IN | 0 | 33 || 34 |   |      | 0v      |     |     |')
        print(' |  19 |  24 | GPIO.24 |   IN | 0 | 35 || 36 | 0 | IN   | GPIO.27 | 27  | 16  |')
        print(' |  26 |  25 | GPIO.25 |   IN | 0 | 37 || 38 | 0 | IN   | GPIO.28 | 28  | 20  |')
        print(' |     |     |      0v |      |   | 39 || 40 | 0 | IN   | GPIO.29 | 29  | 21  |')
        print(' +-----+-----+---------+------+---+----++----+---+------+---------+-----+-----+')
        print(' | BCM | wPi |   Name  | Mode | V | Physical | V | Mode | Name    | wPi | BCM |')
        print(' +-----+-----+---------+------+---+----++----+---+------+---------+-----+-----+')