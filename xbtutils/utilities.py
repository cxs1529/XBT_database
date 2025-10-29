import os # creates output dir
import json

def get_range(csvList,parameter,mType):
    if mType == 1:
        a = 1
        b = 2
    elif mType == 2:
        a = 3
        b = 4
    elif mType == 3:
        a = 5
        b = 6

    for line in csvList:
        if parameter in line:
            startBit = line[a]
            endBit = line[b]
            break
    return [int(startBit),int(endBit)]

# csvList = get_range_list()
# testRange = get_range(csvList, "SHIP_NAME", 3)
# print(testRange)

def bits_to_ascii(bitStr,startBit,endBit):
    binaryChunk = bitStr[startBit:(endBit+1)] # extract needed binary chunk
    mydata = int(binaryChunk,2) # binary to integer
    mydata = hex(mydata)[2:] # convert to hexadecimal and remove leading '0x'
    try:
        mydata = bytes.fromhex(mydata) # creates a bytes object from a string of hexadecimal digits like b'DCUJ2\x00\x00\x00\x00'
        mydata = mydata.decode("ASCII") # decode bytes hex to ascii        
    except:
        mydata = "N/A"    
    mydata = mydata.replace('\x00', '') # remove NULL chars
    return mydata

# convert a binary stream into a decimal, given start-end bit index, scale factor and offset
# if last the last variable is used and =True, it'll print the binary number for debugging purpuses
def bits_to_dec(bitStr,startBit,endBit,scale,offset, debugFlag = False):
    binaryChunk = bitStr[startBit:(endBit+1)] # extract needed binary chunk
    mydata = (int(binaryChunk,2) + offset)/scale
    if debugFlag == True:
        print(f"binaryChunk: {binaryChunk}, mydata: {mydata}, startBit: {startBit}, endBit: {endBit}")

    return mydata

def getTemperatures(bitStr,samples,startBit):
    tempList = []
    for x in range(startBit,startBit+samples*12,12): # each sample is 12 bits
        thisTemp = bits_to_dec(bitStr,x,x+11,100,-400) # current temperature point
        tempList.append(round(thisTemp,2))
    return tempList

def getDepths(samples):
    samplingFreq = 10.0
    A = 6.691
    B = -2.25
    dList = []
    for n in range(0,samples):
        time = (n+1)/samplingFreq
        depth = A * time + 0.001 * B * time*time
        dList.append(round(depth,2))
    return dList


# def two_digit(num):
#     strNum = ''
#     num = int(num)
#     if num < 10:
#         strNum = '0' + str(num)
#     else:
#         strNum = str(num)
#     return strNum


# def list_temperatures(temps,depths,nMax):
#     print('\n-------------\n')
#     print('T[°C]    D[m]')
#     i = 0
#     for t in temps:
#         print(t,'   ',depths[i])
#         i = i + 1
#         if i > nMax:
#             break


# export the binary as an ascii (text) file
# It takes an xbt class object and the output directory path
def xbt_export_ascii(xbt, outputDir = "output"):
    # get ascii file name
    fname = xbt.fileName.split("/")[-1] # get only file name
    fname = fname.split(".")[0] # remove the .bin
    asciiFile = fname + '_ascii.txt'
    # create full path to output file
    asciiPath = os.path.join(outputDir, asciiFile)
    try:
        # create output directory if it doesn't exist
        os.makedirs(outputDir, exist_ok=True) 
        # open file to write
        print("> Creating ASCII:", asciiPath)
        with open(asciiPath, 'w') as fout:      
            print('--------------------------------------------------------------------------------------------------', file=fout)
            print('fileName     |', xbt.fileName, file=fout)
            print('CallSign     |', xbt.vessel.callSign, file=fout)
            print('IMO          |', xbt.vessel.imo, file=fout)
            print('ShipName     |', xbt.vessel.shipName, file=fout)
            print('Speed        |', xbt.vessel.shipSpeed, 'kt', file=fout)
            print('Direction    |', xbt.vessel.shipDirection, '°', file=fout)
            print('Date         |', xbt.profileDatetime.dtString, file=fout)
            print('Latitude     |', xbt.vessel.latitude,'°', file=fout)
            print('Longitude    |', xbt.vessel.longitude,'°', file=fout)
            print('Water Depth  |', xbt.vessel.totalWaterDepth, 'm', file=fout)
            print('Line         |', xbt.line.soopLine, file=fout)
            print('Transect No. |', xbt.line.transectNumber, file=fout)
            print('Sequence No. |', xbt.line.sequenceNumber, file=fout)
            print('Agency       |', xbt.agency.name,'(',xbt.agency.code,')', file=fout)
            print('MSGType      |', xbt.msgType, file=fout)
            print('SEAS version |', xbt.gear.seasVersion)
            print('Launcher     |', xbt.gear.launcher.name, '(', xbt.gear.launcher.code,')', file=fout)
            print('LaunchHeight |', xbt.vessel.launchHeight,'m', file=fout)
            print('Recorder     |', xbt.gear.recorder.name, '(', xbt.gear.recorder.code , ')', 'Frequency:', xbt.gear.recorder.frequency,'Hz', file=fout)
            print('Probe        |', xbt.gear.probe.name, '(', xbt.gear.probe.code,')', 'SN:', int(xbt.gear.probe.serial), 'Max Depth:', xbt.gear.probe.maxDepth, 'CoefA:', xbt.gear.probe.coefA, 'CoefB:', xbt.gear.probe.coefB, file=fout)
            print('Samples      |', xbt.profile.dataPoints, file=fout)
            print('Rider        |','Name:' ,xbt.rider.name, "|Email:",xbt.rider.email, "|Institution:", xbt.rider.institution, "|Phone:", xbt.rider.phone, file=fout)
            print('--------------------------------------------------------------------------------------------------', file=fout)
            # write depth vs temperatures
            print("D[m]","T[°C]", file=fout)
            for i in range(0, len(xbt.profile.temperatures)):
                print(xbt.profile.depths[i], xbt.profile.temperatures[i], file=fout)
            print("EOF", file=fout)
            # close file
            fout.close()
            print(f"> ASCII saved to {asciiPath} OK")
    except Exception as e:
        print(f"> WARNING: {asciiPath} could not be saved >>", e)
    finally:
        print("> End of ascii conversion")


# Converts an xbt class object into a json file, stored in outputDir
def xbt_export_json(xbtdict, outputDir = "output"):
    # get file name
    fname = xbtdict["fileName"]
    fname = fname.split(".")[0] # remove the .bin
    jsonFile = fname + '.json'
    # create full path to output file
    jsonPath = os.path.join(outputDir, jsonFile)
    try:
        # create output directory if it doesn't exist
        os.makedirs(outputDir, exist_ok=True)  
        print("> Creating JSON: ", jsonPath)        
        with open(jsonPath,'w') as file:
            json.dump(xbtdict, file, indent=4)
        print(f"> Dictionary saved to {jsonFile} OK")
    except Exception as e:
        print(f"> WARNING: {jsonPath} could not be saved >>", e)
    finally:
        print("> End of json conversion")


def print_dictionary(dict, sample_count = 20):
    for key in dict.keys():
        # do not print all the samples
        if key == "depths" or key == "temperatures":
            print(f"{key} : {dict[key][:sample_count]} ...")
        else:
            print(f"{key} : {dict[key]}")


def print_dictionary_list(dict_list):
    for i,dict in enumerate(dict_list):
        print("\r\n> Entry", i, ":")
        print("------------")
        print_dictionary(dict, 20)


def export_text_to_file(text, outputDir, fname):
    print(f"> Exporting report to {outputDir}")
    filePath = os.path.join(outputDir, fname)
    try:
        # create output directory if it doesn't exist
        os.makedirs(outputDir, exist_ok=True) 
        with open(filePath, 'w') as fout:
            print(text, file=fout)
    except Exception as e:
        print(f"> WARNING: {fname} could not be saved >>", e)




# Uncomment import csv to use this function - function not needed to run script unless dataranges need to be changed
# import csv
#
# def get_range_list():
#     # Columns -> ['Description', 'StartBit1', 'EndBit1', 'StartBit2', 'EndBit2', 'StartBit3', 'EndBit3']
#     filePath = 'dataRanges.csv'
#     fin = open(filePath,'r')
#     csvFile = csv.reader(fin)
#     csvList = []
#     for subList in csvFile:
#         csvList.append(subList)
#     fin.close()
#     return csvList # list with sublists of ranges