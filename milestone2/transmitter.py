import math
import common_txrx as common
import numpy as np

class Transmitter:
    def __init__(self, carrier_freq, samplerate, one, spb, silence):
        self.fc = carrier_freq  # in cycles per sec, i.e., Hz
        self.samplerate = samplerate
        self.one = one
        self.spb = spb
        self.silence = silence
        self.preamble = np.array([1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1])
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

        silence_bits = np.zeros(self.silence, dtype=int)
        preamble_bits = np.array(self.preamble)
        data_bits = np.array(databits)
        databits_with_preamble = np.concatenate([silence_bits, preamble_bits, data_bits])

        return databits_with_preamble

    def bits_to_samples(self, databits_with_preamble):
        '''
        Convert each bits into [spb] samples. 
        Sample values for bit '1', '0' should be [one], 0 respectively.
        Output should be an array of samples.
        '''
        # fill in your implemenation

        num_samples = len(databits_with_preamble)*self.spb
        samples_array = np.empty(num_samples)
        curr_num = 0
        for bit_number in range(len(databits_with_preamble)):
            if databits_with_preamble[bit_number] == 0:
                for i in range(self.spb):
                    samples_array[i+(self.spb*curr_num)] = 0
            elif databits_with_preamble[bit_number] == 1:
                for i in range(self.spb):
                    samples_array[i+(self.spb*curr_num)] = self.one
            curr_num += 1

        return samples_array

    def modulate(self, samples):
        '''
        Calls modulation function. No need to touch it.
        '''
        return common.modulate(self.fc, self.samplerate, samples)