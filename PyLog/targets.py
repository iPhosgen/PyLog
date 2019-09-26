import logging

import graypy

targets = {'file': logging.FileHandler,
           'graylog': graypy.GELFUDPHandler}