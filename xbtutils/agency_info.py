from .utilities import *
from .dataRanges import *


class AgencyClass:
    def __init__(self, code=-99, name="na"):
        self.name = name
        self.code = code


def get_agency(StringOfBits, csvList, newMessageType):
    agency = AgencyClass()    

    try:
        # AGENCY_OWNER
        [a,b] = get_range(csvList, "AGENCY_OWNER", newMessageType)
        code = int(bits_to_dec(StringOfBits,a,b,1,0)) # use this to get agency owner
        agency.code = code
    except:
        code = -1
        agency.code = code

    if code == 36001:
        agency.name = "Australia, Bureau of Meteorology (BoM)"
    elif code == 36002:
        agency.name = "Australia, Joint Australian Facility for Ocean Observing Systems (JAFOOS)"
    elif code == 36003:
        agency.name = "Australia, the Commonwealth Scientific and Industrial Research Organisation (CSIRO)"
    elif code == 124001:
        agency.name = "Canada, Marine Environmental Data Service (MEDS)"
    elif code == 124002:
        agency.name = "Canada, Institute of Ocean Sciences (IOS)"
    elif code == 156001:
        agency.name = "China, The State Oceanic Administration"
    elif code == 156002:
        agency.name = "China, Second Institute of Oceanography, State Oceanic Administration"
    elif code == 156003:
        agency.name = "China, Institute of Ocean Technology"
    elif code == 250001:
        agency.name = "France, Institut de Recherche pour le Developpement (IRD)"
    elif code == 250002:
        agency.name = "France, Institut Francais de Recherche pour l'Exploitation de la mer (IFREMER)"
    elif code == 276001:
        agency.name = "Germany, Bundesamt fuer Seeschiffahrt und Hydrographie (BSH)"
    elif code == 276002:
        agency.name = "Germany, Institut fuer Meereskunde, Kiel"
    elif code == 356001:
        agency.name = "India, National Institute of Oceanography (NIO)"
    elif code == 356002:
        agency.name = "India, National Institute for Ocean Technology (NIOT)"
    elif code == 356003:
        agency.name = "India, National Centre for Ocean Information Service"
    elif code == 392001:
        agency.name = "Japan, Japan Meteorological Agency (JMA)"
    elif code == 392002:
        agency.name = "Japan, Frontier Observational Research System for Global Change"
    elif code == 392003:
        agency.name = "Japan, Japan Marine Science and Technology Centre (JAMSTEC)"
    elif code == 410001:
        agency.name = "Republic of Korea, Seoul National University"
    elif code == 410002:
        agency.name = "Republic of Korea, Korea Ocean Research and Development Institute  (KORDI)"
    elif code == 410003:
        agency.name = "Republic of Korea, Meteorological Research Institute"
    elif code == 540001:
        agency.name = "New Caledonia, Institut de Recherche pour le Developpement (IRD)"
    elif code == 554001:
        agency.name = "New Zealand, National Institute of Water and Atmospheric Research (NIWA)"
    elif code == 643001:
        agency.name = "Russian Federation, State Oceanographic Institute of Roshydromet"
    elif code == 643002:
        agency.name = "Russian Federation, Federal Service for Hydrometeorology and Environmental Monitoring"
    elif code == 724001:
        agency.name = "Spain, Instituto Espanol de Oceanografia"
    elif code == 826001:
        agency.name = "United Kingdom, Hydrographic Office"
    elif code == 826002:
        agency.name = "United Kingdom, Southampton Oceanography Centre (SOC)"
    elif code == 840001:
        agency.name = "USA, NOAA Atlantic Oceanographic and Meteorological Laboratories (AOML)"
    elif code == 840002:
        agency.name = "USA, NOAA Pacific Marine Environmental Laboratories (PMEL)"
    elif code == 840003:
        agency.name = "USA, Scripps Institution of Oceanography (SIO)"
    elif code == 840004:
        agency.name = "USA, Woods Hole Oceanographic Institution (WHOI)"
    elif code == 840005:
        agency.name = "USA, University of Washington"
    elif code == 840006:
        agency.name = "USA, Naval Oceanographic Office"
    elif code == 1048575:
        agency.name = "Missing value"
    else:
        agency.name = "NA"

    return agency