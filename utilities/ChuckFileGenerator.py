from time import time

def generate_new_file_name():
    # More of a holder function. Right now, it just returns the time from epoch as a string.
    return '{}.ck'.format(str(int(time())))

def check_for_none(checkVal, defaultVal=0):
    # Some things return None when no data is returned, so I need to account for that.
    if checkVal is None:
        return defaultVal
    else:
        return checkVal

# Chuck file generation is split into three pieces.
# The Head instantiates the 'patch' of the composition
#   (basically, the raw materials that will be used and their direct links, if necessary).
chuckStringHead = """
SinOsc fmOsc => Gain fmAmount => blackhole;
SinOsc amLfo => blackhole;
SinOsc amModLfo => blackhole;
SinOsc freqLfo => blackhole;
SinOsc carrierOsc => Gain amp => LPF filter => JCRev reverb => dac;
"""

# The Assignment, which is where we store the variables created using the WeatherDataSonificationFormatter.
chuckStringAssignment = """
{amCarrier} => float amCarrierFreq;
{freqLfoAmount} => float freqLfoAmount;
{filterCutoff} => float filterCutoff;
{carrierFreq} => float carrierFreq;
{fmRatio} => float fmRatio;
{amModOffset} => float amModOffset;
{filterResonance} => float filterResonance;
{amModFreq} => float amModFreq;
{reverbMix} => float reverbMix;
"""

# The Composition, which is the application of the variables above, as well as the performance of the piece.
chuckStringComposition = """
carrierFreq * fmRatio => float fmOscFreq => fmOsc.freq;
amModFreq => amModLfo.freq;
reverbMix => reverb.mix;
carrierFreq + (carrierFreq * fmRatio) => filter.freq;
filterResonance => filter.Q;
freqLfoAmount/4 => freqLfo.freq;

while(true){
	(carrierFreq + (carrierFreq * freqLfoAmount * freqLfo.last())) + (fmRatio * fmOscFreq * fmOsc.last()) => carrierOsc.freq;
	amCarrierFreq + (amModFreq * amModLfo.last() * (1.0 - amModOffset)) => amLfo.freq;
	(1 + amLfo.last())/2 + amModOffset => amp.gain;
	1::samp => now;
}
"""

def create_chuck_file(sonificationValues):
    # Create Chuck File will:
    # 1. generate a new filename,
    # 2. populate the chuckStringAssignment portion of the chuck string
    # 3. open the file and write the three segments (Head, Assignment, and Composition) in order, and
    # 4. close the file and return the filename of the resultant file.
    filename = './utilities/generatedChuckFiles/{}'.format(generate_new_file_name())

    # AmCarrier=None catch
    if sonificationValues['amCarrier'] is None:
        amCarrier = 0
    else:
        amCarrier = sonificationValues['amCarrier']



    chuckStringAssignmentPopulated = chuckStringAssignment.format(
        amCarrier = check_for_none(sonificationValues['amCarrier']),
        freqLfoAmount = check_for_none(sonificationValues['freqLfoAmount']),
        filterCutoff = check_for_none(sonificationValues['filterCutoff']),
        carrierFreq = check_for_none(sonificationValues['carrierFreq']),
        fmRatio = check_for_none(sonificationValues['fmRatio']),
        amModOffset = check_for_none(sonificationValues['amModOffset']),
        filterResonance = check_for_none(sonificationValues['filterResonance']),
        amModFreq = check_for_none(sonificationValues['amModFreq']),
        reverbMix = check_for_none(sonificationValues['reverbMix'])
    )

    file = open(filename, 'w')
    file.write(chuckStringHead)
    file.write(chuckStringAssignmentPopulated)
    file.write(chuckStringComposition)
    file.close()

    return filename