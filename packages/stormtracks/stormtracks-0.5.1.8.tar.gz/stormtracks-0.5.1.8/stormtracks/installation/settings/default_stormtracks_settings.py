import os

SETTINGS_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.expandvars('$HOME/stormtracks_data/data')
OUTPUT_DIR = os.path.expandvars('$HOME/stormtracks_data/output')
SECOND_OUTPUT_DIR = os.path.expandvars('$HOME/stormtracks_data/output')
LOGGING_DIR = 'logs'
FIGURE_OUTPUT_DIR = os.path.expandvars('$HOME/stormtracks_data/figures')

C20_FULL_DATA_DIR = os.path.join(DATA_DIR, 'c20_full')
C20_GRIB_DATA_DIR = os.path.join(DATA_DIR, 'c20_grib')
C20_MEAN_DATA_DIR = os.path.join(DATA_DIR, 'c20_mean')
IBTRACS_DATA_DIR = os.path.join(DATA_DIR, 'ibtracs')

TRACKING_RESULTS = 'prod_release_1'
FIELD_RESULTS = 'prod_release_1'

CONSOLE_LOG_LEVEL = 'info'
FILE_LOG_LEVEL = 'debug'

CHUNK_SIZE = 1024*1000
MINIMUM_DOWNLOAD_RATE_1 = 300000 # B/s - 0.3 MB/s.
MINIMUM_DOWNLOAD_RATE_2 = 1000000 # B/s - 1 MB/s.
