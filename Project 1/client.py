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

from utils import file_to_list
from utils import str_to_list
from utils import append_to_file_from_list

from dns_module import DNS_table

from rs import DEFAULT_PORTNO_RS 
from ts import DEFAULT_PORTNO_TS

from os import EX_OK
from os import path
from sys import argv
from enum import Enum

DEFAULT_INPUT_FILE_STR_HNS = 'PROJI-HNS.txt'
DEFAULT_OUTPUT_FILE_STR_RESOLVED = 'RESOLVED.txt'

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

    queried_hostname = ''
    ts_hostname = ''

    input_file_str = DEFAULT_INPUT_FILE_STR_HNS
    output_file_str = DEFAULT_OUTPUT_FILE_STR_RESOLVED

    hostname_list = []
    resolved = DNS_table()

    msg_in = ''
    msg_out = ''

    data_in = ''
    data_out = ''

    cl_sock = 0
    cl_binding = ('', '')
    cl_hostname = ''
    cl_ipaddr = ''
    
    if arg_length is 4:
        rs_hostname = argv[1]

        rs_portno = int(argv[2])
        ts_portno = int(argv[3])
    elif arg_length is 5:
        rs_hostname = argv[1]

        rs_portno = int(argv[2])
        ts_portno = int(argv[3])

        input_file_str = argv[4]
    elif arg_length is 6:
        rs_hostname = argv[1]

        rs_portno = int(argv[2])
        ts_portno = int(argv[3])

        input_file_str = argv[4]
        output_file_str = argv[5]
    else:
        print(usage_str)
        exit()

    hostname_list = file_to_list(input_file_str)

    ###
    ### connect to RS here
    ###

    for elem in hostname_list:
        queried_hostname = elem
        print(queried_hostname) ## send to rs

        """
        send queried_hostname to RS
        reply = recv(...)
        reply_elems = str_to_list(reply, ' ')
    
        if reply_elems[2] == DNS_table.flag.A.value:
            resolved.append_from_str(reply)
        elif reply_elems[2] == DNS_table.flag.NS.value:
            ts_hostname = reply_elems[0]

            ###
            ### connect to TS here
            ###

            if ts_hostname == '__NONE__':
                print('[client]: ERROR - RS has not specified a hostname for the TS server.')
                
                exit()
            else:
                send queried_hostname to TS
                reply = recv(...)
                resolved.append_from_str(reply)
        """

    resolved.write_to_file(output_file_str)

    """
    table = DNS_table()
    table.append_from_str('myhost 198.12.2.1 A')
    table.ts_hostname = 'TS hostname'
    print(table.ts_hostname)

    table.append('hostname', DNS_table.addrflag('ipaddr', DNS_table.flag.A.value))
    table.append_from_str('localhost 198.168.1.1 A')

    table.remove('localhost')
    table.clear()
    table.write_to_file('newfile.txt')
    """

    ## Use this if string with NS is sent back.
    ## check to see if ts_hostname was specified in RS's DNS_table
    """
    if ts_hostname == '__NONE__':
        print('[ERROR]: RS server has not specified a hostname for the TS server.')
        exit()
    """

    print('')
    return EX_OK

if __name__ == '__main__':
    """
        Program execution begins here.
    """
    retval = main(argv)
