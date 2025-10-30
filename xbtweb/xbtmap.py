import folium
import random
import os
    
# dbfile = "xbtData.db"
# max_profiles = 10000


# plot lat,lon in map with a different color for each soopline
def make_summary_map(dict_list, outputDir = "output", fname = "xbtmap.html"):
    init_pos = [20.416501, -69.914840]
    full_map = folium.Map(location=init_pos, zoom_start=6)

    soopLine_prev = ""
    callSign_prev = ""
    transectNumber_prev = ""
    # loop through list of dictionaries/profiles
    for dict in dict_list:   
        
        # extract reelvant values
        latitude = dict["latitude"]
        longitude = dict["longitude"]
        soopLine = dict["soopLine"]
        callSign = dict["callSign"]
        transectNumber = dict["transectNumber"]
        datetime = dict["datetime"]
        fileName = dict["fileName"]

        # check if callsign or soopline changed
        if (callSign != callSign_prev) or (soopLine != soopLine_prev) or (transectNumber != transectNumber_prev):
            fc_r,fc_g,fc_b = generate_random_rgb_color()

        # format to plot in map
        popup_text = f"callSign: {callSign}<br>position: {(latitude):.3f},{(longitude):.3f}<br>soopLine: {soopLine}<br>datetime: {datetime}<br>transectNumber: {transectNumber}<br>file: {fileName}"
        tip_text = f"callSign: {callSign}<br>soopLine: {soopLine} ({transectNumber})<br>datetime: {datetime}"
        
        # marker properties
        fillcolor = f"rgb({fc_r},{fc_g},{fc_b})"
        extcolor = "white"
        radius = 5
        # get marker object and add to map
        obj = create_map_marker(latitude , longitude, radius, extcolor, fillcolor, popup_text, tip_text )
        obj.add_to(full_map)
        # reset previous values for coloring
        callSign_prev = callSign
        soopLine_prev = soopLine
        transectNumber_prev = transectNumber

    # create output dir if it doesn't exist
    os.makedirs(outputDir, exist_ok=True)
    # save map as html
    
    map_path = os.path.join(outputDir,fname)
    full_map.save(map_path)
    print(f"> Map saved in {map_path}")
    
    return fname

# creates a circle marker and returns the marker object to add into the map
def create_map_marker(lat , lon, radius, extcolor, fillcolor, popup_text, tip_text ):

    myobj = folium.CircleMarker(
        location=[lat, lon],  # Latitude and Longitude
        radius=radius,                      # Radius in pixels
        color=extcolor,                   # Outline color
        fill=True,                      # Fill the circle
        fill_color=fillcolor,              # Fill color
        fill_opacity=0.7,               # Fill opacity
        popup=popup_text,           # Popup text on click
        tooltip=tip_text     # Tooltip text on hover
    )

    return myobj

# generates a random rgb color
def generate_random_rgb_color():
    """Generates a random RGB color as a tuple (r, g, b)."""
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)



# def main():
#     # query database and import list of filename, soopline, callsign, lat, lon and datetime
#     profile_list = database.read_database_map_info(dbfile, limit=max_profiles)

#     map = make_summary_map(profile_list)

#     # end of main

# if __name__ == "__main__":
#     main()


