#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
# libraries
import logging
import sys

# Log init
logging.basicConfig(level=logging.DEBUG,
                    filename="EAFpy/EAFpy.log",
                    filemode="a",
                    format='%(asctime)s - %(levelname)s - %(message)s')


logging.info(f"EAFpy Move {sys.argv[1]}  {sys.argv[2]}")
