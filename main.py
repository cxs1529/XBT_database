from xbtutils import decode, database, utilities
import os
import time

# Process files in this directory
# inputDir = "data"
inputDir = "C:\\Users\\christian.saiz\\Documents\\0_NOAA\\1_NOAA_work\\1_XBT\\ftp\\2025"
# output directory for ascii and json files
outputDir = "output"
# database name
dbfile = "xbtData.db"

maxcount = 500 # with -1 disable count and process all

############################################# CODE STARTS HERE #############################################
print("\r\n*** XBT BINARY DECODER ***\r\n")

# start timer to determine processing time
start_time = time.process_time()
# get files to process and store in database
files_to_process = database.get_files_to_process(dbfile, inputDir)
print(f"> Found {len(files_to_process)} new files to process in {inputDir}:")

index = -1 # with -1 it processes all files in directory. Otherwise specify file index in list of files


if index == -1:
    if maxcount > 0:
        files_to_process = files_to_process[:maxcount]
        for i,f in enumerate(files_to_process):
            print(f"> {i} : {f}")
    for k,file in enumerate(files_to_process):
        print(f"\r\n> File {k} of {len(files_to_process)}:")
        filePath = os.path.join(inputDir, file)
        if os.path.isfile(filePath) and (".bin" in file):
            xbtdata, file_ok = decode.decode_binary(filePath)
            if file_ok:
                # xbtdata.print_binary_header()            
                database.xbt_add_to_database(xbtdata, dbfile)
                # export binary to ascii txt file
                # export_ascii(xbtdata, outputDir)
                # export binary to json file
                # xbt_dict = xbtdata.convert_to_dictionary()
                # utilities.xbt_export_json(xbt_dict, outputDir)
        else:
            print(f"> WARNING: {file} not a valid binary file!")

    print(f"> Finished: {k+1} of {len(files_to_process)} files in {inputDir} processed!\r\n")

    # Calculate processing time
    end_time = time.process_time()
    elapsed_time = end_time - start_time
    print(f"CPU time spent by the process: {elapsed_time:.2f} seconds")

    # read from database        
    # database.read_database_all(dbfile, 3)
    # database.read_database_profile(dbfile, "9V8584", plot_profiles=True)
    # database.read_database_profile(dbfile, "9V8584")
    # database.read_database_date_range(dbfile, "2025-10-20", "2025-10-22")
    # database.list_database_tables(dbfile)
    # database.read_database_filtered(dbfile, callsign = "%", shipname = "%", soopline = "%", ridername = "%", 
    #                                 date_start="2025-01-01", date_end="2025-01-15", export_json=False)
    
else:
    filePath = os.path.join(inputDir, str(files_to_process[index]))
    xbtdata, file_ok = decode.decode_binary(filePath)
    if file_ok:
        xbtdata.print_binary_header()
        # database.xbt_add_to_database(xbtdata, dbfile)
        # database.read_database(dbfile)
        
