__author__ = 'teemu kanstren'

#log into mysql? you can use create_db.sql file to create the schema
MYSQL_ENABLED = False
#log directly into elasticsearch (over the network)
ES_NW_ENABLED = True
#log to file using elasticsearch bulk format
ES_FILE_ENABLED = False
#log into a file using CSV format
CSV_ENABLED = True
#print log data to console (CSV/ES only)
PRINT_CONSOLE = False
KAFKA_ENABLED = False

#host address for mysql server
MYSQL_HOST = "localhost"
#username for mysql db
MYSQL_USER = "pypro"
#password for mysql db
MYSQL_PW = "omg-change-this-pw"
#mysql db name
MYSQL_DB = "pypro_db"

#elasticsearch server host address
ES_HOST = "localhost"
#elasticsearch host server port
ES_PORT = 9200

#name of the data collection session
SESSION_NAME = "session1"
#name of the elasticsearch index to write logs into
DB_NAME = "tbd"

KAFKA_SERVER = "localhost:9092"
KAFKA_TOPIC = "pypro"
#target of measurement identifier
TOM = "host1"

#polling interval. this is the time the poller sleeps between reading and writing values.
INTERVAL = 1

#list of processes to poll. process names or ids. "-" to poll no processes, "*" to poll all processes.
PROCESS_LIST = ["*"]
