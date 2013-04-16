import numpy
import math
import operator

# Methods common to both the transmitter and receiver.
def hamming(s1,s2):
    # Given two binary vectors s1 and s2 (possibly of different 
    # lengths), first truncate the longer vector (to equalize 
    # the vector lengths) and then find the hamming distance
    # between the two. Also compute the bit error rate  .
    # BER = (# bits in error)/(# total bits )

    # truncate the longer one
    if len(s1) < len(s2):
    	s2 = s2[:len(s1)]
    elif len(s2) < len(s1):
    	s1 = s1[:len(s2)]

    hamming_d = 0
    for i in range(len(s1)):
    	if s1[i] != s2[i]:
    		hamming_d += 1

    ber = float(hamming_d) / float(len(s1))
    return hamming_d, ber