from .utilities import *



def get_extras(StringOfBits, csvList, newMessageType):
    #LLOYDS UNIQUE_TAG THIS_DATA_IS DATAQUALITY
    [a,b] = get_range(csvList, "LLOYDS", newMessageType)
    lloyds_a = bits_to_dec(StringOfBits,a,b,1,0)
    [a,b] = get_range(csvList, "LLOYDS", newMessageType)
    lloyds_b = bits_to_ascii(StringOfBits,a,b)
    print("lloyds:",lloyds_a, lloyds_b)

    [a,b] = get_range(csvList, "UNIQUE_TAG", newMessageType)
    tag_a = bits_to_dec(StringOfBits,a,b,1,0)
    [a,b] = get_range(csvList, "UNIQUE_TAG", newMessageType)
    tag_b = bits_to_ascii(StringOfBits,a,b)
    print("tag:", tag_a, tag_b)

    [a,b] = get_range(csvList, "THIS_DATA_IS", newMessageType)
    datais_a = bits_to_dec(StringOfBits,a,b,1,0)
    [a,b] = get_range(csvList, "THIS_DATA_IS", newMessageType)
    datais_b = bits_to_ascii(StringOfBits,a,b)
    print("datais:", datais_a, datais_b)

    [a,b] = get_range(csvList, "DATAQUALITY", newMessageType)
    dataq_a = bits_to_dec(StringOfBits,a,b,1,0)
    [a,b] = get_range(csvList, "DATAQUALITY", newMessageType)
    dataq_b = bits_to_ascii(StringOfBits,a,b)
    print("dataq:",dataq_a, dataq_b)