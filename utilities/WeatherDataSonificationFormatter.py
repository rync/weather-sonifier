from utilities.SimpleScaler import simple_scaler

def generate_scaling_object(initMin, initMax, destMin, destMax):
    # Creates an object with the properties required by the SimpleScaler.simple_scaler method.
    return {
        'initMin': initMin,
        'initMax': initMax,
        'destMin': destMin,
        'destMax': destMax
    }

def get_value_by_sister_element(itemArray, matchKey='unit', matchVal='F', reqValue='value'):
    # Given a list of values, this will iterate through that list and return the desired reqValue
    #   if the matchKey/matchVal pair is present.
    for item in itemArray:
        if item[matchKey] == matchVal:
            return item[reqValue]

def generate_scaled_value(destScale, value, unit=None):
    # Intermediary method that takes in the name of the desired scaling object from scalingConversions,
    #   and then converts the provided value using the related scale.
    # A unit field is included, in case we need to use the getValueySisterElement function to pull a particular
    #   object from a list of potential values. This assumes the unit key will be 'unit'.
    if (type(value) == list) and (unit is not None):
        value = get_value_by_sister_element(value, matchVal=unit)
    else:
        value = value['value']

    return simple_scaler(
        scalingConversions[destScale]['initMin'],
        scalingConversions[destScale]['initMax'],
        scalingConversions[destScale]['destMin'],
        scalingConversions[destScale]['destMax'],
        value
    )

scalingConversions = {
    # A list of quick and dirty scaling conversions to create our sonification drone.
    'carrierFreq': generate_scaling_object(0, 100, 1277, 120), # Temperature - use Fahrenheit
    'fmRatio': generate_scaling_object(870, 1084, 1.4, 2.47), # Barometer - use mb
    'amCarrier': generate_scaling_object(0, 100, 4, 14), # Wind
    'amModFreq': generate_scaling_object(0, 100, 0.2, 3.2), # Wind
    'amModOffset': generate_scaling_object(0, 100, 0.4, 0.9), # Wind
    'reverbMix': generate_scaling_object(0, 100, 0, 1), # Humidity
    'freqLfoAmount': generate_scaling_object(0, 100, 0, 0.2), # Dewpoint
    'filterCutoff': generate_scaling_object(0, 10, 1, 6), # Visibility (Note - this will be an offset, a multiple of the current frequency, to the current base frequency)
    'filterResonance': generate_scaling_object(870, 1084, 0.04, 0.76) # Barometer - use mb
}

def convert_weather_data(weatherData):
    # Here's the master method. It takes the elements we expect to find in the output of the NOAA weather page,
    #   as parsed and repackaged by the NOAAWebScraper.scrape_noaa_page method.
    scaledValues = {}

    scaledValues['carrierFreq'] = generate_scaled_value('carrierFreq', weatherData['temperature'], 'F')
    scaledValues['fmRatio'] = generate_scaled_value('fmRatio', weatherData['barometer'], 'mb')
    if weatherData['wind_speed'] is not None:
        scaledValues['amCarrier'] = generate_scaled_value('amCarrier', weatherData['wind_speed'])
        scaledValues['amModFreq'] = generate_scaled_value('amModFreq', weatherData['wind_speed'])
        scaledValues['amModOffset'] = generate_scaled_value('amModOffset', weatherData['wind_speed'])
    else:
        scaledValues['amCarrier'], scaledValues['amModFreq'], scaledValues['amModOffset'] = None, None, None
    scaledValues['reverbMix'] = generate_scaled_value('reverbMix', weatherData['humidity'])
    scaledValues['freqLfoAmount'] = generate_scaled_value('freqLfoAmount', weatherData['dewpoint'], 'F')
    scaledValues['filterCutoff'] = generate_scaled_value('filterCutoff', weatherData['visibility'])
    scaledValues['filterResonance'] = generate_scaled_value('filterResonance', weatherData['barometer'], 'mb')

    return scaledValues


