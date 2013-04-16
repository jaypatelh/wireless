# audiocom library: Source and sink functions
import common_srcsink as common
import Image
from PIL import Image
from graphs import *
import binascii
import random
import os

class Source:
    TEXT = 0
    IMAGE = 1
    MONOTONE = 2

    def __init__(self, monotone, filename=None):
        # The initialization procedure of source object
        self.monotone = monotone
        self.fname = filename
        print 'Source: '

    def process(self):
        # Form the databits, from the filename 
        if self.fname is not None:
            if self.fname.endswith('.png') or self.fname.endswith('.PNG'): # image
                # yo
                img = Image.open(self.fname)
                img.convert("L") # make sure it is grayscale
                dim = img.size()
                header = get_img_header(dim[0], dim[1], 7)
                pixel_list = list(img.getdata())
                payload = bits_from_image(pixel_list)
                databits = header + payload
            else:
                size = int(os.path.getsize(self.fname))
                header = self.get_text_header(size, 6)
                payload = self.text2bits(self.fname)
                databits = header + payload
                prnt_databits = [str(bit) for bit in databits]
                #print "databits: " + ", ".join(prnt_databits)
                #print "len: " + str(len(prnt_databits))
        else:
            # Send monotone (the payload is all 1s for 
            # monotone bits)
            return
        return payload, databits

    def text2bits(self, filename):
        # Given a text file, convert to bits
        f = open(filename)
        ascii_array = []
        # convert each char to its ascii representation first
        for line in f:
            for char in line:
                ascii_array.append(ord(char))

        # convert each ascii number to a 8 bit array
        bits = []
        for elem in ascii_array:
            bits += self.int_to_bit_array(elem, 8)

        return bits

    def int_to_bit_array(self, num, num_bits):
        bits = []
        for i in range(num_bits):
            bits.insert(0, (num >> i) & 1)
        return bits

    def bits_from_image(self, pixel_list):
        # Given an image, convert to bits
        bits = []
        for pix in pixel_list:
            bits += self.int_to_bit_array(pix[0], 8)
            bits += self.int_to_bit_array(pix[1], 8)
        return bits

    def get_text_header(self, payload_length, num_bits):
        # Given the payload length and the type of source 
        # (image, text, monotone), form the header

        # initialize databits with 0, 0 to signify text file
        header = [0, 0]
        
        # append payload size encoded in next num_bits bits
        header += self.int_to_bit_array(payload_length, num_bits)
        return header
    
    def get_img_header(self, width, height, num_bits_each):
        header = [0, 1]
        header += self.int_to_bit_array(width, num_bits_each)
        header += self.int_to_bit_array(height, num_bits_each)
        return header