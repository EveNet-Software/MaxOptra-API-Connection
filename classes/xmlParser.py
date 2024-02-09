#!/usr/bin/python3

###################
##    IMPORTS    ##
###################

import xmltodict
from dict2xml import dict2xml
from xml.etree import ElementTree as ET
from classes.log import log

######################
##    VALIDATION    ##
######################

def xmlResponseCheck(xml):
    try:
        root = ET.fromstring(xml)
        for item in root.iter('error'):
            errorCode = item.find('errorCode').text
            errorMessage = item.find('errorMessage').text
            if float(errorCode) > 1019:
                log.warning(f'[GET] MaxOptra API response with message: [{errorMessage}]')
            else:
                log.error(f'MaxOptra API response with: [Error Code: {errorCode}] [Error Message: {errorMessage}]')
                log.warning('The script detected an error code in the API response within the \'Common API errors\' table. Script terminated.')
                exit(0)
            return False
        return True
    except Exception as e:
        log.critical("An exception occurred: " + str(e))

def xmlResponseLog(xml, type):
    try:
        root = ET.fromstring(xml)
        for item in root.iter('order'):
            orderReference = item.find('orderReference').text
            status = item.find('status').text
            if status:
                log.info(f'MaxOptra API response for \'{type}\' : [orderReference : {orderReference}] [status : {status}]')
            else:
                log.warning('The script detected an error code in the API response within the \'Common API errors\' table. Script terminated.')
    except Exception as e:
        log.critical("An exception occurred: " + str(e))

###########################
##    Return XML Data    ##
###########################

def xmlTree(data):
    try:
        return ET.ElementTree(ET.fromstring(data))
    except Exception as e:
        log.critical("An exception occurred: " + str(e))

def xmlResponse(xml, find):
    try:
        xmldata = xml.findall('*/{search}'.format(search=find))
        if xmldata:
            return str(xmldata[0].text)
        else:
            log.warning(f'Cannot find \'{find}\' in {xml}. Returned null.')
            return
    except Exception as e:
        log.critical("An exception occurred: " + str(e))

def xmlGetDict(xml):
    if xml:
        return xmltodict.parse(xml, force_list={'aoc'})

###########################################
##    Covert Python dictionary to XML    ##
###########################################

def xmlDict2xml(data):
    xml = dict2xml(data, wrap="all", indent="  ")
    return xml

def xmlSaveHardCode(data):
    xmlSaveString = ""