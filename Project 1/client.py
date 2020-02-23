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

def query_servers(cl_sock, rs_binding, hostname_list, ts_portno):
    rs_hostname = rs_binding[0]
    rs_portno = rs_binding[1]

    cl_sock_ts = 0
    ts_hostname = ''
    ts_binding = ('', '')
    
    resolved_list = []
    queried_hostname = ''

    msg_in = ''
    msg_out = ''

    data_in = ''
    data_out = ''

    reply_elems = []

    for elem in hostname_list:
        queried_hostname = elem

        msg_out = queried_hostname
        data_out = msg_out.encode('utf-8')
        cl_sock.send(data_out)
        print('[client]: outgoing to {}: {}'.format(rs_hostname, queried_hostname))

        data_in = cl_sock.recv(128)
        msg_in = data_in.decode('utf-8')
        print('[client]: incoming from {}: {}'.format(rs_hostname, msg_in))

        reply_elems = str_to_list(msg_in, ' ')

        if reply_elems[2] == DNS_table.flag.A.value:
            resolved_list.append(msg_in)
        elif reply_elems[2] == DNS_table.flag.NS.value:
            ts_hostname = reply_elems[0]

            cl_sock_ts = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            ts_binding = (ts_hostname, ts_portno)
            cl_sock_ts.connect(ts_binding)

            msg_out = queried_hostname
            data_out = msg_out.encode('utf-8')
            cl_sock_ts.send(data_out)
            print('[client] outgoing to {}: {}'.format(ts_hostname, queried_hostname))

            data_in = cl_sock_ts.recv(128)
            msg_in = data_in.decode('utf-8')
            print('[client]: incoming from {}: {}'.format(ts_hostname, msg_in))

            resolved_list.append(msg_in)
            cl_sock_ts.close()

        print('')

    return resolved_list

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
    arg_length = len(argv)

    usage_str = '\nUSAGE:\npython {} [rs_hostname] [rs_listen_port] [ts_listen_port]\npython {} [rs_hostname] [rs_listen_port] [ts_listen_port] [input_file_name]\npython {} [rs_hostname] [rs_listen_port] [ts_listen_port] [input_file_name] [output_file_name]\n'.format(argv[0], argv[0], argv[0])

    cl_sock = 0
    binding = ('', '')
    
    rs_hostname = ''
    rs_portno = 0
    rs_binding = ('', '')

    input_file_str = DEFAULT_INPUT_FILE_STR_HNS
    output_file_str = DEFAULT_OUTPUT_FILE_STR_RESOLVED

    hostname_list = []
    resolved_list = []

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

    cl_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    rs_binding = (rs_hostname, rs_portno)
    cl_sock.connect(rs_binding)

    resolved_list = query_servers(cl_sock, rs_binding, hostname_list, ts_portno)
    append_to_file_from_list(output_file_str, resolved_list)

    print('')
    return EX_OK

if __name__ == '__main__':
    """
        Program execution begins here.
    """
    retval = main(argv)
