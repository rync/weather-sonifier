import os
import sys
from utilities.ParseCommandLineVariables import parse_command_line_variables
from utilities.NOAAWebScraper import retrieve_noaa_page, scrape_noaa_page
from utilities.WeatherDataSonificationFormatter import convert_weather_data
from utilities.ChuckFileGenerator import create_chuck_file

def get_data():
    # Uses the utilities in NOAAWebScraper and ParseCommandLineVariables to retrieve the current weather data.
    cmdVar = parse_command_line_variables(sys.argv)
    if cmdVar is not None:
        noaaPage = retrieve_noaa_page(lat=cmdVar['latitude'], lon=cmdVar['longitude'])
    else:
        noaaPage = retrieve_noaa_page()

    if noaaPage is not None:
        try:
            data = scrape_noaa_page(noaaPage)
            return data
        except:
            print("The coordinates you entered aren't accessible by the NOAA website.\nTry using coordinates specific to the continental US.")
    else:
        print("The coordinates you entered are invalid.")


# This will be performed in four steps:
# 1. Retrieve the data from the NOAA website at weather.gov
# 2. Convert the data into something a format that can be 'sonified'
# 3. Create a file that can be performed by the audio generation program Chuck
# 4. Run Chuck via bash command
sonificationData = convert_weather_data(get_data())
filename = create_chuck_file(sonificationData)
os.system('chuck {}'.format(filename))