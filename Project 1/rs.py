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

def linelist_to_dns_table(linelist):
    ts_hostname = '__NONE__'
    DNS_table = {}

    for line in linelist:
        result = [word.strip() for word in line.split(' ')]
        
        if len(result) != 3:
            DNS_table['ERROR'] = addrflag('MALFORMED', 'ENTRY')
        else:
            if result[2] == flag.NS.value and ts_hostname == '__NONE__':
                ts_hostname = result[0]
            elif result[2] == flag.A.value:
                DNS_table[result[0]] = addrflag(result[1], result[2])

    return (DNS_table, ts_hostname)

def find_hostname(DNS_table, queried_hostname):
    found = False

    for key, value in DNS_table.iteritems():
        if key.lower() == queried_hostname:
            found = True
            break
    
    return found

DEFAULT_INPUT_FILE_STR_RS = 'PROJI-DNSRS.txt'
DEFAULT_PORTNO_RS = 8345

from client import file_to_list
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

def udp_receiver(portno):
    sock = 0
    ipaddr = 0
    receiver_binding = ('', '')

    data = 0
    addr = 0

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print('[C]: Client UDP socket created.')
    except socket.error:
        print('[ERROR]: Socket open error - {}\n'.format(socket.error))

    ipaddr = socket.gethostbyname(socket.gethostname())

    try:
        receiver_binding = (ipaddr, portno)
        sock.bind(receiver_binding)
        
        print('[C]: Client UDP socket bound at {}, port number {}'.format(ipaddr, portno))
    except socket.error:
        print('[ERROR]: Socket bind error - {}\n'.format(socket.error))

    (data, addr) = sock.recvfrom(1024)
    print(addr, data.decode('utf-8'))

    sock.close()

def main(argv):
    """Main function, where client function is called

        Args:
            Command line arguments (as per sys.argv)
                argv[1] - rs_listen_port
                    desired port number for RS program
                argv[2] - custom_ts_hostname (OPTIONAL)
                    desired hostname for TS program
                argv[3] - input_file (OPTIONAL)
                    desired name of input file of entries for RS program
        Returns:
            Exit status, by default, 0 upon exit
        Raises:
            (none)
    """
    arg_length = len(argv)

    usage_str = '\nUSAGE:\npython {} [rs_listen_port]\npython {} [rs_listen_port] [input_file_name]\n'.format(argv[0], argv[0])

    rs_portno = DEFAULT_PORTNO_RS

    ts_hostname = ''

    input_file_str = DEFAULT_INPUT_FILE_STR_RS

    DNS_table = {}
    linelist = []
    queried_hostname = ''
    found = False

    msg_in = ''
    msg_out = ''

    data_in = ''
    data_out = ''

    if arg_length is 2:
        rs_portno = int(argv[1])

        input_file_str = DEFAULT_INPUT_FILE_STR_RS

        print(rs_portno)
    elif arg_length is 3:
        rs_portno = int(argv[1])

        input_file_str = argv[2]

        print(rs_portno, ts_hostname)
    else:
        print(usage_str)
        exit()
    
    linelist = file_to_list(input_file_str)
    (DNS_table, ts_hostname) = linelist_to_dns_table(linelist)

    ###
    ### connect to client here
    ###
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print('[RS]: Server socket created.')
    except socket.error:
        print('[ERROR]: {}\n'.format('Server socket open error.\n', socket.error))
        exit()
    
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    binding = ('', rs_portno)
    sock.connect(binding)

    rs_hostname = socket.gethostname()
    print('[RS]: Server hostname is: {}'.format(rs_hostname))

    rs_ipaddr = socket.gethostbyname(rs_hostname)
    print('[RS]: Server IP address is: {}\n'.format(rs_ipaddr))

    try:
        sock.connect(binding)
        print('[RS]: Attempting to connect...')
    except ConnectionRefusedError:
        print('[ERROR]: {}\n'.format('Client socket connection error.', ConnectionRefusedError))
        exit()

    print('[RS]: Connected.\n')

    ## example query from client
    queried_hostname = 'WWW.IBM.COM'.lower() ## get it from the client.
    
    found = find_hostname(DNS_table, queried_hostname)

    if found:
        msg_out = '{} {} {}'.format(queried_hostname, DNS_table[queried_hostname][0], DNS_table[queried_hostname][1])
        
        print(msg_out) ## send to client
    else:
        msg_out = '{} - {}'.format(ts_hostname, flag.NS.value)

        print(msg_out)  ## send to client
    
    ###
    ### Disconnect from client here
    ###
    sock.close()
    del sock

    return EX_OK

if __name__ == '__main__':
    """
        Program execution begins here.
    """
    retval = main(argv)
