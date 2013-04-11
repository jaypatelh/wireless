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

        #look at first two characters
        #if the first two bits are 00
        if recd_bits[0] == 0 and recd_bits[1] == 0
            
            #get the length from the next 6 bits
            array6bit = recd_bits[2:8]
            num_bytes = self.length_from_6bit_array(self, array6bit)

            #truncate the array for this length
            num_bits = num_bytes * 8;
            payload = recd_bits[8:(num_bits+8)]

            #pass the bits to method bits2text
            text = self.bits2text(self, payload)

            #print the returned value
            print text


        # If its an image, save it as "rcd-image.png"
        else recd_bits[0] == 0 and recd_bits[1] == 1
        
            print "image"


        # Return the received payload for comparison purposes
        return rcd_payload

    def length_from_6bit_array(self, array6bit)

        array8bit = [0,0];
        array8bit = array8bit + array6bit;
        length = self.array_of_8bits_to_int(self, array8bit)

        return length


    def bits2text(self, bits):
        # Convert the received payload to text (string)
        num_bits = len(bits)
        num_bytes = num_bits/8

        text = ""
        for i in range(0, num_bytes)
            start = i * 8;
            next_byte = bits[start:(start+8)]
            int_from_byte = self.array_of_8bits_to_int(self, next_byte)
            next_char = chr(int_from_byte)
            text = text.append(next_char)

        return text

    def array_of_8bits_to_int(self, array8bit)
        
        result = 0
        for i in range(0,len(array8bit))
            result = result << 1
            result = result | array8bit[i]

        return result

    def image_from_bits(self, bits,filename):
        # Convert the received payload to an image and save it
        # No return value required .
        pass 

    def read_header(self, header_bits): 
        # Given the header bits, compute the payload length
        # and source type (compatible with get_header on source)
 
        print '\tRecd header: ', header_bits
        print '\tLength from header: ', payload_length
        print '\tSource type: ', srctype
        return srctype, payload_length