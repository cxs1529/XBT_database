from xbtutils import database

dbfile = "xbtData.db"

# # Create database report and optionally export as a text file
database.database_summary(dbfile, start_date="2025-01-01", end_date="2025-03-01",outputDir="output", fname="myreport.txt", export=False)

# # read all database tables in raw format
# database.read_database_all(dbfile, 3)

# # read all profiles matching a callsign, and optionally plot all profiles
# database.read_database_profile(dbfile, callsign="9V8584", plot_profiles=True)

# # read all profile matching a callsign without plotting profiles
# database.read_database_profile(dbfile, "9V8584")

# # read database profile headers within a date range
# database.read_database_date_range(dbfile, "2025-10-20", "2025-10-22")

# # list all tables and columns in the database
# database.list_database_tables(dbfile)

# # The most complete filter. Read database filtering by callsign, shipname, soop line, rider, dates and optionally export a json file for each entry
# Use wildcard '%' for incomplete strings i.e. 'A%' filters all variable values starting in 'A'
# database.read_database_filtered(dbfile, callsign = "%", shipname = "%", soopline = "AX07", ridername = "%", 
#                                 date_start="2025-01-01", date_end="2025-10-31", export_json=True, response_limit=100)