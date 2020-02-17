#!/usr/bin/python2.7
"""rs.py
    Project 1: Recursive DNS client and DNS servers (root DNS server)
 
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
from collections import namedtuple

class flag(Enum):
    HOST_NOT_FOUND = 'Error:HOST NOT FOUND'
    A = 'A'
    NS = 'NS'

addrflag = namedtuple("addrflag", ["ipaddr", "flagtype"])

def file_to_list(input_file_str):
    """Creates a [str] using lines taken from a file named input_file_str;
    each element in the [str] will be suffixed with a linebreak

        Args:
            input_file_str: str
                The name of the desired file to open
        Returns:
            A [str] of lines from file input_file_str
        Raises:
            FileNotFoundError if input_file_str does not exist
    """
    output_list = []
    
    try:
        with open(input_file_str, 'r') as input_file:
            output_list = [line.rstrip() for line in input_file]
            print('[SUCCESS]: Input file \'{}\' opened.\n'.format(input_file_str))
    except FileNotFoundError:
        print('[ERROR]: Input file \'{}\' not found.\n'.format(input_file_str))
    
    return output_list

from ts import HOST_NOT_FOUND_STR

DEFAULT_INPUT_FILE_STR_RS = 'PROJI-DNSRS.txt'
DEFAULT_PORTNO_RS = 8345
DEFAULT_TS_HOSTNAME = 'kill.cs.rutgers.edu'

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

class entry:
    hostname = ''
    af_pair = addrflag

    def __init__(self, hostname, af_pair):
        self.hostname = hostname
        self.af_pair = af_pair

    def __str__(self):
        fmt = ''
        ipaddr = self.af_pair.ipaddr
        flagtype = self.af_pair.flagtype

        if self.af_pair.flagtype is flag.HOST_NOT_FOUND:
            fmt = '{} - {}'.format(self.hostname, HOST_NOT_FOUND_STR)
        else:
            fmt = '{} {} {}'.format(self.hostname, ipaddr, flagtype)

        return fmt

def main(argv):
    """Main function, where client function is called

        Args:
            Command line arguments (as per sys.argv)
        Returns:
            Exit status, by default, 0 upon exit
        Raises:
            (none)
    """
    rs_portno = -1

    arg_length = len(argv)
    usage_str = '\nUSAGE:\npython {} [rs_listen_port]\n'.format(argv[0])

    if arg_length is 2:
        rs_portno = int(argv[1])
        print(rs_portno)
    else:
        print(usage_str)

    
    ### populate the local DNS_table with the provided input file.

    ### convert input file into a list of strings
    DNS_table = {}
    linelist = file_to_list(DEFAULT_INPUT_FILE_STR_RS)

    ### each field is separated by whitespace,
    ### normal case (A or NS) will have 3 fields.
    ### any other case (not 3 fields) will be treated as an error.
    for line in linelist:
        result = [x.strip() for x in line.split(' ')]

        if len(result) != 3:
            DNS_table[result[0]] = addrflag(result[1], HOST_NOT_FOUND_STR)
        else:
            DNS_table[result[0]] = addrflag(result[1], result[2])

    ## example query from client
    queried_hostname = 'www.ibm.com'
    found = False

    for key, value in DNS_table.iteritems():
        if key == queried_hostname:
            msg_out = '{} {} {}'.format(key, value.ipaddr, value.flagtype)
            print(msg_out)
            found = True
            break

    if not found:
        ts_hostname = 'theTShostname'
        msg_out = '{} {} {}'.format(ts_hostname, '-', flag.NS.value)
        print(msg_out)

        ## ts will do search with queried_hostname
        ## if ts succeeds, do what rs would have done above
        ## if ts fails,
        ## msg_out = '{} {} {}'.format(queried_hostname, '-', HOST_NOT_FOUND_STR)
        ## then send msg_out
        
    return EX_OK

if __name__ == '__main__':
    """
        Program execution begins here.
    """
    retval = main(argv)
