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

from os import EX_OK
from sys import argv

from dns_module import DNS_table

DEFAULT_INPUT_FILE_STR_TS = 'PROJI-DNSTS.txt'
DEFAULT_PORTNO_TS = 50007

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
    arg_length = len(argv)

    usage_str = '\nUSAGE:\npython {} [ts_listen_port]\npython {} [ts_listen_port] [input_file]\n'.format(argv[0], argv[0])

    ts_portno = DEFAULT_PORTNO_TS

    input_file_str = '__NONE__'

    table = {}
    queried_hostname = ''

    msg_in = ''
    msg_out = ''

    data_in = ''
    data_out = ''

    ts_sock = 0
    ts_binding = ('', '')
    ts_hostname = ''
    ts_ipaddr = ''

    client_hostname = ''
    client_portno = 0
    client_binding = ('', '')

    if arg_length is 2:
        ts_portno = int(argv[1])
        input_file_str = DEFAULT_INPUT_FILE_STR_TS
    elif arg_length is 3:
        ts_portno = int(argv[1])
        input_file_str = argv[2]
    else:
        print(usage_str)
        exit()

    table = DNS_table()
    table.append_from_file(input_file_str)

    ts_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ts_binding = (ts_hostname, ts_portno)
    ts_sock.bind(ts_binding)

    while True:
        data_in, (client_hostname, client_portno) = ts_sock.recvfrom(128)
        client_binding = (client_hostname, client_portno)

        msg_in = data_in.decode('utf-8')
        print('[TS]: incoming from client \'{}\': \'{}\''.format(client_hostname, msg_in))

        queried_hostname = msg_in

        if table.has_hostname(queried_hostname):
            msg_out = '{} {} {}'.format(queried_hostname, table.ipaddr(queried_hostname), table.flagtype(queried_hostname))
        else:
            msg_out = '{} - {}'.format(queried_hostname, DNS_table.flag.HOST_NOT_FOUND.value)

        data_out = msg_out.decode('utf-8')
        ts_sock.sendto(data_out, client_binding)
        print('[TS]: outgoing to client \'{}\': \'{}\'\n'.format(client_hostname, msg_out))

    return EX_OK

if __name__ == '__main__':
    """
        Program execution begins here.
    """
    retval = main(argv)
