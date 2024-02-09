#!/usr/bin/python3

#########################
##    SET DIRECTORY    ##
#########################

import inspect
import os
import sys

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

###################
##    IMPORTS    ##
###################

import threading
import time
import schedule

from config import MSSQLInfo, APIMethod, currentScheduleDaysFrom, dailyScheduleHistoryDays, forceTruncation, disableDateValidationCheck
from classes.server import getNextNDays, getLastNDays, validateDateRanges, listAllDates
from classes.xmlParser import xmlGetDict
from classes.log import *
from maxoptra.authentication import createSession
from maxoptra.endpointsOrders import *
from maxoptra.endpointsObjects import *
from maxoptra.endpointsSchedules import *
from db.sqlPOST import sqlPOST_GetScheduleByAOCOnDate, sqlTruncate
from functools import partial

################
##   GLOBAL   ##
################

# Get the session ID
sessionID = createSession()

################
##   ORDERS   ##
################

def APIgetOrderStatuses(orders):
    log.info('Running Task: [GetOrderStatuses]')
    try:
        return getOrderStatuses(sessionID, orders)
    except Exception as e:
        log.critical("[GetOrderStatuses] exception: " + str(e))

def APIgetOrdersWithZone(APIDate, AOCID):
    log.info('Running Task: [GetOrdersWithZone]')
    try:
        return getOrdersWithZone(sessionID, APIDate, AOCID)
    except Exception as e:
        log.critical("[GetOrdersWithZone] exception: " + str(e))

def APIgetOrdersLog(XML):
    log.info('Running Task: [GetOrdersLog]')
    try:
        return getOrdersLog(XML)
    except Exception as e:
        log.critical("[GetOrdersLog] exception: " + str(e))

#################
##   OBJECTS   ##
#################

def APIgetVehicles(APIDate):
    log.info('Running Task: [GetVehicles]')
    try:
        return getVehicles(sessionID, APIDate)
    except Exception as e:
        log.critical("[GetVehicles] exception: " + str(e))

def APIgetPerformers(APIDate, AOCID):
    log.info('Running Task: [GetPerformers]')
    try:
        return getPerformers(sessionID, APIDate, AOCID)
    except Exception as e:
        log.critical("[GetPerformers] exception: " + str(e))

def APIexportPerformers():
    log.info('Running Task: [ExportPerformers]')
    try:
        return exportPerformers(sessionID)
    except Exception as e:
        log.critical("[ExportPerformers] exception: " + str(e))

def APIexportVehicles():
    log.info('Running Task: [ExportVehicles]')
    try:
        return exportVehicles(sessionID)
    except Exception as e:
        log.critical("[ExportVehicles] exception: " + str(e))

##################
##   SCHEDULE   ##
##################

def APIgetScheduleByAOCOnDate(daily, aocID, aocName):
    log.info('Running Task: [GetScheduleByAOCOnDate]')
    try:
        if daily:
            getScheduleDate = getLastNDays(dailyScheduleHistoryDays)
            table = MSSQLInfo.DB_APIDaily
        else:
            # API Data needs to be the current date and the new date.
            getScheduleDate = getNextNDays(currentScheduleDaysFrom)
            table = MSSQLInfo.DB_APICurrent
        if forceTruncation:
            log.info(f'\'Configuration \'forceTruncation\' enabled. Forcing truncation of table \'{table}\'')
            sqlTruncate(table)
            Truncated = True
        else:
            Truncated = False
        for date in getScheduleDate:
            APIData = getScheduleByAOCOnDate(sessionID, date, aocID)
            if APIData:
                if not Truncated:
                    log.info(f'Data found for date \'{date}\'. Truncating table \'{table}\'')
                    # Truncate the table
                    sqlTruncate(table)
                APIXML = xmlGetDict(APIData)['apiResponse']['scheduleResponse']['vehicles']['vehicle']
                log.info(f'\'GetScheduleByAOCOnDate\' returned data for date \'{date}\'')
                # Update the SQL server with the new data
                sqlPOST_GetScheduleByAOCOnDate.sqlUpdate_GetScheduleByAOCOnDate(table, aocName, APIXML)
                Truncated = True
            else:
                log.info(f'\'GetScheduleByAOCOnDate\' returned null for date \'{date}\'')
            time.sleep(3)
        if not Truncated:
            log.info(
                f'No results were found whilst attempting to retrieve data from MaxOptra. No truncation of table \'{table}\' performed.')
    except Exception as e:
        log.critical("[GetScheduleByAOCOnDate] exception: " + str(e))

def APIgetScheduleByAOCOnDateRange(aocID, aocName):
    log.info('Running Task: [GetScheduleByAOCOnDate]')
    try:
        Truncated = False
        # Retrieve the date range from the SQL server
        sqlDateRange = sqlGET_ScheduleImport.sqlGetDateRange(MSSQLInfo.DB_APIDateRange)
        # Check if the dates retrieved are valid
        isValidDateRange = disableDateValidationCheck or validateDateRanges(sqlDateRange)
        if isValidDateRange:
            # Convert all dates into list
            dates = listAllDates(sqlDateRange)
            # Date range data table
            table = MSSQLInfo.DB_APIDateRangeData
            # If truncating table
            if forceTruncation:
                log.info(f'\'Configuration \'forceTruncation\' enabled. Forcing truncation of table \'{table}\'')
                sqlTruncate(table)
                Truncated = True
            for date in dates:
                APIData = getScheduleByAOCOnDate(sessionID, date, aocID)
                if APIData:
                    if not Truncated:
                        log.info(f'Data found for date \'{date}\'. Truncating table \'{table}\'')
                        # Truncate the table
                        sqlTruncate(table)
                    APIXML = xmlGetDict(APIData)['apiResponse']['scheduleResponse']['vehicles']['vehicle']
                    log.info(f'\'GetScheduleByAOCOnDate\' returned data for date \'{date}\'')
                    # Update the SQL server with the new data
                    sqlPOST_GetScheduleByAOCOnDate.sqlUpdate_GetScheduleByAOCOnDate(table, aocName, APIXML)
                    Truncated = True
                else:
                    log.info(f'\'GetScheduleByAOCOnDate\' returned null for date \'{date}\'')
                time.sleep(3)
            if not Truncated:
                log.info(
                    f'No results were found whilst attempting to retrieve data from MaxOptra. No truncation of table \'{table}\' performed.')
    except Exception as e:
        log.critical("[GetScheduleByAOCOnDate] exception: " + str(e))

########################
##    GET API DATA    ##
########################

def API_GET(daily=False, useDateRange=False):
    try:
        log.info(f'Script {os.path.basename(__file__)} started.')
        if sessionID:
            # Get the ID list of Area of Controls
            AreaOfControls = xmlGetDict(getAreaOfControls(sessionID))
            if AreaOfControls:
                AreaOfControls = AreaOfControls['apiResponse']['areaOfControlResponse']['aocs']['aoc']
                # Loop through the Area of Controls
                for aoc in AreaOfControls:
                    aocID = aoc['@id']
                    aocName = aoc['@name']
                    # If enabled go to function
                    if APIMethod.enableGetOrderStatuses:
                        #APIgetOrderStatuses(orders)
                        return
                    if APIMethod.enableGetOrdersWithZone:
                        #APIgetOrdersWithZone(APIDate, aocID)
                        return
                    if APIMethod.enableGetOrdersLog:
                        #APIgetOrdersLog(XML)
                        return
                    if APIMethod.enableGetVehicles:
                        #APIgetVehicles(APIDate)
                        return
                    if APIMethod.enableGetPerformers:
                        #APIgetPerformers(APIDate, aocID)
                        return
                    if APIMethod.enableExportPerformers:
                        #APIexportPerformers()
                        return
                    if APIMethod.enableExportVehicles:
                        #APIexportVehicles()
                        return
                    if APIMethod.enableGetScheduleByAOCOnDate:
                        if useDateRange:
                            APIgetScheduleByAOCOnDateRange(aocID, aocName)
                        else:
                            APIgetScheduleByAOCOnDate(daily, aocID, aocName)
            else:
                log.warning('The server could not retrieve any \'AreaOfControls\'. Please review the script or API configuration.')
        else:
            log.error('The session ID could not be found or created. Please review the authentication configuration credentials.')
    except Exception as e:
        log.critical("An exception occurred: " + str(e))


########################
##    AUTO SCHEDULE   ##
########################

def autoSchedule():
    log.info(f'Running \'Auto Schedule\'')
    try:
        schedule.every(60).seconds.do(API_GET)
        while True:
            schedule.run_pending()
            time.sleep(5)
    except Exception as e:
        log.critical("SCHEDULE Exception: " + str(e))

# For script schedule
def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

# RUN MAIN SCRIPT
if __name__ == '__main__':
    fileName = os.path.basename(__file__)
    if len(sys.argv) < 2:
        log.warning(f"""No arguments were provided for {fileName}. Please use one the following:
            -runDaily
            -runOnDemand            
            -runAutoSchedule
            -runDate""")
    try:
        options = \
            {
                '-runDaily': partial(API_GET, True),
                '-runOnDemand': API_GET,
                '-runAutoSchedule': autoSchedule,
                '-runDate': partial(API_GET, False, True)
            }
        options[sys.argv[1]]()
    except KeyError:
        log.error(f'No argument found for \'{sys.argv[1]}\'. Please use a valid argument.')
    log.info(f'Script {fileName} successfully finished.')