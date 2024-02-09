#!/usr/bin/python3

###################
##    IMPORTS    ##
###################

from classes.server import getAPIData, getAPIDataXML, postAPIData
from config import URL

####################################
##    Connection API Endpoints    ##
####################################

def saveOrder(XML):
    postAPIData(URL.postOrderSaveURL, XML, 'saveOrder')

def deleteOrder(sessionID):
    # ORDER HERE
    return

def getOrderStatuses(sessionID, orders):
    return getAPIData(URL.getOrderStatusesURL, {'sessionID' : sessionID, 'orders' : orders})

def getOrdersWithZone(sessionID, date, aocID):
    return getAPIData(URL.getOrdersWithZoneURL, {'sessionID' : sessionID, 'date' : date, 'aocID' : aocID})

def getOrdersLog(XML):
    return getAPIDataXML(URL.getOrdersLogURL, XML)