
SinOsc fmOsc => Gain fmAmount => blackhole;
SinOsc amLfo => blackhole;
SinOsc amModLfo => blackhole;
SinOsc freqLfo => blackhole;
SinOsc carrierOsc => Gain amp => LPF filter => JCRev reverb => dac;

4.6 => float amCarrierFreq;
0.13 => float freqLfoAmount;
6.0 => float filterCutoff;
467.1 => float carrierFreq;
2.1165 => float fmRatio;
0.43000000000000005 => float amModOffset;
0.5221308411214951 => float filterResonance;
0.38 => float amModFreq;
0.84 => float reverbMix;

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
