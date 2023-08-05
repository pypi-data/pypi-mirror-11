__author__ = 'teemu kanstren'

import pypro.local.main
import pypro.local.config as config

config.MYSQL_HOST = "192.168.2.79"
config.MYSQL_ENABLED = False

config.SESSION_NAME = "session2"
config.DB_NAME = "session1"
config.ES_HOST = "192.168.2.79"
config.ES_NW_ENABLED = True
config.ES_FILE_ENABLED = True
config.CSV_ENABLED = False
config.KAFKA_ENABLED = False
config.KAFKA_TOPIC = "session2"
config.KAFKA_SERVER = "192.168.2.153"
config.PRINT_CONSOLE = True

config.INTERVAL = 1

#config.PROCESS_LIST = ["iperf"]

pypro.local.main.run_poller()




