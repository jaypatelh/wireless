# audiocom library: Source and sink functions
import common_srcsink
import Image
from graphs import *
import binascii
import random


class Sink:
    def __init__(self):
        # no initialization required for sink 
        print 'Sink:'

    def process(self, recd_bits):
        # Process the recd_bits to form the original transmitted
        # file. 
        # Here recd_bits is the array of bits that was 
        # passed on from the receiver. You can assume, that this 
        # array starts with the header bits (the preamble has 
        # been detected and removed). However, the length of 
        # this array could be arbitrary. Make sure you truncate 
        # it (based on the payload length as mentioned in 
        # header) before converting into a file.
        
        #get first 8 bits

        #print recd_bits
        #print recd_bits[2:8]
        #print recd_bits[2:8] + [2 6 7]

        #look at first two characters
        #if the first two bits are 00
        if recd_bits[0] == 0 and recd_bits[1] == 0:
            #get the length from the next 6 bits
            array_len = recd_bits[2:8]
            num_bytes = self.array_of_bits_to_int(array_len)

            #truncate the array for this length
            num_bits = num_bytes * 8;
            payload = recd_bits[8:(num_bits+8)]

            #pass the bits to method bits2text
            text = self.bits2text(payload)

            #print the returned value
            print "output: " + text
        # If its an image, save it as "rcd-image.png"
        elif recd_bits[0] == 0 and recd_bits[1] == 1:
            print "image"

        # Return the received payload for comparison purposes
        return payload

    def bits2text(self, bits):
        # Convert the received payload to text (string)
        num_bits = len(bits)
        num_bytes = num_bits/8

        text = ""
        for i in range(0, num_bytes):
            start = i * 8
            next_byte = bits[start:(start+8)]
            int_from_byte = self.array_of_bits_to_int(next_byte)
            next_char = chr(int_from_byte)
            text = text + next_char

        return text

    def array_of_bits_to_int(self, array_bits):
        result = 0
        for i in range(0,len(array_bits)):
            result = result << 1
            result = result | array_bits[i]

        return result

    def image_from_bits(self, bits,filename):
        # Convert the received payload to an image and save it
        # No return value required .
        return

    def read_header(self, header_bits): 
        # Given the header bits, compute the payload length
        # and source type (compatible with get_header on source)
        print '\tRecd header: ', header_bits
        print '\tLength from header: ', payload_length
        print '\tSource type: ', srctype
        return srctype, payload_length