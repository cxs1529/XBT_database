import bitstring # https://bitstring.readthedocs.io/en/stable/bitarray.html#bitstring.BitArray
from .utilities import *
from .dataRanges import *
from .agency_info import *
from .gear_info import *
from .rider_info import *


# Get bit range from CSV file - Table embedded in script already
# csvList = get_range_list() # returns list with ['Description', 'StartBit1', 'EndBit1', 'StartBit2', 'EndBit2', 'StartBit3', 'EndBit3']
def export_to_ascii(binfile, outputDir):
    # Extract data from binary file
    myBitStream = bitstring.ConstBitStream(filename=binfile) # reads the whole file as a bitstring object
    StringOfBits = myBitStream.bin  # get the contents as a string of bits
    # metadata
    newMessageType = int(bits_to_dec(StringOfBits,78,87,1,0)) # use this to determine start and end bits
    # WMO_ID
    [a,b] = get_range(csvList, "WMO_ID", newMessageType)
    callsign = bits_to_ascii(StringOfBits,a,b)
    # LATITUDE
    [a,b] = get_range(csvList, "LATITUDE", newMessageType)
    lat = bits_to_dec(StringOfBits,a,b,1E5,-9E6)
    # LONGITUDE
    [a,b] = get_range(csvList, "LONGITUDE", newMessageType)
    lon = bits_to_dec(StringOfBits,a,b,1E5,-18E6)
    # SOOP_LINE
    [a,b] = get_range(csvList, "SOOP_LINE", newMessageType)
    soopLine = bits_to_ascii(StringOfBits,a,b)
    # TRANSECT_NUMBER
    [a,b] = get_range(csvList, "TRANSECT_NUMBER", newMessageType)
    transectNumber = bits_to_dec(StringOfBits,a,b,1,0)
    # SEQUENCE_NUMBER
    [a,b] = get_range(csvList, "SEQUENCE_NUMBER", newMessageType)
    sequenceNumber = bits_to_dec(StringOfBits,a,b,1,0)
    # SHIP_NAME
    [a,b] = get_range(csvList, "SHIP_NAME", newMessageType)
    shipName = bits_to_ascii(StringOfBits,a,b)
    # XBT_LAUNCHER_TYPE
    launcher = LauncherClass("code", "name")
    [a,b] = get_range(csvList, "XBT_LAUNCHER_TYPE", newMessageType)
    launcher.code = bits_to_dec(StringOfBits,a,b,1,0)
    launcher.name = get_launcher(launcher.code)

    # SEAS_VERSION
    [a,b] = get_range(csvList, "SEAS_VERSION", newMessageType)
    seasVersion = bits_to_dec(StringOfBits,a,b,1,0)
    # PROBE_SERIAL_NUMBER
    [a,b] = get_range(csvList, "PROBE_SERIAL_NUMBER", newMessageType)
    probeSerialNumber = bits_to_dec(StringOfBits,a,b,1,0)
    # LAUNCH_HEIGHT
    [a,b] = get_range(csvList, "LAUNCH_HEIGHT", newMessageType)
    launchHeight = bits_to_dec(StringOfBits,a,b,1E2,0)
    # SHIP_DIRECTION
    [a,b] = get_range(csvList, "SHIP_DIRECTION", newMessageType)
    shipDirection = bits_to_dec(StringOfBits,a,b,1,0)
    # SHIP_SPEED
    [a,b] = get_range(csvList, "SHIP_SPEED", newMessageType)
    shipSpeed = round(bits_to_dec(StringOfBits,a,b,1E2,0) * 1.94384, 2) # m/s to knot
    # INSTRUMENT_TYPE
    [a,b] = get_range(csvList, "INSTRUMENT_TYPE", newMessageType)
    instrumentType = int(bits_to_dec(StringOfBits,a,b,1,0)) # use this to determine coefficients A,B - based on probe ex. deep blue
    probe = ProbeClass(-99.9, -99.9, -999, "unknown",-99)
    probe = get_probe(instrumentType)
    # RECORDER_TYPE
    [a,b] = get_range(csvList, "RECORDER_TYPE", newMessageType)
    recorderType = int(bits_to_dec(StringOfBits,a,b,1,0)) # use this to determine sampling frequency - based on data acquisition system ex. MK21
    recorder = RecorderClass('unknown', -99, -99)
    recorder = get_recorder(recorderType)
    # TOTAL_WATER_DEPTH
    [a,b] = get_range(csvList, "TOTAL_WATER_DEPTH", newMessageType)
    totalWaterDepth = bits_to_dec(StringOfBits,a,b,1,0)
    # AGENCY_OWNER
    [a,b] = get_range(csvList, "AGENCY_OWNER", newMessageType)
    agencyCode = int(bits_to_dec(StringOfBits,a,b,1,0)) # use this to get agency owner
    agency = AgencyClass(-99, "name")
    agency = get_agency(agencyCode)
    # TIMES_REPLICATED
    [a,b] = get_range(csvList, "TIMES_REPLICATED", newMessageType)
    dataPoints = int(bits_to_dec(StringOfBits,a,b,1,0))

    # DATE & TIME
    # YEAR
    [a,b] = get_range(csvList, "YEAR", newMessageType)
    year = int(bits_to_dec(StringOfBits,a,b,1,0))
    # MONTH
    [a,b] = get_range(csvList, "MONTH", newMessageType)
    month = int(bits_to_dec(StringOfBits,a,b,1,0))
    # DAY
    [a,b] = get_range(csvList, "DAY", newMessageType)
    day = int(bits_to_dec(StringOfBits,a,b,1,0))
    # HOUR
    [a,b] = get_range(csvList, "HOUR", newMessageType)
    hour = int(bits_to_dec(StringOfBits,a,b,1,0))
    # MINUTE
    [a,b] = get_range(csvList, "MINUTE", newMessageType)
    minute = int(bits_to_dec(StringOfBits,a,b,1,0))

    # RIDER INFORMATION (class/object rider.var)
    rider = RiderClass("name", "email", "institution", "phone")
    rider = get_rider(StringOfBits, csvList, newMessageType, dataPoints)

    # temperatures and depths as recorded - no smoothering
    [a,b] = get_range(csvList, "SEA_SURFACE_TEMPERATURE", newMessageType)
    temperatureList = getTemperatures(StringOfBits,dataPoints,a)
    depthList = getDepths(dataPoints)


    # DATE FORMAT
    date = str(month) + "-" + str(day) + "-" + str(year) + ' ' + two_digit(hour) + ':' + two_digit(minute)

    print('CallSign     |', callsign)
    print('ShipName     |', shipName)
    print('Speed        |', shipSpeed, 'kt')
    print('Direction    |', shipDirection, '°')
    print('Date         |',date)
    print('Latitude     |',lat,'°')
    print('Longitude    |',lon,'°')
    print('Water Depth  |', totalWaterDepth, 'm')
    print('Line         |',soopLine)
    print('Transect No. |',transectNumber)
    print('Sequence No. |',sequenceNumber)
    print('Agency       |',agency.name,'(',agency.code,')')
    print('MSGType      |',newMessageType)
    print('SEAS version |',seasVersion)
    print('Launcher     |',launcher.name, '(', launcher.code,')')
    print('LaunchHeight |',launchHeight,'m')
    print('Recorder     |', recorder.name, '(', recorder.code , ')', ' -Frequency:', recorder.frequency,'Hz')
    print('Probe        |', probe.name, '(', probe.code,')', '-SN:',    int(probeSerialNumber), '-Max Depth:', probe.maxDepth, '-CoefA:', probe.coefA, '-CoefB:', probe.coefB)
    print('Samples      |', dataPoints)
    print('Rider        |','-Name:' ,rider.name, "-Email:",rider.email, "-Institution:", rider.institution, "-Phone:", rider.phone)


    export_ascii(binfile, outputDir, callsign,shipName,shipSpeed,shipDirection,date,lat,lon,totalWaterDepth,
                soopLine,transectNumber,sequenceNumber,agency,newMessageType,seasVersion,launcher,launchHeight,
                recorder,probe,dataPoints,rider,temperatureList,depthList,probeSerialNumber)