#!/usr/bin/python3

###################
##    IMPORTS    ##
###################

import pyodbc
from config import MSSQLInfo
from classes.log import log

#########################
##    SQL Connector    ##
#########################
try:
    if (MSSQLInfo.DB_Server == '' or MSSQLInfo.DB_Name == '' or MSSQLInfo.DB_UserName == '' or MSSQLInfo.DB_Password == ''):
        log.warning("\n /!\ NO DATABASE CREDS \n Open the 'config.py' file and please provide the MSSQL database credentials.")
        exit(1)
    else:
        conn = pyodbc.connect(f'Driver={MSSQLInfo.DB_Driver};'
                              f'Server={MSSQLInfo.DB_Server};'
                              f'Database={MSSQLInfo.DB_Name};'
                              f'UID={MSSQLInfo.DB_UserName};'
                              f'PWD={MSSQLInfo.DB_Password};')
        MSSQL = conn.cursor()
        log.info('Connected to Database: ' + str(MSSQLInfo.DB_Server))
except Exception as e:
    log.critical("MSSQL connection error: " + str(e))
    exit(1)
# finally:
#     if (conn.is_connected()):
#         SQL.close()
#         conn.close()