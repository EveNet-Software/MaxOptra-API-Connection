#!/usr/bin/python3

########################
##    Module Check    ##
########################

def checkRequiredModules():
    if not disableModuleCheck:
        try:
            import requests
            import schedule
            import pyodbc
            import xmltodict
            import dict2xml
            return True
        except:
            log.error('\nOne or more of the required modules is not installed. The following must be installed:'
                '\n- requests'
                '\n- schedule'
                '\n- pyodbc'
                '\n- xmltodict'
                '\n- dict2xml'        
                '\nUse: \'pip3 install module_name\' to install the missing module.')
            exit(0)

###################
##    IMPORTS    ##
###################

import requests, locale
from datetime import datetime, timedelta
from config import disableSafeCheck, disableModuleCheck, dailyScheduleHistoryDays
from classes.log import log
from classes.xmlParser import xmlResponseCheck, xmlResponseLog
from db.connector import MSSQL

################
##    MAIN    ##
################

def scriptArguments():
    return [
        '-runDaily',
        '-runOnDemand',
        '-runAutoSchedule',
        '-runDate'
    ]

#########################
##    API RESPONSES    ##
#########################

# Get Request API responses
def getAPIData(url, prams):
    try:
        if not (prams):
            log.warning(__name__ + ' One or more the required parameters was left blank.' + str(prams))
        else:
            response = requests.post(url, params=prams)
            if URLCheck(__name__, response):
                return response.text
    except Exception as e:
        log.critical("An exception occurred:" + str(e))

# Get Request API responses
def getAPIDataXML(url, xml):
    try:
        if not (xml):
            log.warning(__name__ + ' One or more the required parameters was left blank.' + str(xml))
        else:
            response = requests.post(url, data=xml.encode('utf-8'), headers={'Content-Type': 'application/xml; charset=UTF-8'})
            if URLCheck(__name__, response):
                return response.text
    except Exception as e:
        log.critical("An exception occurred:" + str(e))

####################
##    API POST    ##
####################

# Get Request API responses
def postAPIData(url, xml, type):
    try:
        if not (xml):
            log.warning(__name__ + ' One or more the required parameters was left blank.' + str(xml))
        else:
            response = requests.post(url, data=xml.encode('utf-8'), headers={'Content-Type': 'application/xml; charset=UTF-8'})
            if URLCheck(__name__, response):
                xmlResponseLog(response.text, type)
    except Exception as e:
        log.critical("An exception occurred:" + str(e))


#######################
##    SQL to JSON    ##
#######################

def db2json(query, one=False):
    MSSQL.execute(query)
    r = [dict((MSSQL.description[i][0], value) \
               for i, value in enumerate(row)) for row in MSSQL.fetchall()]
    MSSQL.connection.close()
    return (r[0] if r else None) if one else r

######################
##    DATE/TIME     ##
######################

def getCurrentDate(days=None):
    if days:
        date = datetime.today() + timedelta(days=days)
    else:
        date = datetime.today()
    return date.strftime('%d/%m/%Y')

def getNextNDays(days=None):
    date = datetime.today()
    dateRange = [date + timedelta(days=x) for x in range(days)]
    dateList = []
    for dates in dateRange:
        dateList.append(dates.strftime('%d/%m/%Y'))
    return dateList

def getLastNDays(days=None):
    date = datetime.today()
    dateRange = [date - timedelta(days=x) for x in range(days)]
    dateList = []
    for dates in dateRange:
        dateList.append(dates.strftime('%d/%m/%Y'))
    return dateList

def date2SQLFormat(date):
    try:
        if date:
            return datetime.strptime(date, '%d/%m/%Y')
    except Exception as e:
        log.critical(f"Exception thrown whilst attempting to convert datetime '{date}': " + str(e))

def dateTime2SQLFormat(date):
    try:
        if date:
            return datetime.strptime(date, '%d/%m/%Y %H:%M')
    except Exception as e:
        log.critical(f"Exception thrown whilst attempting to convert datetime '{date}': " + str(e))

def time2SQLFormat(time):
    if time:
        try:
            timeInt = int(time)
        except ValueError:
            log.error(f"An error occurred whilst attempting to convert the time '{time}' into an integer.")
            return
    else:
        return
    try:
        return datetime.fromtimestamp(timeInt).time()
    except Exception as e:
        log.critical(f"Exception thrown whilst attempting to convert datetime '{time}': " + str(e))


def listAllDates(date_ranges):
    all_dates = []
    # Set the locale to en_GB to ensure UK date formatting
    locale.setlocale(locale.LC_TIME, 'en_GB')
    for start_date_str, end_date_str in date_ranges:
        start_date = datetime.strptime(start_date_str, '%d/%m/%Y')
        end_date = datetime.strptime(end_date_str, '%d/%m/%Y')
        current_date = start_date
        while current_date <= end_date:
            all_dates.append(current_date.strftime('%d/%m/%Y'))
            current_date += timedelta(days=1)
    return all_dates

######################
##    VALIDATION    ##
######################

# Check that a status code 200 is returned
def URLCheck(func_name, response):
    if not disableSafeCheck:
        if response.status_code == 200:
            if xmlResponseCheck(response.text):
                return True
        else:
            log.error(f'Connection error occurred in {func_name}. Server responded with: {response.status_code}')
            exit(0)
    else:
        return True

def validateDateFormat(date_str):
    try:
        datetime.strptime(date_str, '%d/%m/%Y')
        return True
    except ValueError:
        log.error(f'Error validating format of date. Date string \'{date_str}\' is not a valid type.')
        return False

def validateDateRanges(date_ranges):
    seen_ranges = set()
    # Loop through date ranges
    for start_date, end_date in date_ranges:
        # Check date format
        if not (validateDateFormat(start_date) and validateDateFormat(end_date)):
            return False

        # Check start date not greater than end date
        if start_date > end_date:
            log.error(f'Start date \'{start_date}\' cannot be greater than end date \'{end_date}\'.')
            return False

        # Check the number of days between dates
        days_difference = (datetime.strptime(end_date, '%d/%m/%Y') - datetime.strptime(start_date, '%d/%m/%Y')).days
        if days_difference > dailyScheduleHistoryDays:
            log.error(f'Date range should not exceed {dailyScheduleHistoryDays} days.')
            return False

        # Check for conflicts with previous date ranges
        # current_range = set(range(datetime.strptime(start_date, '%d/%m/%Y').toordinal(),
        #                           datetime.strptime(end_date, '%d/%m/%Y').toordinal() + 1))
        current_range = frozenset(range(datetime.strptime(start_date, '%d/%m/%Y').toordinal(),
                                        datetime.strptime(end_date, '%d/%m/%Y').toordinal() + 1))
        conflicting_ranges = [existing_range for existing_range in seen_ranges if current_range.intersection(existing_range)]
        if conflicting_ranges:
            conflicting_ranges_str = ', '.join([f'({datetime.fromordinal(min(conflict_range))} to {datetime.fromordinal(max(conflict_range))})' for conflict_range in conflicting_ranges])
            log.error(f'Date ranges should not conflict with each other. Conflicting ranges: {conflicting_ranges_str}')
            return False
        # Add range of dates if no conflict
        seen_ranges.add(current_range)
    return True