import os

# ElasticSearch cluster host
ELASTICSEARCH_HOST = "elasticsearch"

# Minimal line length used to check repetition
MINIMAL_LINE_LENGTH = 25

# Jaccard threshold value
JACCARD_THRESHOLD_VALUE = 0.45

# Image hamming threshold value
IMAGE_HAMMING_THRESHOLD_VALUE = 0.8

# DICER2 Storage path
DICER2_STORAGE_PATH = "store"

# Document checking job processing number
JOB_PROCESSING_NUM = os.cpu_count()

# Enable CORS
ENABLE_CORS = True

# Enable error traceback display
ENABLE_ERROR_TRACEBACK = True

# Job result ensure_ascii
ENSURE_ASCII = True

# Search precision: The number of valid results for each line of searches
SEARCH_PRECISION = 5

# MySQL database uri 
def get_db_uri(dbinfo):
    engine = dbinfo.get("ENGINE")
    driver = dbinfo.get("DRIVER")
    user = dbinfo.get("USER")
    password = dbinfo.get("PASSWORD")
    host = dbinfo.get("HOST")
    port = dbinfo.get("PORT")
    name = dbinfo.get("NAME")

    return "{}+{}://{}:{}@{}:{}/{}".format(engine, driver, user, password, host, port, name)

dbinfo = {
        "ENGINE": "mysql",
        "DRIVER": "pymysql",
        "USER": "root",
        "PASSWORD": "hadoop",
        "HOST": "localhost",
        "PORT": "3306",
        "NAME": "FlaskAPI"
    }

SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)
