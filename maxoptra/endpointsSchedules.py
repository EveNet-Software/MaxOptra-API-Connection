#!/usr/bin/python3

###################
##    IMPORTS    ##
###################

from classes.server import getAPIData
from config import URL
from db.sqlGET import sqlGET_ScheduleImport

####################################
##    Connection API Endpoints    ##
####################################

def getScheduleByAOCOnDate(sessionID, date, aocID):
    return getAPIData(URL.getScheduleByAOCOnDateURL, {
        'sessionID': sessionID,
        'date': date,
        'aocID': aocID
    })

def postScheduleImport(sessionID):
    return sqlGET_ScheduleImport.sqlPrepare_ScheduleImport('t_APIGetScheduleRequest_Current')