import bitstring # https://bitstring.readthedocs.io/en/stable/bitarray.html#bitstring.BitArray
from .utilities import *
from .dataRanges import *
from .agency_info import *
from .gear_info import *
from .rider_info import *
from .vessel_info import *
from .sample_info import *
# from .extras import *


class xbtBinaryClass:
  def __init__(self, msgType=-99, fileName="na"):
    self.vessel = VesselClass()
    self.gear = GearClass()
    self.line = LineClass()    
    self.agency = AgencyClass()
    self.rider = RiderClass()
    self.msgType = msgType
    self.fileName = fileName
    self.profileDatetime = ProfileDatetimeClass()
    self.profile = ProfileClass()

  # returns a dictionary with the xbt object values
  def convert_to_dictionary(self):
    xbtdict = {
      # vessel
      "callSign": self.vessel.callSign,
      "imo": self.vessel.imo,
      "shipName": self.vessel.shipName,
      "shipSpeed": self.vessel.shipSpeed,
      "shipDirection": self.vessel.shipDirection,
      "launchHeight": self.vessel.launchHeight,
      "latitude": self.vessel.latitude,
      "longitude": self.vessel.longitude,
      "totalWaterDepth": self.vessel.totalWaterDepth,
      # gear
      "launcherCode": self.gear.launcher.code,
      "launcherName": self.gear.launcher.name,
      "probeCode": self.gear.probe.code,
      "probeName": self.gear.probe.name,
      "probeCoefA": self.gear.probe.coefA,
      "probeCoefB": self.gear.probe.coefB,
      "probeMaxDepth": self.gear.probe.maxDepth,      
      "recorderCode": self.gear.recorder.code,
      "recorderName": self.gear.recorder.name,
      "recorderFreq": self.gear.recorder.frequency,
      "seasVersion": self.gear.seasVersion,
      # line
      "soopLine": self.line.soopLine,
      "transectNumber": self.line.transectNumber,
      "sequenceNumber": self.line.sequenceNumber,
      # agency
      "agencyCode": self.agency.code,
      "agencyName": self.agency.name,
      # rider
      "riderName": self.rider.name,
      "riderEmail": self.rider.email,
      "riderInstitution": self.rider.institution,
      "riderPhone": self.rider.phone,
      # msgtype
      "msgType" : self.msgType,
      # fname
      "fileName" : self.fileName,
      # profile datetime
      # "dtObject": int = -99,
      "dtString": self.profileDatetime.dtString,
      # profile
      "dataPoints": self.profile.dataPoints,
      "depths": self.profile.depths,
      "temperatures": self.profile.temperatures  
    }
    
    return xbtdict

  # print only the metadata
  def print_binary_header(self):
    print("\r\n********************************************************************")
    print('fileName     |', self.fileName)
    print('CallSign     |', self.vessel.callSign)
    print('IMO          |', self.vessel.imo)
    print('ShipName     |', self.vessel.shipName)
    print('Speed        |', self.vessel.shipSpeed, 'kt')
    print('Direction    |', self.vessel.shipDirection, '°')
    print('Date         |', self.profileDatetime.dtString)
    print('Latitude     |', self.vessel.latitude,'°')
    print('Longitude    |', self.vessel.longitude,'°')
    print('Water Depth  |', self.vessel.totalWaterDepth, 'm')
    print('Line         |', self.line.soopLine)
    print('Transect No. |', self.line.transectNumber)
    print('Sequence No. |', self.line.sequenceNumber)
    print('Agency       |', self.agency.name,'(',self.agency.code,')')
    print('MSGType      |', self.msgType)
    print('SEAS version |', self.gear.seasVersion)
    print('Launcher     |', self.gear.launcher.name, '(', self.gear.launcher.code,')')
    print('LaunchHeight |', self.vessel.launchHeight,'m')
    print('Recorder     |', self.gear.recorder.name, '(', self.gear.recorder.code , ')', 'Frequency:', self.gear.recorder.frequency,'Hz')
    print('Probe        |', self.gear.probe.name, '(', self.gear.probe.code,')', 'SN:', int(self.gear.probe.serial), 'Max Depth:', self.gear.probe.maxDepth, 'CoefA:', self.gear.probe.coefA, 'CoefB:', self.gear.probe.coefB)
    print('Samples      |', self.profile.dataPoints)
    print('Rider        |','Name:' ,self.rider.name, "Email:",self.rider.email, "Institution:", self.rider.institution, "Phone:", self.rider.phone)
    print("********************************************************************\r\n")

  # print only sampled data
  def print_binary_data(self):
    print("\n>DataPoints:", self.profile.dataPoints)
    print("#############################")
    print("D[m]","T[°C]")
    for i in range(0, len(self.profile.temperatures)):
      print(self.profile.depths[i], self.profile.temperatures[i])
    print("#############################")



     
     



# XBT Binary decoder main funciton
# Takes a self-descriptive .bin file path and returns an xbtBinaryClass object
def decode_binary(binfile):
    # create xbtdata object class to store binary file info
    xbt = xbtBinaryClass()
    file_ok = True # flag for flow control outside the function
    # File name
    xbt.fileName = binfile.split(os.sep)[-1] # get only file name

    print("\r\n** DECODING BINARY ", xbt.fileName, " **")
    try:
      # Extract data from binary file
      myBitStream = bitstring.ConstBitStream(filename=binfile) # reads the whole file as a bitstring object
      StringOfBits = myBitStream.bin  # get the contents as a string of bits
      # binary message decoder type 
      newMessageType = int(bits_to_dec(StringOfBits,78,87,1,0)) # use this to determine start and end bits
      xbt.msgType = newMessageType
      # METADATA & DATA
      # ----------------------------------------------------------------------------------------------------------------- #

      # VESSEL INFORMATION
      xbt.vessel = get_vessel(StringOfBits, csvList, newMessageType)
      # GEAR INFORMATION
      xbt.gear = get_gear(StringOfBits, csvList, newMessageType)
      # XBT LINE INFORMATION
      xbt.line = get_line(StringOfBits, csvList, newMessageType)
      # DATE TIME
      xbt.profileDatetime = get_sample_datetime(StringOfBits, csvList, newMessageType)
      # print("> xbt.profileDatetime:", xbt.profileDatetime.dtString)
      # PROFILE DATA
      xbt.profile = get_profile_data(StringOfBits, csvList, newMessageType)
      # AGENCY_OWNER
      xbt.agency = get_agency(StringOfBits, csvList, newMessageType)
      # RIDER INFORMATION (class/object rider.var)
      xbt.rider = get_rider(StringOfBits, csvList, newMessageType)
    # in case of any problem flag file as bad so no further processing or storage is done
    except Exception as e:
      print(f"> WARNING: {xbt.fileName} not a valid binary file! >>", e)
      file_ok = False
    finally:
      print("** END DECODING", xbt.fileName, " **")

    return xbt, file_ok



def decode_binary_warnings(binfile):
    # create xbtdata object class to store binary file info
    xbt = xbtBinaryClass()
    
    # File name
    xbt.fileName = binfile.split(os.sep)[-1] # get only file name

    print("\r\n** DECODING BINARY ", xbt.fileName, " **")
    
    # Extract data from binary file
    myBitStream = bitstring.ConstBitStream(filename=binfile) # reads the whole file as a bitstring object
    StringOfBits = myBitStream.bin  # get the contents as a string of bits
    # binary message decoder type 
    newMessageType = int(bits_to_dec(StringOfBits,78,87,1,0)) # use this to determine start and end bits
    xbt.msgType = newMessageType
    print("MSGType:", newMessageType)
    # METADATA & DATA
    # ----------------------------------------------------------------------------------------------------------------- #

    # VESSEL INFORMATION
    xbt.vessel = get_vessel(StringOfBits, csvList, newMessageType)
    # GEAR INFORMATION
    xbt.gear = get_gear(StringOfBits, csvList, newMessageType)
    # XBT LINE INFORMATION
    xbt.line = get_line(StringOfBits, csvList, newMessageType)
    # DATE TIME
    xbt.profileDatetime = get_sample_datetime(StringOfBits, csvList, newMessageType)
    # print("> xbt.profileDatetime:", xbt.profileDatetime.dtString)
    # PROFILE DATA
    xbt.profile = get_profile_data(StringOfBits, csvList, newMessageType)
    # AGENCY_OWNER
    xbt.agency = get_agency(StringOfBits, csvList, newMessageType)
    # RIDER INFORMATION (class/object rider.var)
    xbt.rider = get_rider(StringOfBits, csvList, newMessageType)
    # in case of any problem flag file as bad so no further processing or storage is done

  
    print("** END DECODING", xbt.fileName, " **")

    return xbt