#!/usr/bin/python2.7
"""ts.py
    Project 1: Recursive DNS client and DNS servers (top-level DNS server)
 
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

DEFAULT_INPUT_FILE_STR_TS = 'PROJI-DNSTS.txt'
DEFAULT_PORTNO_TS = 50007
HOST_NOT_FOUND_STR = 'Error:HOST NOT FOUND'

from client import file_to_list

from rs import flag
from rs import addrflag
from rs import linelist_to_dns_table
from rs import find_hostname

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
                argv[1] - ts_listen_port
                    desired port number for TS program
                argv[2] - input_file (OPTIONAL)
                    desired name of input file of entries for TS program
        Returns:
            Exit status, by default, 0 upon exit
        Raises:
            (none)
    """
    ts_portno = -1
    ts_placeholder = ''
    input_file_str = '__NONE__'

    arg_length = len(argv)

    usage_str = '\nUSAGE:\npython {} [ts_listen_port]\npython {} [ts_listen_port] [input_file]\n'.format(argv[0], argv[0])

    DNS_table = {}
    linelist = []
    queried_hostname = ''
    found = False

    if arg_length is 2:
        ts_portno = int(argv[1])
        input_file_str = DEFAULT_INPUT_FILE_STR_TS

        print(ts_portno)
    elif arg_length is 3:
        ts_portno = int(argv[1])
        input_file_str = argv[2]

        print(ts_portno, input_file_str)
    else:
        print(usage_str)
        exit()
    ##

    linelist = file_to_list(input_file_str)
    (DNS_table, ts_placeholder) = linelist_to_dns_table(linelist)

    ###
    ### connect to client here
    ###
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print('[TS]: Server socket created.')
    except socket.error:
        print('[ERROR]: {}\n'.format('Server socket open error.\n', socket.error))
        exit()
    
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    binding = ('', ts_portno)
    sock.connect(binding)

    ts_hostname = socket.gethostname()
    print('[TS]: Server hostname is: {}'.format(ts_hostname))

    ts_ipaddr = socket.gethostbyname(ts_hostname)
    print('[TS]: Server IP address is: {}\n'.format(ts_ipaddr))

    try:
        sock.connect(binding)
        print('[TS]: Attempting to connect...')
    except ConnectionRefusedError:
        print('[ERROR]: {}\n'.format('Client socket connection error.', ConnectionRefusedError))
        exit()

    print('[TS]: Connected.\n')

    ## example query from client
    queried_hostname = 'www.ibm.com' ## get it from the client.
    
    found = find_hostname(DNS_table, queried_hostname)

    if found:
        msg_out = '{} {} {}'.format(queried_hostname, DNS_table[queried_hostname][0], DNS_table[queried_hostname][1])
        
        print(msg_out) ## send to client
    else:
        msg_out = '{} - {}'.format(queried_hostname, HOST_NOT_FOUND_STR)

        print(msg_out) ## send to client

    ###
    ### disconnect from client here
    ###

    return EX_OK

if __name__ == '__main__':
    """
        Program execution begins here.
    """
    retval = main(argv)
