#!/usr/bin/env python

import serial
from thebox import sdb

# NAME: Sample 9: serial reading
# DESCRIPTION: Open, configure and read data from a serial port

# Serial port:
serial_port = "/dev/ttyHSL1"  # HSL1 (source is UART) or USB0 (source is RS485 or RS232)
baudrate = 19200
data_byte = 7  # 7 or 8
parity = serial.PARITY_EVEN # EVEN, ODD, NONE
stopbits = 1

def string_to_byte(str_input):
    byte_output = []
    for char in str_input:
        byte_output.append(char)
    return byte_output
def main():
    # create a client connection
    c = sdb.Client('python sample')
    c.connect()
    
    # create a tag
    thebox_tag = c.add_tag('serial_line', sdb.DT_BYTE, count=40)

    # Reading timeout : 1 sec
    # Writing timeour : 1 sec
    with serial.Serial(port=serial_port, baudrate=baudrate, bytesize=data_byte, parity=parity, stopbits=stopbits, timeout=1, writeTimeout=1) as port_serie:
        if port_serie.isOpen():
            while True:
                line = port_serie.readline()
                if "ADCO" in line:  # we want this frame 
                    print line
                    # some processing on the line (eg. is for the TIC)
                    line = line.replace("ADCO", '')
                    line = line.replace(" ", '')
                    line = line[:-1]
                    line = bytearray(line)
                    print(line, type(line), type(line[0]))
                    thebox_tag.write(string_to_byte(line))
            
            
if __name__ == '__main__':
    main()
