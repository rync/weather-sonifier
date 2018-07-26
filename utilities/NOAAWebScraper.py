import re

from bs4 import BeautifulSoup
from urllib import parse
from urllib.request import Request, urlopen

def format_measurement(str, splitter=' '):
    # This method splits strings into value and unit, via either a space or another character.
    # This is included to extract integer data for temperature and barometer readings,
    #   eg. '12.22 in' becomes [12.22, 'in']
    # The data is then returned as an object containing the value and unit.
    valList = str.split(splitter)
    return {
        'value': float(valList[0]),
        'unit': valList[1]
    }

def format_wind_speed(str):
    # Wind speed presents a unique case compared to format_measurement due to the added cardinality chars.
    # This will extract cardinality, value, and unit from the space-delimited string,
    #   e.g. 'S 12 mph' becomes ['S', 12.0, 'mph']
    # The data is then returned as an object containing the cardinality, value, and unit.
    try:
        valList = str.split(' ')
        return {
            'cardinality': valList[0],
            'value': float(valList[1]),
            'unit': valList[2]
        }
    except:
        # When there is no perceptible wind, NOAA returns 'Calm'. We'll return None.
        return None

def format_humidity(str):
    # This method handles the unique case of humidity, which is presented without a delimiting character.
    # In example, '83%' becomes [83, '%']
    # The data is then returned as an object containing the value and unit.
    return {
        'value': float(str.split('%')[0]),
        'unit': '%'
    }

def split_string_and_parens(str):
    # This method will reformat a string that the NOAA creates to represent multiple measurements for
    #   a particular metric and return an array of the contained strings.
    # E.g.: '10 in (25.4 cm)' becomes ['10 in', '25.4 cm']
    return str.replace(')', '').split(' (')

def get_current_conditions_table_rows(dom):
    # Searches the NOAA site DOM for the rows in the current conditions details table,
    #   and returns the row objects as an array of HTML elements.
    return dom.find_all(id='current_conditions_detail')[0].findChildren('table')[0].findChildren('tr')

def extract_multiple_readings(text, unitSplitter=' '):
    # This intermediary method will:
    #   1. extract the list of measurements from a string (e.g. '10 in (25.4 cm)'),
    #   2. use split_string_and_parens() to extract an array of measurement strings,
    #   3. use format_measurement to convert each measurement string into an object containing value and unit, and
    #   4. return the objects as an array.
    readings = split_string_and_parens(text)
    return [
        format_measurement(readings[0], unitSplitter),
        format_measurement(readings[1], unitSplitter)
    ]

def retrieve_noaa_page(lat=40.44, lon=-80.07):
    # Given a location latitude and longitude, this method will format the corresponding URL
    #   for the local forecast page on the NOAA weather website, and then return the webpage
    #   as a 'bytes' object type for use with BeautifulSoup or another similar DOM parser.
    # Provided that the response code is a 200.
    url = 'https://forecast.weather.gov/MapClick.php?lat={}&lon={}'.format(lat, lon)
    page = urlopen(url)
    if page.getcode() is 200:
        return page.read()
    else:
        return None

def scrape_noaa_page(webpage):
    # Given the bytes array of data for the NOAA website, this method will parse the page DOM
    #   and return the current conditions data within as an object for further use.
    weather = {}
    dom = BeautifulSoup(webpage, 'html5lib')
    currentConditionsRows = get_current_conditions_table_rows(dom)

    # The current forecast conditions string and temperature are stored outside of the main table,
    #   so they need to be captured with unique dom parsing statements.
    weather['current_forecast'] = dom.find('p', class_="myforecast-current").text
    weather['temperature'] = [
        format_measurement(dom.find('p', class_="myforecast-current-lrg").text, '°'),
        format_measurement(dom.find('p', class_="myforecast-current-sm").text, '°')
    ]

    # The rest of the data can be extracted from the list of rows.
    weather['humidity'] = format_humidity(currentConditionsRows[0].findChildren('td')[1].text)
    weather['wind_speed'] = format_wind_speed(currentConditionsRows[1].findChildren('td')[1].text)
    weather['barometer'] = extract_multiple_readings(currentConditionsRows[2].findChildren('td')[1].text)
    weather['dewpoint'] = extract_multiple_readings(currentConditionsRows[3].findChildren('td')[1].text, '°')
    weather['visibility'] = format_measurement(currentConditionsRows[4].findChildren('td')[1].text)
    weather['last_updated'] = currentConditionsRows[5].findChildren('td')[1].text.replace('\n', '').replace('  ', '')

    return weather

