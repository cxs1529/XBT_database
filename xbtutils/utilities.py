import os # creates output dir


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
        dList.append(-round(depth,2))
    return dList

def two_digit(num):
    strNum = ''
    num = int(num)
    if num < 10:
        strNum = '0' + str(num)
    else:
        strNum = str(num)
    return strNum


def list_temperatures(temps,depths,nMax):
    print('\n-------------\n')
    print('T[°C]    D[m]')
    i = 0
    for t in temps:
        print(t,'   ',depths[i])
        i = i + 1
        if i > nMax:
            break


def export_ascii(binfile, outputDir, callsign,shipName,shipSpeed,shipDirection,date,lat,lon,totalWaterDepth,
    soopLine,transectNumber,sequenceNumber,agency,newMessageType,seasVersion,launcher,launchHeight,
    recorder,probe,dataPoints,rider,temperatureList,depthList,probeSerialNumber):

    fname = binfile.split("/")[-1] # get only file name
    fname = fname.split(".")[0] # remove the .bin
    asciiFile = fname + '_ascii.txt'
    # create full path to output file
    asciiPath = os.path.join(outputDir, asciiFile)
    # create output directory if it doesn't exist
    os.makedirs(outputDir, exist_ok=True) 
    
    with open(asciiPath, 'w') as fout:
        print('FileName: ',fname ,file=fout)
        print('--------------------------------------------------------------------------------------------------', file=fout)
        print('CallSign     |', callsign, file=fout)
        print('ShipName     |', shipName, file=fout)
        print('Speed        |', shipSpeed, 'kt', file=fout)
        print('Direction    |', shipDirection, '°', file=fout)
        print('Date         |',date, file=fout)
        print('Latitude     |',lat,'°', file=fout)
        print('Longitude    |',lon,'°', file=fout)
        print('Water Depth  |', totalWaterDepth, 'm', file=fout)
        print('Line         |',soopLine, file=fout)
        print('Transect No. |',transectNumber, file=fout)
        print('Sequence No. |',sequenceNumber, file=fout)
        print('Agency       |',agency.name,'(', agency.code,')', file=fout)
        print('MSGType      |',newMessageType, file=fout)
        print('SEAS version |',seasVersion, file=fout)
        print('Launcher     |',launcher.name, '(', launcher.code,')', file=fout)
        print('LaunchHeight |',launchHeight,'m', file=fout)
        print('Recorder     |', recorder.name, '(', recorder.code , ')', ' -Frequency:', recorder.frequency,'Hz', file=fout)
        print('Probe        |', probe.name, '(', probe.code,')', '-SN:',    int(probeSerialNumber), '-Max Depth:', probe.maxDepth, '-CoefA:', probe.coefA, '-CoefB:', probe.coefB, file=fout)
        print('Samples      |', dataPoints, file=fout)
        print('Rider        |','-Name:' ,rider.name, "-Email:",rider.email, "-Institution:", rider.institution, "-Phone:", rider.phone, file=fout)
        print('--------------------------------------------------------------------------------------------------\n', file=fout)
        print('T[°C]    D[m]\n', file=fout)
        i = 0
        for t in temperatureList:
            print(t,'   ',depthList[i], file=fout)
            i = i + 1
        fout.close()



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