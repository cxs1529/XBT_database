from .utilities import *


class RiderClass:
  def __init__(self, name="na", email="na", institution="na", phone="na"):
    self.name = name
    self.email = email
    self.institution = institution
    self.phone = phone


def get_rider(StringOfBits,csvList,newMessageType):

    rider = RiderClass()

    try:
      # TIMES_REPLICATED
      [a,b] = get_range(csvList, "TIMES_REPLICATED", newMessageType)
      dataPoints = int(bits_to_dec(StringOfBits,a,b,1,0))

      # Temperature blocks info (size, start, end)
      [SSTstartBit,SSTendBit] = get_range(csvList, "SEA_SURFACE_TEMPERATURE", newMessageType)
      [tempStartBit,tempEndBit] = get_range(csvList, "RIDER_NAME", newMessageType)
      blockSize = SSTendBit - SSTstartBit + 1 # data blocksize is 12 bits

      # 1- rider name
      [a,b] = get_range(csvList, "NUMBER_OF_RIDER_BLOCKS", newMessageType)
      riderBlocks = int(bits_to_dec(StringOfBits,a,b,1,0))
      riderNameStartBit = tempStartBit + (dataPoints * blockSize)
      riderNameEndBit = riderNameStartBit + riderBlocks * 40 - 1 # ascii blocks are 40 bits
      rider.name = bits_to_ascii(StringOfBits,riderNameStartBit,riderNameEndBit)

      # 2- rider email
      [a,b] = get_range(csvList, "NUMBER_OF_RIDER_EMAIL_BLOCKS", newMessageType)
      riderEmailBlocks = int(bits_to_dec(StringOfBits,a,b,1,0))
      riderEmailStartBit = riderNameEndBit
      riderEmailEndBit = riderEmailStartBit + riderEmailBlocks * 40
      rider.email = bits_to_ascii(StringOfBits,riderEmailStartBit,riderEmailEndBit)

      # 3- rider institution
      [a,b] = get_range(csvList, "NUMBER_OF_RIDER_INSTITUTION_BLOCKS", newMessageType)
      riderInstitutionBlocks = int(bits_to_dec(StringOfBits,a,b,1,0))
      riderInstitutionStartBit = riderEmailEndBit
      riderInstitutionEndBit = riderInstitutionStartBit + riderInstitutionBlocks * 40
      rider.institution = bits_to_ascii(StringOfBits,riderInstitutionStartBit,riderInstitutionEndBit)

      # 4- rider phone
      [a,b] = get_range(csvList, "NUMBER_OF_RIDER_PHONE_BLOCKS", newMessageType)
      riderPhoneBlocks = int(bits_to_dec(StringOfBits,a,b,1,0))
      riderPhoneStartBit = riderInstitutionEndBit
      riderPhoneEndBit = riderPhoneStartBit + riderPhoneBlocks * 40
      rider.phone = bits_to_ascii(StringOfBits,riderPhoneStartBit,riderPhoneEndBit)
    except:
       rider.name = "NA"
       rider.email = "NA"
       rider.phone = "NA"
       rider.institution = "NA"

    return rider