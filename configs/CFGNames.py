###START ImportBlock
##systemImport
import string
import os
###FINISH ImportBlock


###START GlobalConstantBlock

#####BEGIN FilePathsBlock
ROOT_DIRECTORY = os.curdir
GLOBAL_LOG_DIR = os.path.join(ROOT_DIRECTORY, 'logs/')

#Profiler and graphs directories and files
GLOBAL_STATS_DIR = os.path.join(GLOBAL_LOG_DIR, 'stats/')

GLOBAL_PROFILE_DIR = os.path.join(GLOBAL_STATS_DIR, 'profile/')
GLOBAL_GRAPH_DIR = os.path.join(GLOBAL_STATS_DIR, 'graph/')

GLOBAL_PROFILE_FILE = os.path.join(GLOBAL_PROFILE_DIR, 'prof-data.prof')
GLOBAL_PROFILE_DOT_FILE = os.path.join(GLOBAL_PROFILE_DIR, 'prof-data.dot')

GLOBAL_GRAPH_FILE = os.path.join(GLOBAL_GRAPH_DIR, 'prof-graph.png')

#log files
GLOBAL_TEST_DIRECTORY = os.path.join(GLOBAL_LOG_DIR,'tests/')

GLOBAL_LOG_FILE = os.path.join(GLOBAL_LOG_DIR, 'LOGCommon.log')
LOCAL_NAMES_LOG_FILE = os.path.join(GLOBAL_LOG_DIR, 'LOGNames.log')
LOCAL_ANALYSIS_LOG_FILE = os.path.join(GLOBAL_LOG_DIR, 
                            'LOGAnalysis.log')
GLOBAL_TEST_LOG_FILE = os.path.join(GLOBAL_TEST_DIRECTORY, 
                        'LOGTESTCommon.log')


DB_NAMES_DIRECTORY = os.path.join(ROOT_DIRECTORY, "DBNames/")

NAMES_BASE_INITIALIZE_FILE = os.path.join(DB_NAMES_DIRECTORY,
                                "NamesBaseInitialize.cfg")
CHECK_SUM_FILE = os.path.join(DB_NAMES_DIRECTORY, "CheckSumDB.cfg")
ANALYTIC_DB_FILE = os.path.join(DB_NAMES_DIRECTORY, "DBAnalytic.cfg")
#####END FilePathsBlock

#####BEGIN FlagsBlock
DB_NAMES_FILENAME_FLAG = "DBNames"
CHECKSUM_DB_GLOBAL_FLAG = "globalExist"

#Type True to reinitialize database
ERASE_NAME_BASE_INIT_FLAG = False
#Type True to use storing in files
#or type False to use MongoDB
USING_FILE_STORING_FLAG = bool(
                            #True
                            False
)
#Type True to make unittests
MAKE_UNITTESTS_FLAG = bool(
                            True
                            #False
)
#Type True to get grofiling
MAKE_PROFILING_FLAG = bool(
                            #True
                            False
)
#####END FlagsBlock

#####BEGIN MongoengineBlock
class ME_SETTINGS():
    '''
    Contains settings for mongoengine.
    '''
    mdbUser = os.environ['mongoDBALogin']
    mdbPass = os.environ['mongoDBAPass']
    mdbCluster = os.environ['mongoDBACluster']

    MDB_n_Aliases = dict({
                'mdbName': {
                    'db_name': os.environ['mongoDBANamedb'],
                    'alias': 'mdbName'},
                'mdbAnalytic': {
                    'db_name': os.environ['mongoDBAAnlyticdb'],
                    'alias': 'mdbAnalytic'},
                'mdbCheckSum': {
                    'db_name': os.environ['mongoDBACheckSumdb'],
                    'alias': 'mdbCheckSum'}
                })
#####END MongoengineBlock

#####BEGIN FunctionalLetterVariablesBlock
ALPHABET = str(string.ascii_lowercase)
VOWELS_LETTERS = "aeiouy"
CONSONANTS_LETTERS = "bcdfghjklmnpqrstvwxz"

VOWELS_MAX_COUNT = 2
CONSONANTS_MAX_COUNT = 3
#####END FunctionalLetterVariablesBlock

#####BEGIN FunctionalGroupKeysBlock
GROUP_KEYS = [
    "Male", 
    "Female", 
    "Surnames"
]
#####END FunctionalGroupKeysBlock

#####BEGIN ClassPropertyBlock
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#####END ClassPropertyBlock

###FINISH GlobalConstantBlock

###START DecoratorBlock
###FINISH DecoratorBlock

###START FunctionalBlock
###FINISH FunctionalBlock

###START MainBlock
###FINISH Mainblock