#!/usr/bin/python3

###################
##    IMPORTS    ##
###################

from config import debugMode, MSSQLInfo
from classes.log import log
from classes.server import date2SQLFormat, dateTime2SQLFormat, time2SQLFormat
from db.connector import conn, MSSQL

def sqlTruncate(table):
    sqlQuery = f"TRUNCATE TABLE [{MSSQLInfo.DB_Name}].[dbo].[{table}];"
    MSSQL.execute(sqlQuery)
    conn.commit()
    if debugMode:
        log.debug(f'Server executed SQL query: {sqlQuery}')

class sqlPOST_GetScheduleByAOCOnDate:
    ###################
    ##    GLOBALS    ##
    ###################

    distributionCentreName = 'distributionCentreName'
    orderReference = 'orderReference'
    sequenceNumber = 'sequenceNumber'
    customerLocationName = 'customerLocationName'
    contactNumber = 'contactNumber'
    customerLocationAddress = 'customerLocationAddress'
    additionalInstructions = 'additionalInstructions'
    driverName = 'driverName'
    vehicleName = 'vehicleName'
    factArrivalTime = 'factArrivalTime'
    factDepartureTime = 'factDepartureTime'
    planArrivalTime = 'planArrivalTime'
    planDepartureTime = 'planDepartureTime'
    estimatedArrivalTime = 'estimatedArrivalTime'
    estimatedDepartureTime = 'estimatedDepartureTime'
    factDrivingTime = 'factDrivingTime'
    factDuration = 'factDuration'
    factMileage = 'factMileage'
    planDrivingTime = 'planDrivingTime'
    planMileage = 'planMileage'
    capacity = 'capacity'
    bowakref = 'bowakref'
    runDay = 'runDay'
    runNumber = 'runNumber'

    def __init__(self):
        self.sqlDict = {self.distributionCentreName: []
        ,self.orderReference: []
        ,self.sequenceNumber: []
        ,self.customerLocationName: []
        ,self.contactNumber: []
        ,self.customerLocationAddress: []
        ,self.additionalInstructions: []
        ,self.driverName: []
        ,self.vehicleName: []
        ,self.factArrivalTime: []
        ,self.factDepartureTime: []
        ,self.planArrivalTime: []
        ,self.planDepartureTime: []
        ,self.estimatedArrivalTime: []
        ,self.estimatedDepartureTime: []
        ,self.factDrivingTime: []
        ,self.factDuration: []
        ,self.factMileage: []
        ,self.planDrivingTime: []
        ,self.planMileage: []
        ,self.capacity: []
        ,self.bowakref: []
        ,self.runDay: []
        ,self.runNumber: []}

        self.DATAdistributionCentreName = ''
        self.DATAorderReference = ''
        self.DATAsequenceNumber = ''
        self.DATAcustomerLocationName = ''
        self.DATAcontactNumber = ''
        self.DATAcustomerLocationAddress = ''
        self.DATAadditionalInstructions = ''
        self.DATAdriverName = ''
        self.DATAvehicleName = ''
        self.DATAfactArrivalTime = ''
        self.DATAfactDepartureTime = ''
        self.DATAplanArrivalTime = ''
        self.DATAplanDepartureTime = ''
        self.DATAestimatedArrivalTime = ''
        self.DATAestimatedDepartureTime = ''
        self.DATAfactDrivingTime = ''
        self.DATAfactDuration = ''
        self.DATAfactMileage = ''
        self.DATAplanDrivingTime = ''
        self.DATAplanMileage = ''
        self.DATAcapacity = ''
        self.DATAbowakref = ''
        self.DATArunDay = ''
        self.DATArunNumber = ''

    #@staticmethod
    def updateVeriables(self):
        aoc = sqlPOST_GetScheduleByAOCOnDate()
        self.sqlDict[aoc.distributionCentreName].append(self.DATAdistributionCentreName)
        self.sqlDict[aoc.orderReference].append(self.DATAorderReference)
        self.sqlDict[aoc.sequenceNumber].append(self.DATAsequenceNumber)
        self.sqlDict[aoc.customerLocationName].append(self.DATAcustomerLocationName)
        self.sqlDict[aoc.contactNumber].append(self.DATAcontactNumber)
        self.sqlDict[aoc.customerLocationAddress].append(self.DATAcustomerLocationAddress)
        self.sqlDict[aoc.additionalInstructions].append(self.DATAadditionalInstructions)
        self.sqlDict[aoc.driverName].append(self.DATAdriverName)
        self.sqlDict[aoc.vehicleName].append(self.DATAvehicleName)
        self.sqlDict[aoc.factArrivalTime].append(self.DATAfactArrivalTime)
        self.sqlDict[aoc.factDepartureTime].append(self.DATAfactDepartureTime)
        self.sqlDict[aoc.planArrivalTime].append(self.DATAplanArrivalTime)
        self.sqlDict[aoc.planDepartureTime].append(self.DATAplanDepartureTime)
        self.sqlDict[aoc.estimatedArrivalTime].append(self.DATAestimatedArrivalTime)
        self.sqlDict[aoc.estimatedDepartureTime].append(self.DATAestimatedDepartureTime)
        self.sqlDict[aoc.factDrivingTime].append(self.DATAfactDrivingTime)
        self.sqlDict[aoc.factDuration].append(self.DATAfactDuration)
        self.sqlDict[aoc.factMileage].append(self.DATAfactMileage)
        self.sqlDict[aoc.planDrivingTime].append(self.DATAplanDrivingTime)
        self.sqlDict[aoc.planMileage].append(self.DATAplanMileage)
        self.sqlDict[aoc.capacity].append(self.DATAcapacity)
        self.sqlDict[aoc.bowakref].append(self.DATAbowakref)
        self.sqlDict[aoc.runDay].append(self.DATArunDay)
        self.sqlDict[aoc.runNumber].append(self.DATArunNumber)

    def sqlPrepare_GetScheduleByAOCOnDate(self, aocName, data):
        try:
            # If not a list, make into a list
            if not isinstance(data, list):
                data = [data]
            for row in data:
                self.DATAdistributionCentreName = aocName
                self.DATAdriverName = row.get('@driverName')
                self.DATAvehicleName = row.get('@name')

                ##### NESTED: RUN #####
                if ('run' in row):
                    run = row.get('run')
                    # If not a list, make into a list
                    if not isinstance(run, list):
                        run = [run]
                    for Rrow in run:
                        self.DATArunDay = date2SQLFormat(Rrow.get('@runDay'))
                        self.DATArunNumber = Rrow.get('@runNumber')

                        ##### NESTED: LOCATION #####
                        if ('location' in Rrow):
                            location = Rrow.get('location')
                            # If not a list, make into a list
                            if not isinstance(location, list):
                                location = [location]
                            for Lrow in location:
                                self.DATAsequenceNumber = Lrow.get('@number')
                                self.DATAcustomerLocationName = Lrow.get('@name')
                                self.DATAcustomerLocationAddress = Lrow.get('@address')
                                self.DATAfactArrivalTime = dateTime2SQLFormat(Lrow.get('@factArrivalTime'))
                                self.DATAfactDepartureTime = dateTime2SQLFormat(Lrow.get('@factDepartureTime'))
                                self.DATAplanArrivalTime = dateTime2SQLFormat(Lrow.get('@planArrivalTime'))
                                self.DATAplanDepartureTime = dateTime2SQLFormat(Lrow.get('@planDepartureTime'))
                                self.DATAestimatedArrivalTime = dateTime2SQLFormat(Lrow.get('@estimatedArrivalTime'))
                                self.DATAestimatedDepartureTime = dateTime2SQLFormat(Lrow.get('@estimatedDepartureTime'))
                                self.DATAfactDrivingTime = time2SQLFormat(Lrow.get('@factDrivingTime'))
                                self.DATAfactDuration = time2SQLFormat(Lrow.get('@factDuration'))
                                self.DATAfactMileage = Lrow.get('@factMileage')
                                self.DATAplanDrivingTime = time2SQLFormat(Lrow.get('@planDrivingTime'))
                                self.DATAplanMileage = Lrow.get('@planMileage')

                                ##### NESTED: ORDER #####
                                if ('order' in Lrow):
                                    order = Lrow.get('order')
                                    # If not a list, make into a list
                                    if not isinstance(order, list):
                                        order = [order]
                                    for Orow in order:
                                        self.DATAorderReference = Orow.get('@orderReference')
                                        self.DATAcontactNumber = Orow.get('@contactNumber')
                                        self.DATAadditionalInstructions = Orow.get('@additionalInstructions')
                                        self.DATAcapacity = Orow.get('@weight')
                                        self.DATAbowakref = Orow.get('@bowakref')
                                        sqlPOST_GetScheduleByAOCOnDate.updateVeriables(self)
                                else:
                                    self.DATAorderReference = ''
                                    self.DATAcontactNumber = ''
                                    self.DATAadditionalInstructions = ''
                                    self.DATAcapacity = ''
                                    self.DATAbowakref = ''
                                    sqlPOST_GetScheduleByAOCOnDate.updateVeriables(self)
                        else:
                            self.DATAsequenceNumber = ''
                            self.DATAcustomerLocationName = ''
                            self.DATAcustomerLocationAddress = ''
                            self.DATAfactArrivalTime = ''
                            self.DATAfactDepartureTime = ''
                            self.DATAplanArrivalTime = ''
                            self.DATAplanDepartureTime = ''
                            self.DATAestimatedArrivalTime = ''
                            self.DATAestimatedDepartureTime = ''
                            self.DATAfactDrivingTime = ''
                            self.DATAfactDuration = ''
                            self.DATAfactMileage = ''
                            self.DATAplanDrivingTime = ''
                            self.DATAplanMileage = ''
                            self.DATAorderReference = ''
                            self.DATAcontactNumber = ''
                            self.DATAadditionalInstructions = ''
                            self.DATAcapacity = ''
                            self.DATAbowakref = ''
                            sqlPOST_GetScheduleByAOCOnDate.updateVeriables(self)
                else:
                    self.DATAsequenceNumber = ''
                    self.DATAcustomerLocationName = ''
                    self.DATAcustomerLocationAddress = ''
                    self.DATAfactArrivalTime = ''
                    self.DATAfactDepartureTime = ''
                    self.DATAplanArrivalTime = ''
                    self.DATAplanDepartureTime = ''
                    self.DATAestimatedArrivalTime = ''
                    self.DATAestimatedDepartureTime = ''
                    self.DATAfactDrivingTime = ''
                    self.DATAfactDuration = ''
                    self.DATAfactMileage = ''
                    self.DATAplanDrivingTime = ''
                    self.DATAplanMileage = ''
                    self.DATAorderReference = ''
                    self.DATAcontactNumber = ''
                    self.DATAadditionalInstructions = ''
                    self.DATAcapacity = ''
                    self.DATAbowakref = ''
                    self.DATArunDay = ''
                    self.DATArunNumber = ''
                    sqlPOST_GetScheduleByAOCOnDate.updateVeriables(self)
            return self.sqlDict
        except Exception as e:
            log.critical("An exception occurred: " + str(e))

    @staticmethod
    def sqlUpdate_GetScheduleByAOCOnDate(table, aocName, data):
        aoc = sqlPOST_GetScheduleByAOCOnDate()
        sqlData = aoc.sqlPrepare_GetScheduleByAOCOnDate(aocName, data)
        try:
            placeholders = ', '.join(['?'] * len(sqlData))
            columns = ', '.join(sqlData.keys())
            sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % (f'[{MSSQLInfo.DB_Name}].[dbo].[{table}]', columns, placeholders)
            for i in range(len(sqlData[aoc.distributionCentreName])):
                updateData = (sqlData[aoc.distributionCentreName][i]
                              ,sqlData[aoc.orderReference][i]
                              ,sqlData[aoc.sequenceNumber][i]
                              ,sqlData[aoc.customerLocationName][i]
                              ,sqlData[aoc.contactNumber][i]
                              ,sqlData[aoc.customerLocationAddress][i]
                              ,sqlData[aoc.additionalInstructions][i]
                              ,sqlData[aoc.driverName][i]
                              ,sqlData[aoc.vehicleName][i]
                              ,sqlData[aoc.factArrivalTime][i]
                              ,sqlData[aoc.factDepartureTime][i]
                              ,sqlData[aoc.planArrivalTime][i]
                              ,sqlData[aoc.planDepartureTime][i]
                              ,sqlData[aoc.estimatedArrivalTime][i]
                              ,sqlData[aoc.estimatedDepartureTime][i]
                              ,sqlData[aoc.factDrivingTime][i]
                              ,sqlData[aoc.factDuration][i]
                              ,sqlData[aoc.factMileage][i]
                              ,sqlData[aoc.planDrivingTime][i]
                              ,sqlData[aoc.planMileage][i]
                              ,sqlData[aoc.capacity][i]
                              ,sqlData[aoc.bowakref][i]
                              ,sqlData[aoc.runDay][i]
                              ,sqlData[aoc.runNumber][i])
                MSSQL.execute(sql, updateData)
            conn.commit()
            if debugMode:
                log.debug(f'Server executed SQL query: {sql}')
        except Exception as e:
            log.critical("An exception occurred: " + str(e))