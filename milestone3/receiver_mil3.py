import numpy as np
import math
import operator
import random
import scipy.cluster.vq
import common_txrx as common

def detect_threshold(demod_samples): 
        # Now, we have a bunch of values that, for on-off keying, are
        # either near amplitude 0 or near a positive amplitude
        # (corresp. to bit "1").  Because we don't know the balance of
        # zeroes and ones in the input, we use 2-means clustering to
        # determine the "1" and "0" clusters.  In practice, some
        # systems use a random scrambler to XOR the input to balance
        # the zeroes and ones. We have decided to avoid that degree of
        # complexity in audiocom (for the time being, anyway).

	# initialization
  center1 = min(demod_samples)
  center2 = max(demod_samples) 
  prev1 = 0
  prev2 = 0

  # insert code to implement 2-means clustering 	
  while (not((center1 == prev1) and (center2 == prev2))):
    prev1 = center1
    prev2 = center2
    sum1 = 0
    sum2 = 0
    count1 = 0
    count2 = 0

    for n in np.arange(0, len(demod_samples)):
      curr = demod_samples[n];
      if(abs(curr-prev1) <= abs(curr-prev2)):
        sum1 += curr
        count1 += 1
      else:
        sum2 += curr
        count2 += 1

    center1 = sum1/count1
    center2 = sum2/count2

  zero = center1
  one = center2

  # insert code to associate the higher of the two centers 
  # with one and the lower with zero
  
  print "Threshold for 1:"
  print one
  print " Threshold for 0:"
  print zero

  # insert code to compute thresh
  thresh = (zero + one)/2

  return one, zero, thresh

    
