# audiocom library: Source and sink functions
import common_srcsink
from PIL import Image
from graphs import *
import binascii
import random

class Sink:

    def __init__(self):
        # no initialization required for sink 
        print 'Sink:'

    def process(self, recd_bits):
        """
        Process the recd_bits to form the original transmitted file. 
        Here recd_bits is the array of bits that was 
        passed on from the receiver. You can assume, that this 
        array starts with the header bits (the preamble has 
        been detected and removed). However, the length of 
        this array could be arbitrary. Make sure you truncate 
        it (based on the payload length as mentioned in 
        header) before converting into a file.
        """
        payload = []
        
        #look at first two characters
        #if the first two bits are 00
        if recd_bits[0] == 0 and recd_bits[1] == 0:
            #get the length from the next 6 bits
            array_len = recd_bits[2:18]
            num_bytes = self.array_of_bits_to_int(array_len)

            #truncate the array for this length
            num_bits = num_bytes * 8;
            payload = recd_bits[18:(18+num_bits)]

            #pass the bits to method bits2text
            text = self.bits2text(payload)

            #print the returned value
            print text

        # If its an image, save it as "rcd-image.png"
        elif recd_bits[0] == 0 and recd_bits[1] == 1:
            #get the length from the next 14 bits
            array_width = recd_bits[2:9]
            image_width = self.array_of_bits_to_int(array_width)
            array_height = recd_bits[9:16]
            image_height = self.array_of_bits_to_int(array_height)

            image_size = (image_width, image_height)

            #Every pixel is 2 bytes and num_pixels = width*height
            num_bytes = image_width * image_width * 2;

            #truncate the array for this length
            num_bits = num_bytes * 8;
            payload = recd_bits[16:(num_bits+16)]

            #pass the bits to method bits2text
            if (self.image_from_bits(payload, image_size, "recd-image.png") == -1):
                print "Error reading image"

        elif recd_bits[0] == 1 and recd_bits[1] == 0: # i.e. monotone
            array_len = recd_bits[2:18]
            num_ones = self.array_of_bits_to_int(array_len)
            payload = recd_bits[18:18+num_ones]

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

    def image_from_bits(self, bits, dimensions, filename):
        # Convert the received payload to an image and save it

        image_file = Image.new("LA", dimensions)

        image_data = []
        for x in range(0, dimensions[0]):
            for y in range(0, dimensions[1]):
                pixel_num = (x * dimensions[1]) + y
                start = pixel_num * 16
                color_bits = bits[start:(start+8)]
                color_num = self.array_of_bits_to_int(color_bits)
                alpha_bits = bits[(start+8):(start+16)]
                alpha_num = self.array_of_bits_to_int(alpha_bits)
                next_pixel = (color_num, alpha_num)
                image_data.append(next_pixel)

        image_file.putdata(image_data)
        image_file.save(filename)

    def read_header(self, header_bits): 
        # Given the header bits, compute the payload length
        # and source type (compatible with get_header on source)
        print '\tRecd header: ', header_bits
        print '\tLength from header: ', payload_length
        print '\tSource type: ', srctype
        return srctype, payload_length