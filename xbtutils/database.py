import sqlite3 as sql
from .decode import xbtBinaryClass
import json


# add xbt object to database, create tables if these don't exist
def xbt_add_to_database(xbt, dbfile):
    # create database if doesn't exist
    conn = sql.connect(dbfile)
    dbc = conn.cursor()

    # Enable use of foreign keys to link tables
    dbc.execute("PRAGMA foreign_keys = ON")

    # CREATE MAIN TABLE
    # create main table and link to secondary tables with secondary keys
    CREATE_MAIN_TABLE = "CREATE TABLE IF NOT EXISTS main( " \
                        "fileName TEXT PRIMARY KEY, latitude FLOAT, longitude FLOAT, datetime TEXT, " \
                        "shipSpeed FLOAT, shipDirection INT, totalWaterDepth INT, launchHeight INT, probeSerial INT, " \
                        "soopLine TEXT, transectNumber INT, sequenceNumber INT, seasVersion INT, msgType INT," \
                        "callSign TEXT, agencyCode INT, launcherCode INT, probeCode INT, recorderCode INT, riderName TEXT, " \
                        "FOREIGN KEY(callSign) REFERENCES vessel(callSign), " \
                        "FOREIGN KEY(agencyCode) REFERENCES agency(code)," \
                        "FOREIGN KEY(launcherCode) REFERENCES launcher(code)" \
                        "FOREIGN KEY(probeCode) REFERENCES probe(code), " \
                        "FOREIGN KEY(recorderCode) REFERENCES recorder(code), " \
                        "FOREIGN KEY(riderName) REFERENCES rider(name) )"
    dbc.execute(CREATE_MAIN_TABLE)
    # CREATE SECONDARY TABLES
    # create vessel table
    CREATE_VESSEL_TABLE = "CREATE TABLE IF NOT EXISTS vessel (callSign TEXT PRIMARY KEY, IMO INT, shipName TEXT)"
    dbc.execute(CREATE_VESSEL_TABLE)
    # create agency table
    CREATE_AGENCY_TABLE = "CREATE TABLE IF NOT EXISTS agency (code INT PRIMARY KEY, name TEXT)"
    dbc.execute(CREATE_AGENCY_TABLE)
    # create launcher table
    CREATE_LAUNCHER_TABLE = "CREATE TABLE IF NOT EXISTS launcher (code INT PRIMARY KEY, name TEXT)"
    dbc.execute(CREATE_LAUNCHER_TABLE)
    # create probe table # self.code = code, self.coefA = coefA, self.coefB = coefB, self.maxDepth = maxDepth, self.name = name, self.serial = serial >> not unique goes to main table
    CREATE_PROBE_TABLE = "CREATE TABLE IF NOT EXISTS probe (code INT PRIMARY KEY, name TEXT, coefA FLOAT, coefB FLOAT, maxDepth INT)"
    dbc.execute(CREATE_PROBE_TABLE)
    # create recorder table
    CREATE_RECORDER_TABLE = "CREATE TABLE IF NOT EXISTS recorder (code INT PRIMARY KEY, name TEXT, frequency INT)"
    dbc.execute(CREATE_RECORDER_TABLE)
    # create rider table
    CREATE_RIDER_TABLE = "CREATE TABLE IF NOT EXISTS rider (name TEXT PRIMARY KEY, email TEXT, phone TEXT, institution TEXT)"
    dbc.execute(CREATE_RIDER_TABLE)
    # create depth, temperature table
    CREATE_SAMPLES_TABLE = "CREATE TABLE IF NOT EXISTS samples (fileName TEXT PRIMARY KEY, dataPoints INT, data TEXT, FOREIGN KEY(fileName) REFERENCES main(fileName))"
    dbc.execute(CREATE_SAMPLES_TABLE)

    # INSERT VALUES >> order matters: if using a foreign reference in another table, these values need to be populated beforehand in the secondary table
    INSERT_TO_VESSEL_TABLE = "INSERT OR IGNORE INTO vessel VALUES(?,?,?)"    
    dbc.execute(INSERT_TO_VESSEL_TABLE, (xbt.vessel.callSign, xbt.vessel.imo, xbt.vessel.shipName))

    INSERT_TO_AGENCY_TABLE = "INSERT OR IGNORE INTO agency VALUES(?,?)"    
    dbc.execute(INSERT_TO_AGENCY_TABLE, (xbt.agency.code, xbt.agency.name))    
    
    INSERT_TO_LAUNCHER_TABLE = "INSERT OR IGNORE INTO launcher VALUES(?,?)"    
    dbc.execute(INSERT_TO_LAUNCHER_TABLE, (xbt.gear.launcher.code, xbt.gear.launcher.name))   
    
    INSERT_TO_PROBE_TABLE = "INSERT OR IGNORE INTO probe VALUES(?,?,?,?,?)"      
    dbc.execute(INSERT_TO_PROBE_TABLE, (xbt.gear.probe.code, xbt.gear.probe.name, xbt.gear.probe.coefA, xbt.gear.probe.coefB, xbt.gear.probe.maxDepth))  

    INSERT_TO_RECORDER_TABLE = "INSERT OR IGNORE INTO recorder VALUES(?,?,?)"    
    dbc.execute(INSERT_TO_RECORDER_TABLE, (xbt.gear.recorder.code, xbt.gear.recorder.name, xbt.gear.recorder.frequency))   

    INSERT_TO_RIDER_TABLE = "INSERT OR IGNORE INTO rider VALUES(?,?,?,?)"    
    dbc.execute(INSERT_TO_RIDER_TABLE, (xbt.rider.name, xbt.rider.email, xbt.rider.phone, xbt.rider.institution)) 

    # main has foreign keys that need to be populated in the origin tables before inserting the references into main
    INSERT_TO_MAIN_TABLE = "INSERT OR IGNORE INTO main VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)" # 20 entries    
    dbc.execute(INSERT_TO_MAIN_TABLE, (xbt.fileName, xbt.vessel.latitude, xbt.vessel.longitude, xbt.profileDatetime.dtString,
                                       xbt.vessel.shipSpeed, xbt.vessel.shipDirection, xbt.vessel.totalWaterDepth, xbt.vessel.launchHeight,
                                       xbt.gear.probe.serial, xbt.line.soopLine, xbt.line.transectNumber, xbt.line.sequenceNumber,
                                       xbt.gear.seasVersion, xbt.msgType,
                                       xbt.vessel.callSign, xbt.agency.code, xbt.gear.launcher.code, xbt.gear.probe.code, 
                                       xbt.gear.recorder.code, xbt.rider.name) ) 

    # # option 1: new table with one item per row >>  10 items, 1204 kB db
    # CREATE_SAMPLES_TABLE_1 = "CREATE TABLE IF NOT EXISTS samples (depth FLOAT, temperature FLOAT, fileName TEXT, FOREIGN KEY(fileName) REFERENCES main(fileName))"
    # INSERT_TO_SAMPLES_TABLE_1 = "INSERT OR IGNORE INTO samples VALUES(?,?,?)"
    # dbc.execute(CREATE_SAMPLES_TABLE_1)
    # # insert values to table one row at a time
    # for i in range(len(xbt.profile.temperatures)):
    #     dbc.execute(INSERT_TO_SAMPLES_TABLE, (xbt.profile.depths[i], xbt.profile.temperatures[i], xbt.fileName))
    # option 2: new table with json row with data >> 10 items, 268 kB
    samples = { "depth": xbt.profile.depths, "temperature": xbt.profile.temperatures }
    json_samples = json.dumps(samples) # convert back to list later using json.loads(json_samples)    
    # samples has a foreign key (filename) that needs to be populated before inserting new values in samples
    INSERT_TO_SAMPLES_TABLE = "INSERT OR IGNORE INTO samples VALUES(?,?,?)"    
    dbc.execute(INSERT_TO_SAMPLES_TABLE, (xbt.fileName, xbt.profile.dataPoints, json_samples))    
    # print("> File:",xbt.fileName)
    # print(json.loads(json_samples)["temperature"][0]) # get surface temperature

    # save changes to database and close
    conn.commit()
    conn.close()



    
def read_database(dbfile):
    conn = sql.connect(dbfile)
    dbc = conn.cursor()

    # res = dbc.execute("SELECT main.fileName FROM main JOIN vessel ON main.callSign = vessel.callSign")
    # res = dbc.execute("SELECT * FROM main JOIN vessel USING (callSign)")
    res = dbc.execute("SELECT main.fileName,main.latitude,main.longitude,main.callSign,vessel.shipName,agency.name FROM main JOIN vessel ON main.callSign = vessel.callSign JOIN agency ON main.agencyCode = agency.code WHERE main.callSign = ? ", ("3E3535",))
    # print(res.fetchall())
    for row in res:
        print(row)


    conn.close()

def read_database_profile(dbfile):
    conn = sql.connect(dbfile)
    dbc = conn.cursor()
    res = dbc.execute("SELECT main.fileName,main.callSign,samples.dataPoints,samples.data FROM main JOIN samples ON main.fileName = samples.fileName")
    for row in res:
        print("> dataPoints:", row[2])
        t = json.loads(row[3])["temperature"]        
        print("> List length:", len(t), "Printing list values:\r\n" , t)
    conn.close()
    