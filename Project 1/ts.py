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

from rs import flag
from rs import addrflag
from rs import file_to_list

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
    input_file_str = '__NONE__'

    arg_length = len(argv)

    usage_str = '\nUSAGE:\npython {} [ts_listen_port]\npython {} [ts_listen_port] [input_file]\n'.format(argv[0], argv[0])

    DNS_table = {}
    linelist = []
    queried_hostname = ''
    found = False

    ## functionalize this - checkargs
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
    ##

    ### convert input file into a list of strings
    linelist = file_to_list(input_file_str)

    ## functionalize this
    ### each field is separated by whitespace,
    ### normal case (A or NS) will have 3 fields.
    ### any other case (not 3 fields) will be treated as an error.
    for line in linelist:
        result = [x.strip() for x in line.split(' ')]

        if len(result) != 3:
            DNS_table[result[0]] = addrflag(result[1], HOST_NOT_FOUND_STR)
        else:
            DNS_table[result[0]] = addrflag(result[1], result[2])
    ##

    ## example query from client
    queried_hostname = 'www.ibm.com' ## get it from the client.
    found = False

    ## functionalize this - table search
    for key, value in DNS_table.iteritems():
        if key == queried_hostname:
            msg_out = '{} {} {}'.format(key, value.ipaddr, value.flagtype)
            print(msg_out)

            found = True
            break
    ##

    if not found:
        msg_out = '{} {} {}'.format(queried_hostname, '-', HOST_NOT_FOUND_STR)
        print(msg_out) ## replace with send to client

    return EX_OK

if __name__ == '__main__':
    """
        Program execution begins here.
    """
    retval = main(argv)
