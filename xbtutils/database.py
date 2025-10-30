import sqlite3 as sql
from .decode import xbtBinaryClass
from .xbt_plots import plot_profile
from .utilities import print_dictionary_list, xbt_export_json, export_text_to_file
import json
import os


# add xbt object to database, create tables if these don't exist
def xbt_add_to_database(xbt, dbfile):
    print(f"> Adding {xbt.fileName} to {dbfile}...")
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


# prints each table with corresponding columns
def list_database_tables(dbfile):
    print("\r\n> Listing tables and columns...\r\n")
    conn = sql.connect(dbfile)
    dbc = conn.cursor() 
    # get tables in database
    res = dbc.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")

    tables = [row[0] for row in res.fetchall()]    
    # list columns in each table
    for table in tables:        
        table_res = dbc.execute(f"SELECT * FROM {table}")
        columns = []
        for col in table_res.description:
            columns.append(col[0])
        print("> Table:",table, ", Columns:",columns)
    
    conn.close()

       


# reads all tables and columns from the data base, specifying number of entries to print    
def read_database_all(dbfile, limit=10):
    conn = sql.connect(dbfile)
    dbc = conn.cursor()
    # res = dbc.execute("SELECT main.fileName FROM main JOIN vessel ON main.callSign = vessel.callSign")
    # res = dbc.execute("SELECT * FROM main JOIN vessel USING (callSign)")
    # res = dbc.execute("SELECT main.fileName,main.datetime,main.latitude,main.longitude,main.callSign,vessel.shipName,rider.institution FROM main JOIN vessel ON main.callSign = vessel.callSign JOIN rider ON main.riderName = rider.name")
    # print(res.fetchall())
    res = dbc.execute(f"SELECT * FROM main " \
                        "JOIN vessel ON main.callSign = vessel.callSign " \
                        "JOIN agency ON main.agencyCode = agency.code " \
                        "JOIN launcher ON main.launcherCode = launcher.code " \
                        "JOIN probe ON main.probeCode = probe.code " \
                        "JOIN recorder ON main.recorderCode = recorder.code " \
                        "JOIN rider on main.riderName = rider.name " \
                        "JOIN samples on main.fileName = samples.fileName " \
                        "LIMIT ?", (limit,))
    
    print(f"\r\n> Printing {limit} entries:\r\n")    
    # convert query to dictionary
    dictionary_list = query_to_dict(res)
    
    print_dictionary_list(dictionary_list)

    print("> All read\r\n")    
    conn.close()


# reads data filtered by callsign and plots all the profiles ( if plot_profiles = True)
def read_database_profile(dbfile, callsign, plot_profiles=False):
    conn = sql.connect(dbfile)
    dbc = conn.cursor()
    res = dbc.execute("SELECT main.fileName,main.callSign,samples.dataPoints,samples.data FROM main JOIN samples ON main.fileName = samples.fileName WHERE main.callSign = ? ", (callsign,))

    print("Printing profiles for:", callsign, "\r\n")
    i = 0
    for row in res:
        print(">", row[0],"| dataPoints:", row[2])
        profile = json.loads(row[3])       
        depths = profile["depth"] 
        temperatures = profile["temperature"]
        print("> List length:", len(temperatures), "| Printing top-20 values:\r\n" , f"> DEPTHS:{depths[:20]}\r\n", f"> TEMPS:{temperatures[:20]}", "\r\n--\r\n")
        # plot profile
        if(plot_profiles == True):
            print(f"Plotting profile {i}...")
            plot_profile(depths,temperatures)
            i = i + 1

    conn.close()


# reads database filtered by range of dates
def read_database_date_range(dbfile, date_start, date_end):
    conn = sql.connect(dbfile)
    dbc = conn.cursor()
    res = dbc.execute("SELECT main.fileName,main.datetime,main.callSign,main.latitude,main.longitude,main.soopLine FROM main WHERE main.datetime >= ? AND main.datetime <= ?", (date_start, date_end))   

    print(f"> Printing by date: between {date_start} and {date_end}")
    # convert query to dictionary
    dictionary_list = query_to_dict(res)    
    # print dictionaries:
    print_dictionary_list(dictionary_list)

    print("> All read\r\n")
    conn.close()
    
    
# The most complete filter. Read database filtering by callsign, shipname, soop line, rider, dates and optionally export a json file for each entry
# Use wildcard '%' for incomplete strings i.e. 'A%' filters all variable values starting in 'A'
def read_database_filtered(dbfile, callsign = "%", shipname = "%", soopline = "%", ridername = "%", date_start="1900-01-01", date_end="2100-01-01", response_limit = 10000, export_json = False):
    conn = sql.connect(dbfile)
    dbc = conn.cursor()

    COMMAND = """SELECT
	main.callSign,vessel.IMO,vessel.shipName,main.shipSpeed,main.shipDirection,main.launchHeight,main.latitude,main.longitude,main.totalWaterDepth,
	main.launcherCode,launcher.name as launcherName,main.probeCode,probe.name as probeName,probe.coefA as probeCoefA,probe.coefB as probeCoefB,probe.maxDepth as probeMaxDepth,
	main.recorderCode,recorder.name as recorderName, recorder.frequency as recorderFreq,main.seasVersion,main.soopLine,main.transectNumber,main.sequenceNumber,
    main.agencyCode,agency.name as agencyName,main.riderName,rider.email as riderEmail,rider.phone as riderPhone,rider.institution as riderInstitution,
	main.msgType,main.fileName,main.datetime,samples.dataPoints,samples.data
    FROM main 
    JOIN vessel ON main.callSign = vessel.callSign
    JOIN rider ON main.riderName = rider.name
    JOIN agency ON main.agencyCode = agency.code
    JOIN launcher ON main.launcherCode = launcher.code
    JOIN probe ON main.probeCode = probe.code
    JOIN recorder ON main.recorderCode = recorder.code
    JOIN samples ON main.fileName = samples.fileName
    WHERE main.soopLine LIKE ? AND vessel.shipName LIKE ? AND main.callSign LIKE ? AND main.riderName LIKE ?
    AND main.datetime BETWEEN ? AND ? 
    LIMIT ?"""

    try:
        res = dbc.execute(COMMAND, (soopline, shipname, callsign, ridername, date_start, date_end, response_limit))
        
        print(f"> Printing selection: date {date_start} - {date_end} | soopline {soopline} | shipname {shipname} | callsign {callsign} | rider {ridername} | up to {response_limit} entries...\r\n")
        # convert query to dictionary
        dictionary_list = query_to_dict(res)    
        # print dictionaries:
        print_dictionary_list(dictionary_list)
        # Export query to json files
        if export_json == True:
            database_to_json(dictionary_list)
    except Exception as e:
        print("> ERROR: database query could not be done! >>", e)
        
    conn.close()


def database_to_json(dict_list):
    for i,xbtdict in enumerate(dict_list):
        try:
            print(f"> {i}: exporting {xbtdict["fileName"]} to json...")
            # add db_ to indicate it was read from the database and not directy exported from binary file
            xbtdict["fileName"] = "db_" + xbtdict["fileName"]
            xbt_export_json(xbtdict)
        except:
            print("> ERROR: json file could not be saved!")
    print("> Json exports finished\r\n")


# reads database and generates a grouped report by soopline, callsign and year-month
def database_summary(dbfile, start_date = "1900-01-01", end_date = "2100-01-01", show = True, outputDir = "output", fname = "report.txt", export = False):
    print("> XBT DATABASE SUMMARY:\r\n")
    conn = sql.connect(dbfile)
    dbc = conn.cursor()

    COMMAND = """
        SELECT main.soopLine,strftime('%Y-%m', main.datetime) AS year_month,main.callSign,vessel.shipName,main.riderName,main.transectNumber,COUNT(main.fileName) AS profiles,MIN(main.datetime) AS date_start,MAX(main.datetime) as date_end
        FROM main
        JOIN vessel ON main.callSign = vessel.callSign
        WHERE main.datetime BETWEEN ? AND ?
        GROUP BY main.soopLine,year_month,main.callSign,main.transectNumber 
        ORDER BY main.soopLine,year_month ASC """
    try:
        res = dbc.execute(COMMAND, (start_date, end_date))
        dictionary_list = query_to_dict(res)    
        columns = list(dictionary_list[0].keys())
        TEXT = ""
        for i,col in enumerate(columns):
            if i == (len(columns) - 1):
                # print(col, end = '\r\n')
                TEXT = TEXT + str(col) + "\n"
            else:
                # print(col, end = ',')
                TEXT = TEXT + str(col) + ","
        
        for dictionary in dictionary_list:
            for j,col in enumerate(columns):
                if j == (len(columns) - 1):
                    # print(dictionary[col], end='\r\n')
                    TEXT = TEXT + str(dictionary[col]) + "\n"
                else:
                    # print(dictionary[col], end=',')
                    TEXT = TEXT + str(dictionary[col]) + ","
        # display report on screen
        if show == True:
            print(TEXT)
            print("\r\n")
        print("> All read\r\n") 
    except Exception as e:
        print("> ERROR: database query could not be done! >>", e)
        TEXT = f"WARNING: No results found for the date range specified: {start_date} : {end_date}"

    if export == True:
        export_text_to_file(TEXT, outputDir, fname)

    conn.close()

    return TEXT


# converts an sqlite select response to a dictionary
def query_to_dict(res):
    dictionary_list = []
    # get column names
    colNames = []
    for col in res.description:
        colNames.append(col[0])   
    # get values from each row
    for row in res:        
        xbtdict = {}
        for j,value in enumerate(row):
            # data is stored as json in database
            if colNames[j] == "data":
                xbtdict["depths"] = json.loads(value)["depth"]
                xbtdict["temperatures"] = json.loads(value)["temperature"]
            else:
                xbtdict[colNames[j]] = value
        dictionary_list.append(xbtdict)
    
    return dictionary_list


# reads database and retrieves data to create map, optionally limit number of points to plot
def read_database_map_info(dbfile, limit=10000):
    conn = sql.connect(dbfile)
    dbc = conn.cursor()
    COMMAND = """
        SELECT main.soopLine,main.callSign,main.transectNumber,main.latitude,main.longitude,main.datetime,main.fileName
        FROM main
        ORDER BY main.soopLine,main.transectNumber ASC
        LIMIT ? """

    res = dbc.execute(COMMAND, (limit,))
       
    # convert query to dictionary
    dictionary_list = query_to_dict(res)

    print(f"> Found {len(dictionary_list)} profiles to plot (<={limit})")
       
    conn.close()

    return dictionary_list



def get_files_to_process(dbfile, inputDir):
    new_files = []
    if os.path.isdir(inputDir) == True:
        # list files in directory
        fileList = os.listdir(inputDir)
        if os.path.isfile(dbfile):
            print(f"> Database {dbfile} found!")
            # connect to db and query files already there
            conn = sql.connect(dbfile)
            dbc = conn.cursor()
            COMMAND = "SELECT main.fileName from main"
            res = dbc.execute(COMMAND)
            # list files already in db    
            files_processed = []
            for f in res:
                files_processed.append(f[0])
            print(f"> {len(files_processed)} files already stored in database")
            # add files not in db to new list
            for file in fileList:
                if file not in files_processed:
                    new_files.append(file)
            print(f"> {len(new_files)} new files not stored in database")
        else:
            print(f"> {dbfile} database NOT found!")
            print(f"> All files in {inputDir} will be processed")
            return fileList
    else:
        print("> WARNING: directory does not exist!")
    
    return new_files