import numpy as np
import math
import operator

# Methods common to both the transmitter and receiver
def modulate(fc, samplerate, samples):
  '''
  A modulator that multiplies samples with a local carrier 
  of frequency fc, sampled at samplerate
  '''

  result = []

  omega_c = 2*np.pi*((1.0*fc)/samplerate)
  for n in np.arange(0, len(samples)):
    result += [samples[n]*math.cos(omega_c*n)]

  result = np.array(result)

  return result

def demodulate(fc, samplerate, samples):
  '''
  A demodulator that performs quadrature demodulation
  '''
  
  result = []

  omega_c = 2*np.pi*((1.0*fc)/samplerate)
  for n in np.arange(0, len(samples)):
    result += [samples[n] * np.exp(1j*omega_c*n)]

  result = np.array(result)

  result = lpfilter(result, omega_c)

  return result

def lpfilter(samples_in, omega_cut):
  '''
  A low-pass filter of frequency omega_cut.
  '''
  # set the filter unit sample response
  L = 50
  
  # get the hn_array which is the unit sample response in the values -L to L
  hn_array = []
  for n in np.arange(-L, 0):
    hn_array += [(math.sin(omega_cut*n))/(n*np.pi)]

  hn_array += [omega_cut/np.pi]

  for n in np.arange(1, L+1):
    hn_array += [(math.sin(omega_cut*n))/(n*np.pi)]

  padding = np.zeros(50)
  samples = np.append(padding, samples_in)
  samples = np.append(samples, padding)

  result = []
  for i in np.arange(len(samples_in)):
    start_index = 0+i
    result += [abs(np.dot(hn_array, (samples[start_index:(start_index+len(hn_array))])))]

  result = np.array(result)
  # compute the demodulated samples
  return result