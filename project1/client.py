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

from utils import file_to_list
from utils import str_to_list
from utils import write_to_file_from_list
from utils import CHAIN_LINK

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
__status__ = "Release"

def query_servers(rs_hostname, rs_portno, hostname_list, ts_portno):
    client_ipaddr = ''
    client_hostname = ''
    
    cl_sock_rs = 0
    cl_sock_ts = 0

    rs_ipaddr = ''

    ts_hostname = ''
    ts_ipaddr = ''
    ts_binding = ('', '')
    
    resolved_list = []
    queried_hostname = ''

    msg_in = ''
    msg_out = ''

    data_in = ''
    data_out = ''

    delimiter = ' '
    reply_elems = []

    ts_connected = False

    try:
        cl_sock_rs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except EnvironmentError:
        print('[client]: ERROR - client socket open error.\n')
        exit()

    cl_sock_rs.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    print('[client]: Opened new datagram socket.\n')

    rs_binding = (rs_hostname, rs_portno)

    try:
        socket.gethostbyname(rs_hostname)
        cl_sock_rs.connect(rs_binding)
    except EnvironmentError:
        print('[client]: ERROR - Unable to connect to RS server \'{}\'\n'.format(rs_hostname))
        exit()

    client_hostname = socket.gethostname()
    client_ipaddr = socket.gethostbyname(client_hostname)

    print('[client]: Client hostname is \'{}\'.'.format(client_hostname))
    print('[client]: Client IP address is \'{}\'.\n'.format(client_ipaddr))

    for elem in hostname_list:
        ts_not_found = False
        queried_hostname = elem

        print('{}\n[client]: Querying hostname \'{}\'...\n{}\n'.format(CHAIN_LINK, queried_hostname, CHAIN_LINK))

        rs_ipaddr = socket.gethostbyname(rs_hostname)

        msg_out = queried_hostname
        data_out = msg_out.encode('utf-8')
        cl_sock_rs.send(data_out)
        print('[client]: outgoing to RS server \'{}\' at \'{}\': \'{}\''.format(rs_hostname, rs_ipaddr, queried_hostname))
        
        try:
            data_in = cl_sock_rs.recv(128)
        except EnvironmentError:
            print('[client]: ERROR - RS server by hostname \'{}\' not available.'.format(rs_binding[0]))
            return resolved_list

        msg_in = data_in.decode('utf-8')
        print('[client]: incoming from RS server \'{}\' at \'{}\': \'{}\''.format(rs_hostname, rs_ipaddr, msg_in))

        reply_elems = str_to_list(msg_in, delimiter)

        if len(reply_elems) == 3:
            if reply_elems[2] == DNS_table.flag.A.value:
                resolved_list.append(msg_in)
            elif reply_elems[2] == DNS_table.flag.NS.value:
                ts_hostname = reply_elems[0]

                print('[client]: Redirecting query \'{}\' to TS server by hostname \'{}\'.'.format(queried_hostname, ts_hostname))

                try:
                    cl_sock_ts = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                except EnvironmentError:
                    print('[client]: ERROR - client socket open error.\n')
                    continue

                print('[client]: Opened new datagram socket.')

                ts_binding = (ts_hostname, ts_portno)

                try:
                    socket.gethostbyname(rs_hostname)
                    cl_sock_ts.connect(ts_binding)
                except EnvironmentError:
                    print('[client]: ERROR - Unable to connect to TS server \'{}\'.\n'.format(ts_hostname))
                    continue
                
                ts_connected = True
                ts_ipaddr = socket.gethostbyname(ts_hostname)

                msg_out = queried_hostname
                data_out = msg_out.encode('utf-8')
                cl_sock_ts.send(data_out)
                print('[client]: outgoing to TS server \'{}\' at \'{}\': \'{}\''.format(ts_hostname, ts_ipaddr, queried_hostname))

                try:
                    data_in = cl_sock_ts.recv(128)
                except EnvironmentError:
                    print('[client]: ERROR - TS server by hostname \'{}\' not available.'.format(rs_binding[0]))
                    ts_connected = False
                
                if ts_connected:
                    msg_in = data_in.decode('utf-8')
                    print('[client]: incoming from TS server \'{}\' at \'{}\': \'{}\''.format(ts_hostname, ts_ipaddr, msg_in))

                    reply_elems = str_to_list(msg_in, delimiter)

                    if len(reply_elems) == 3 and reply_elems[1] != '-':
                        pass
                    elif len(reply_elems) == 5 and reply_elems[2] == 'Error:HOST':
                        pass
                    else:
                        print('[client]: NOTE - message from \'{}\' (at \'{}\'), \'{}\' is malformed. Appending to resolved_list anyway.'.format(ts_hostname, ts_ipaddr, msg_in))  

                    resolved_list.append(msg_in)
                    cl_sock_ts.close()
            else:
                print('[client]: message from \'{}\' (at \'{}\'), \'{}\' is malformed.'.format(rs_hostname, rs_ipaddr, msg_in))

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
    
    rs_hostname = ''
    rs_portno = 0

    ts_portno = 0

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

    print('')
    hostname_list = file_to_list(input_file_str)

    if len(hostname_list) > 0:
        resolved_list = query_servers(rs_hostname, 
                                      rs_portno, 
                                      hostname_list, 
                                      ts_portno)

    if len(resolved_list) > 0:
        write_to_file_from_list(output_file_str, resolved_list, 'w')

    print('')    
    return EX_OK

if __name__ == '__main__':
    """
        Program execution begins here.
    """
    retval = main(argv)
