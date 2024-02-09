#!/usr/bin/python3

###################
##    IMPORTS    ##
###################

from datetime import date

################################
##    Script Configuration    ##
################################

debugMode = False
disableSilentMode = True
disableModuleCheck = False
disableSafeCheck = False
disableDateValidationCheck = False

# Number of days the system will look forward from the current date
currentScheduleDaysFrom = 5
# Number of days the system will go back from the current/start date
dailyScheduleHistoryDays = 60
# Force truncation of table, even if data is not found
forceTruncation = False

###################################
##    LOG FILE NAME & LOCATION   ##
###################################

logFileName = f'system{date.today()}.log'

####################################
##    Authentication Parameters   ##
####################################

# Credentials for Authentication
APIcredentials = {
    'accountID' : 'USER_accountID', # Maxoptra Account Id
    'user' : 'USER_EMAIL_ADDRESS',  # Maxoptra Username
    'password' : 'USER_PASSWORD'    # Maxoptra Password
}

###########################
##    MSSQL Parameters   ##
###########################

class MSSQLInfo:
    DB_Driver =             'ODBC Driver 17 for SQL Server'
    DB_Server =             'localhost'
    DB_Name =               'DB_NAME'
    DB_UserName =           'DB_USERNAME'
    DB_Password =           'DB_PASSWORD'
    DB_Trusted_Connection = 'yes'

    # Name of API table for 'Request Daily'
    DB_APIDaily = ''
    # Name of API table for 'Request Current'
    DB_APICurrent = ''
    # Name of API table for 'Saved data to upload'
    DB_APISave = ''
    # Name of API table for 'Date Range Data'
    DB_APIDateRangeData = ''
    # Name of API table for 'Request Data from Date Range' (START DATE & END DATE)
    DB_APIDateRange = ''
    DB_APIDateRange_ColumnStartDateName = ''
    DB_APIDateRange_ColumnEndDateName = ''

######################################
##    Enable/Disable API methods    ##
######################################

class APIMethod:
    ### ORDERS: METHODS ###
    enableSave                   = True
    enableDelete                 = False
    enableGetOrderStatuses       = False
    enableGetOrdersWithZone      = False
    enableGetOrdersLog           = False

    ### OBJECTS: METHODS ###
    enableGetVehicles            = False
    enableGetVehiclesByAoc       = False
    enableGetPerformers          = False
    enableGetSchedulingZones     = False
    enableExportPerformers       = False
    enableExportVehicles         = False

    ### SCHEDULE: METHODS ###
    enableScheduleImport         = False
    enableGetScheduleByAOCOnDate = True

    ### SCHEDULE: AUTOSCHEDULING ###
    enableStart                  = True
    enableStop                   = False
    enableStatus                 = False

#########################
##    URL Pramaters    ##
#########################

class URL:
    ### Base API URL
    APIrestURL =                                ''
    ### Session Authentication URL
    createSessionURL = APIrestURL +             'authentication/createSession'

    ### ORDERS: URL ###
    ordersURL = APIrestURL +                    'distribution-api/orders/'
    postOrderSaveURL = ordersURL +              'save'
    getOrderStatusesURL = ordersURL +           'getOrderStatuses'
    getOrdersWithZoneURL = ordersURL +          'getOrdersWithZone'
    getOrdersLogURL = ordersURL +               'getOrdersLog'
    ### OBJECTS: URL ###
    objectsURL = APIrestURL +                   'distribution-api/objects/'
    getAreaOfControlsURL = objectsURL +         'getAreaOfControls'
    getVehiclesURL = objectsURL +               'getVehicles'
    getVehiclesByAocURL = objectsURL +          'getVehiclesByAoc'
    getPerformersURL = objectsURL +             'getPerformers'
    getSchedulingZonesURL = objectsURL +        'getSchedulingZones'
    exportPerformersURL = objectsURL +          'exportPerformers'
    exportVehiclesURL = objectsURL +            'exportVehicles'
    ### SCHEDULE: URL ###
    scheduleURL = APIrestURL +                  'distribution-api/schedules/'
    getScheduleByAOCOnDateURL = scheduleURL +   'getScheduleByAOCOnDate'
    ### AUTOSCHEDULING: URL ###
    autoschedulingURL = APIrestURL +            'distribution-api/schedules/'
    startRequest = autoschedulingURL +          'start'
    stopRequest = autoschedulingURL +           'stop'
    statusRequest = autoschedulingURL +         'status'
