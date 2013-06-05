import sys
import math
import numpy as np
import scipy.cluster.vq
import common_txrx as common
from numpy import linalg as LA
import receiver_mil3

class Receiver:
    def __init__(self, carrier_freq, samplerate, spb):
        '''
        The physical-layer receive function, which processes the
        received samples by detecting the preamble and then
        demodulating the samples from the start of the preamble 
        sequence. Returns the sequence of received bits (after
        demapping)
        '''
        self.fc = carrier_freq
        self.samplerate = samplerate
        self.spb = spb
        self.preamble = [1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1]
        print 'Receiver: '

    def detect_threshold(self, demod_samples):
        '''
        Calls the detect_threshold function in another module.
        No need to touch this.
        ''' 
        return receiver_mil3.detect_threshold(demod_samples)
 
    def detect_preamble(self, demod_samples, thresh, one):
        '''
        Find the sample corresp. to the first reliable bit "1"; this step 
        is crucial to a proper and correct synchronization w/ the xmitter.
        '''

        '''
        First, find the first sample index where you detect energy based on the
        moving average method described in the milestone 2 description.
        '''
        # Fill in your implementation of the high-energy check procedure
        energy_offset = 0
        found = False
        while energy_offset < len(demod_samples)-self.spb:
            interval = demod_samples[energy_offset:energy_offset+self.spb]  # take interval of spb samples starting from energy_offset
            central_samples = interval[self.spb/4:(3*self.spb)/4] # take central spb/2 samples
            avg = float(sum(central_samples))/float(len(central_samples))
            if avg > (one+thresh)/2:
                found = True
                break
            energy_offset += 1

        if not found:
            print '*** ERROR: Could not detect any ones (so no preamble). ***'
            print '\tIncrease volume / turn on mic?'
            print '\tOr is there some other synchronization bug? ***'
            sys.exit(1)

        '''
        Then, starting from the demod_samples[offset], find the sample index where
        the cross-correlation between the signal samples and the preamble 
        samples is the highest. 
        '''
        # Fill in your implementation of the cross-correlation check procedure
        # construct preamble_samples to do the cross-correlation
        num_samples = len(self.preamble)*self.spb
        preamble_samples = np.empty(num_samples)
        curr_num = 0
        for bit_number in range(len(self.preamble)):
            if self.preamble[bit_number] == 0:
                for i in range(self.spb):
                    preamble_samples[i+(self.spb*curr_num)] = 0
            elif self.preamble[bit_number] == 1:
                for i in range(self.spb):
                    preamble_samples[i+(self.spb*curr_num)] = 1
            curr_num += 1

        preamble_offset = 0
        range_to_check_against = demod_samples[energy_offset:energy_offset+3*len(preamble_samples)]

        max_correlation_offset = 0
        max_correlation = 0
        for i in range(2*len(preamble_samples)):
            cc = np.correlate(preamble_samples, range_to_check_against[i:i+len(preamble_samples)])[0]
            if cc > max_correlation:
                max_correlation = cc
                max_correlation_offset = i

        preamble_offset = max_correlation_offset
        
        '''
        [preamble_offset] is the additional amount of offset starting from [offset],
        (not a absolute index reference by [0]). 
        Note that the final return value is [offset + pre_offset]
        '''

        return energy_offset + preamble_offset
        
    def demap_and_check(self, demod_samples, preamble_start):
        '''
        Demap the demod_samples (starting from [preamble_start]) into bits.
        1. Calculate the average values of midpoints of each [spb] samples
           and match it with the known preamble bit values.
        2. Use the average values and bit values of the preamble samples from (1)
           to calculate the new [thresh], [one], [zero]
        3. Demap the average values from (1) with the new three values from (2)
        4. Check whether the first [preamble_length] bits of (3) are equal to
           the preamble. If it is proceed, if not terminate the program. 
        Output is the array of data_bits (bits without preamble)
        '''

        # build table
        vals_one = []
        vals_zero = []
        #np_demod_samples = np.array(demod_samples)

        # get average of each spb chunk
        avgs_for_preamble_bits = []
        for i in range(len(self.preamble)):
            curr_bit_samples = demod_samples[preamble_start+(self.spb*i):preamble_start+(self.spb*(i+1))] # take interval of spb samples starting from energy_offset
            central_samples = curr_bit_samples[(self.spb/4):((3*self.spb)/4)] # take central spb/2 samples
            avg = float(sum(central_samples))/float(len(central_samples))
            avgs_for_preamble_bits.append(float(avg))
            if self.preamble[i] == 1:
                vals_one.append(float(avg))
            elif self.preamble[i] == 0:
                vals_zero.append(float(avg))

        # compute threshold
        average_one = float(sum(vals_one))/float(len(vals_one))
        average_zero = float(sum(vals_zero))/float(len(vals_zero))
        new_threshold = float(average_one+average_zero)/2.0

        # check that preamble is correct
        recd_preamble = []
        for i in range(len(self.preamble)):
            if avgs_for_preamble_bits[i] >= new_threshold:
                curr_bit = 1
            elif avgs_for_preamble_bits[i] < new_threshold:
                curr_bit = 0

            if curr_bit != self.preamble[i]:
                # preamble is incorrect
                print 'Could not detect preamble.'
                return

            print curr_bit

            recd_preamble.append(curr_bit)

        #print 'recd preamble: '
        #print recd_preamble
        #print 'preamble: '
        #print self.preamble

        # demap all the other samples
        data_samples = demod_samples[preamble_start+(len(self.preamble)*self.spb):]
        num_bits = len(data_samples)/self.spb
        data_bits = np.empty(num_bits)
        for i in range(num_bits):
            curr_bit_samples = data_samples[self.spb*i:self.spb*(i+1)]
            central_samples = curr_bit_samples[self.spb/4:(3*self.spb)/4]
            avg = float(sum(central_samples))/float(len(central_samples))

            if avg >= new_threshold:
                data_bits[i] = 1
            elif avg < new_threshold:
                data_bits[i] = 0

        return data_bits # without preamble

    def demodulate(self, samples):
        return common.demodulate(self.fc, self.samplerate, samples)