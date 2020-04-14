#!/usr/bin/python2.7
"""utils.py
    Project 1: Recursive DNS client and DNS servers (miscellaneous utilities)
 
    Rutgers University
        School of Arts and Sciences
            (01:198:352) Internet Technology
            Professor Nath Badri
            Section 02

    Assignment synopsis:
        The goal of this project is to implement a simplified DNS system consisting of a client program and two server programs: RS (a simplified root DNS server) and TS (a simplified top-level DNS server). In project 0 (your first HW), you have already seen a client-server program with one socket each in the client and the server. In this project, you will extend that implementation to have two sockets in the client program. One socket will be used to communicate with RS and the other with TS.

    Copyright (c) 2020 Gemuele Aludino

    Permission is hereby granted, free of charge, to any person obtaining
    a copy of this software and associated documentation files 
    (the "Software"), to deal in the Software without restriction, including
    without limitation the rights to use, copy, modify, merge, publish,
    distribute, sublicense, and/or sell copies of the Software, and to
    permit persons to whom the Software is furnished to do so, subject to
    the following conditions:

    The above copyright notice and this permission notice shall be included
    in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BY NOT LIMITED TO THE WARRANTIES
    OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
    BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
    OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH
    THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from os import path

__author__ = "Gemuele (Gem) Aludino"
__copyright__ = "Copyright (c) 2020, Gemuele Aludino"
__date__ = "04 Mar 2020"
__license__ = "MIT"
__email0__ = "g.aludino@gmail.com"
__email1__ = "gem.aludino@rutgers.edu"
__status__ = "Release"

CHAIN_LINK = '--------------------------------------------------------------'

def file_to_list(input_file_str):
    """Creates a [str] using lines taken from a file named input_file_str;
    each element in the [str] will be suffixed with a linebreak

        Args:
            input_file_str: str
                The name of the desired file to open
        Returns:
            A [str] of lines from file input_file_str
        Raises:
            IOError if input_file_str does not exist
    """
    output_list = []
    
    try:
        with open(input_file_str, 'r') as input_file:
            output_list = [line.rstrip() for line in input_file]
            print('[utils]: SUCCESS - Input file \'{}\' opened.\n'.format(input_file_str))

            input_file.close()
    except IOError:
        print('[utils]: ERROR - Input file \'{}\' not found.\n'.format(input_file_str))
    
    return output_list

def str_to_list(input_str, delim):
    output_list = []
    
    output_list = [word.strip() for word in input_str.split(delim)]
    return output_list

def write_to_file_from_list(output_file_str, input_list, flag):
    """Writes/appends each str from input_list to a file named output_file_str, with each
    appendage suffixed with a linebreak

        Args:
            output_file_str: str
                The name of the desired output file to write to
            
            input_list: str
                The name of a list of str
            
            flag: str
                For open() call, should be 'w' for write or 'a' for append
        Returns:
            (none)
        Raises:
            (none)
    """
    message = []

    if flag is 'w':
        message = ('overwrite', 'written')
    elif flag is 'a':
        message = ('append to', 'appended')
    else:
        print('[utils]: ERROR - flag must be \'w\' for write or \'a\' for append.')
        return

    if path.isfile(output_file_str):
        print('[utils]: NOTE - Output file {} exists. Will {} existing contents.'.format(output_file_str, message[0]))
    else:
        print('[utils]: NOTE - New file {} will be created for output.'.format(output_file_str))

    with open(output_file_str, flag) as output_file:
        for line in input_list:
            output_file.write(line + '\n')

    print('[utils]: SUCCESS - Contents of successfully {} to {}.'.format(message[1], output_file_str))

class K:
    NRM = '\033[00m'
    
    class color:
        GRY = '\033[0;02m'
        RED = '\033[0;31m'
        GRN = '\033[0;32m'
        YEL = '\033[0;33m'
        BLU = '\033[0;34m'
        MAG = '\033[0;35m'
        CYN = '\033[0;36m'
        WHT = '\033[0;37m'
        
        class bold:
            RED = '\033[1;31m'
            GRN = '\033[1;32m'
            YEL = '\033[1;33m'
            BLU = '\033[1;34m'
            MAG = '\033[1;35m'
            CYN = '\033[1;36m'
            WHT = '\033[1;37m'

    class italic:
        ITL = '\033[0;03m'
    
    class underline:
        ULN = '\033[0;04m'
    
    class special:
        BNK = '\033[0;05m'
        HIL = '\033[0;07m'
    