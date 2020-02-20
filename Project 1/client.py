#!/usr/bin/python2.7
"""client.py
    Project 1: Recursive DNS client and DNS servers (client socket portion)
 
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

### Run order: ts.py, rs.py, client.py

# remember to remove unused imports
from os import EX_OK
from sys import argv
from enum import Enum

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
            print('[SUCCESS]: Input file \'{}\' opened.\n'.format(input_file_str))
    except IOError:
        print('[ERROR]: Input file \'{}\' not found.\n'.format(input_file_str))
        exit()
    
    return output_list

from rs import DEFAULT_PORTNO_RS
from rs import flag
from rs import addrflag

DEFAULT_INPUT_FILE_STR_HNS = 'PROJI-HNS.txt'
DEFAULT_OUTPUT_FILE_STR_RESOLVED = 'RESOLVED.txt'

from ts import DEFAULT_PORTNO_TS
from ts import HOST_NOT_FOUND_STR

import socket
import threading
import time
import random

__author__ = "Gemuele (Gem) Aludino"
__copyright__ = "Copyright (c) 2020, Gemuele Aludino"
__date__ = "04 Mar 2020"
__license__ = "MIT"
__email0__ = "g.aludino@gmail.com"
__email1__ = "gem.aludino@rutgers.edu"
__status__ = "Debug"

def main(argv):
    """Main function, where client function is called

        Args:
            Command line arguments (as per sys.argv)
                argv[1] - rs_hostname
                    desired hostname for RS program
                argv[2] - rs_listen_port
                    desired port number for RS program
                argv[3] - ts_portno
                    desired port number for TS program
                argv[4] - input_file_name (OPTIONAL)
                    desired name of input file (queried_hostnames)
                argv[5] - output_file_name (OPTIONAL)
                    desired name of output file
        Returns:
            Exit status, by default, 0 upon exit
        Raises:
            (none)
    """
    """ERASE ME WHEN DONE
    type1 = flag.NS
    if type1 is flag.A:
        print('match')
    else:
        print('mismatch')
    ERASE ME WHEN DONE"""
    arg_length = len(argv)

    usage_str = '\nUSAGE:\npython {} [rs_hostname] [rs_listen_port] [ts_listen_port]\npython {} [rs_hostname] [rs_listen_port] [ts_listen_port] [input_file_name]\npython {} [rs_hostname] [rs_listen_port] [ts_listen_port] [input_file_name] [output_file_name]\n'.format(argv[0], argv[0], argv[0])

    rs_portno = DEFAULT_PORTNO_RS
    ts_portno = DEFAULT_PORTNO_TS

    rs_hostname = ''
    ts_hostname = ''

    input_file_str = DEFAULT_INPUT_FILE_STR_HNS
    output_file_str = DEFAULT_OUTPUT_FILE_STR_RESOLVED

    hostname_list = []

    if arg_length is 4:
        rs_hostname = argv[1]

        rs_portno = int(argv[2])
        ts_portno = int(argv[3])

        print(rs_hostname, rs_portno, ts_portno)
    elif arg_length is 5:
        rs_hostname = argv[1]

        rs_portno = int(argv[2])
        ts_portno = int(argv[3])

        input_file_str = argv[4]

        print(rs_hostname, rs_portno, ts_portno, input_file_str)
    elif arg_length is 6:
        rs_hostname = argv[1]

        rs_portno = int(argv[2])
        ts_portno = int(argv[3])

        input_file_str = argv[4]
        output_file_str = argv[5]

        print(rs_hostname, rs_portno, ts_portno, input_file_str, output_file_str)
    else:
        print(usage_str)
        exit()

    hostname_list = file_to_list(input_file_str)

    for elem in hostname_list:
        rs_hostname = elem
        print(rs_hostname) ## send to rs

        # if rs_hostname not found then assign ts_hostname
        # to portion of received string

    ## Use this if string with NS is sent back.
    ## check to see if ts_hostname was specified in RS's DNS_table
    """
    if ts_hostname == '__NONE__':
        print('[ERROR]: RS server has not specified a hostname for the TS server.')
        exit()
    """

    """
    client connects to RS first using rs_portno
        sends rs_hostname to RS socket
        waiting on string received...

    if string received has 'NS' at last portion of string
        match: no
        ts_hostname = first portion of string received
    else if string received has 'A' at last portion of string
        match: yes
    
    if match:
        print string received from RS as is
        append string to DEFAULT_OUTPUT_FILE_STR_RESOLVED
        done.
    else:
        client connects to TS using ts_portno
            sends ts_hostname to TS socket
            waiting on string received...

    if string received has 'HOST NOT FOUND' at last portion of string:
        match: no
    else:
        match: yes

    print string received from TS as is
    append string to DEFAULT_OUTPUT_FILE_STR_RESOLVED
    done.
    
    """

    return EX_OK

if __name__ == '__main__':
    """
        Program execution begins here.
    """
    retval = main(argv)
