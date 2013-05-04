import math
import common_txrx as common
import numpy

class Transmitter:
    def __init__(self, carrier_freq, samplerate, one, spb, silence):
        self.fc = carrier_freq  # in cycles per sec, i.e., Hz
        self.samplerate = samplerate
        self.one = one
        self.spb = spb
        self.silence = silence
        print 'Transmitter: '

    def add_preamble(self, databits):
        '''
        Prepend the array of source bits with silence bits and preamble bits
        The recommended preamble bits is 
        [1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1]
        The output should be the concatenation of arrays of
            [silence bits], [preamble bits], and [databits]
        '''
        # fill in your implementation

        silence_bits = [];
        for s in range(0, self.silence):
            silence_bits = silence_bits + [0]

        preamble_bits = self.get_preamble
        databits_with_preamble = silence_bits + preamble_bits + databits

        return databits_with_preamble

    def get_preamble
        return [1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1]

    def bits_to_samples(self, databits_with_preamble):
        '''
        Convert each bits into [spb] samples. 
        Sample values for bit '1', '0' should be [one], 0 respectively.
        Output should be an array of samples.
        '''
        # fill in your implemenation

        samples_array = []

        for bit_number in range(0, databits_with_preamble.length):
                if(databits_with_preamble[bit_number] == 0):
                    for sample_number in range(0, self.spb):
                        samples_array = samples_array + [0]
                else if (databits_with_preamble[bit_number] == 1):
                    for sample_number in range(0, self.spb):
                        samples_array = samples_array + [one]

        samples = np.array(samples_array)
        return samples
        

    def modulate(self, samples):
        '''
        Calls modulation function. No need to touch it.
        '''
        return common.modulate(self.fc, self.samplerate, samples)
