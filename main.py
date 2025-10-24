from xbtutils import decode
from xbtutils import database
import os

# File Path
# binfiles = ["data/done_20251021-1425_3E3535_20251021171500_N21_XBT.bin", 
#            "data/done_20251021-1425_3E3535_20251021171500_N21_XBT.bin",
#            "data/done_20251017-2040_PWAZ_20251017224500_N21_XBT.bin",
#            "data/done_20251017-2040_PWAZ_20251017213700_N20_XBT.bin",
#            "data/done_20251017-1925_D5CB9_20251017163600_N20_XBT.bin",
#            "data/done_20251017-1925_D5CB9_20251017152300_N19_XBT.bin"]

# find files in directory
inputDir = "data"
fileList = os.listdir("data")
print(fileList)

outputDir = "output"

dbfile = "xbtData.db"

index = -1
if index == -1:
    for file in fileList:
        filePath = os.path.join(inputDir, file)
        if os.path.isfile(filePath) and (".bin" in file):
            xbtdata = decode.decode_binary(filePath)
            xbtdata.print_binary_header()
            database.xbt_add_to_database(xbtdata, dbfile)
        else:
            print(f"{file} not a binary file")
    database.read_database(dbfile)
    # database.read_database_profile(dbfile)
else:
    filePath = os.path.join(inputDir, str(fileList[index]))
    xbtdata = decode.decode_binary(filePath)
    xbtdata.print_binary_header()
    database.xbt_add_to_database(xbtdata, dbfile)
    # database.read_database(dbfile)


# print depth vs temperature of the xbt object
# xbtdata.print_binary_data()

# convert xbt object to dictionary
# xbtdict = xbtdata.convert_to_dictionary()
# print(xbtdict)