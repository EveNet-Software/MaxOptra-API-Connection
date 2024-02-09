#!/usr/bin/python3

###################
##    IMPORTS    ##
###################

from classes.server import getAPIData
from config import URL

####################################
##    Connection API Endpoints    ##
####################################

def startRequest(sessionID, aocID, startDate, isSchedulingCollections):
    return getAPIData(URL.startRequest, {'sessionID': sessionID, 'aocID': aocID, 'startDate': startDate, 'isSchedulingCollections': isSchedulingCollections })

def stopRequest(sessionID, aocID, startDate, isSchedulingCollections):
    return getAPIData(URL.startRequest, {'sessionID': sessionID, 'aocID': aocID, 'startDate': startDate, 'isSchedulingCollections': isSchedulingCollections })

def statusRequest(sessionID, aocID, startDate, isSchedulingCollections):
    return getAPIData(URL.startRequest, {'sessionID': sessionID, 'aocID': aocID, 'startDate': startDate, 'isSchedulingCollections': isSchedulingCollections })