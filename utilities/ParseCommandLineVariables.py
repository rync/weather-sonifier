import re

def parse_command_line_variables(cmdVarList):
    # Extracts latitude and longitude from the commandline and returns them as an object
    #   if and only if both are populated.
    coords = {}
    for item in cmdVarList:
        try:
            if re.match('lat(itude)?=[\d]{0,2}(-)?(\.[\d]+)?' , item) is not None:
                coords['latitude'] = float(item.split('=')[1])
            if re.match('lon(gitude)?=[\d]{0,3}(-)?(\.[\d]+)?' , item ) is not None:
                coords['longitude'] = float(item.split('=')[1])
        except:
            print("The coordinates you entered are not properly formatted floats.\nWill continue, but using the default Robinson, PA coordinates.")
    try:
        if (coords['longitude'] is not None) and (coords['latitude'] is not None):
            return coords
        else:
            return None
    except:
        return None