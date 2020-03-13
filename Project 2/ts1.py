#!/usr/bin/python2.7
"""ts1.py
    Project 2: Load-balancing DNS servers (top-level DNS server socket 1)

    Rutgers University
        School of Arts and Sciences
            (01:198:352) Internet Technology
            Professor Nath Badri
            Section 02

    Assignment synopsis:
        In project 2, we will explore a design that implements load balancing among DNS servers by splitting the set of hostnames across multiple DNS servers.

        You will change the root server from project 1, RS, into a load-balancing server LS, that interacts with two top-level domain servers, TS1 and TS2. Only the TS servers store mappings from hostnames to IP addresses; the LS does not. 
        
        Further, the mappings stored by the TS servers do not overlap with each other; as a result, AT MOST ONE of the two TS servers will send a response to LS. 
        
        Overall, you will have four programs: the client, the load-balancing server (LS), and two DNS servers (TS1 and TS2).

        Each query proceeds as follows. 
        The client program makes the query (in the form of a hostname) to the LS. LS then forwards the query to _both_ TS1 and TS2. 
    
        However, at most one of TS1 and TS2 contain the IP address for this hostname. Only when a TS server contains a mapping will it respond to LS; otherwise, that TS sends nothing back.

        There are three possibilities. Either (1) LS receives a response from TS1, or (2) LS receives a response from TS2, or (3) LS receives no response from either TS1 or TS2 within a fixed timeout interval (see details below).
        
        If the LS receives a response (cases (1) and (2) above), it forwards the response as is to the client. If it times out waiting for a response (case 3) it sends an error string to the client. More details will follow.
        
        Please see the attached pictures showing interactions among the different programs.

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

from os import EX_OK
from sys import argv

from dns_module import DNS_table

DEFAULT_INPUT_FILE_STR_TS1 = "PROJ2-DNSTS1.txt"
DEFAULT_PORTNO_TS1 = 50007

import socket
import threading
import time
import random

__author__ = "Gemuele (Gem) Aludino"
__copyright__ = "Copyright (c) 2020, Gemuele Aludino"
__date__ = "06 Apr 2020"
__license__ = "MIT"
__email0__ = "g.aludino@gmail.com"
__email1__ = "gem.aludino@rutgers.edu"
__status__ = "Debug"

def main(argv):
    """Main function, where client function is called

        Args:
            Command line arguments (as per sys.argv)
                argv[1] - ts1_listen_port
                    desired port number for TS1 program
                argv[2] - input_file (OPTIONAL)
                    desired name of input file of entries for TS1 program
        Returns:
            Exit status, by default, 0 upon exit
        Raises:
            (none)
    """
    arg_length = len(argv)

    usage_str = '\nUSAGE:\npython {} [ts1_listen_port]\npython {} [ts1_listen_port] [input_file]\n'.format(argv[0], argv[0])

    ts1_portno = DEFAULT_PORTNO_TS1

    input_file_str = '__NONE__'

    table = {}
    queried_hostname = ''

    msg_in = ''
    msg_out = ''

    data_in = ''
    data_out = ''

    ts1_sock = 0
    ts1_binding = ('', '')
    ts1_hostname = ''
    ts1_ipaddr = ''

    client_ipaddr = ''
    client_hostname = ''
    client_portno = 0
    client_binding = ('', '')

    ### debugging args
    if arg_length is 1:
        ts1_portno = DEFAULT_PORTNO_TS1
        input_file_str = DEFAULT_INPUT_FILE_STR_TS1
    ### end debugging args
    elif arg_length is 2:
        ts1_portno = int(argv[1])
        input_file_str = DEFAULT_INPUT_FILE_STR_TS1
    elif arg_length is 3:
        ts1_portno = int(argv[1])
        input_file_str = argv[2]
    else:
        print(usage_str)
        exit()

    print('')
    table = DNS_table()
    table.append_from_file(input_file_str)

    try:
        ts1_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except EnvironmentError:
        print('[TS1]: ERROR - server socket open error.\n')
        exit()

    ts1_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    print('[TS1]: Opened new datagram socket.\n')

    ts1_binding = ('', ts1_portno)
    ts1_sock.bind(ts1_binding)

    ts1_hostname = socket.gethostname()
    ts1_ipaddr = socket.gethostbyname(ts1_hostname)

    print('[TS1]: Server hostname is \'{}\'.'.format(ts1_hostname))
    print('[TS1]: Server IP address is \'{}\'.\n'.format(ts1_ipaddr))

    while True:
        data_in, (client_ipaddr, client_portno) = ts1_sock.recvfrom(128)
        client_binding = (client_ipaddr, client_portno)

        client_hostname = socket.gethostbyaddr(client_ipaddr)[0]

        msg_in = data_in.decode('utf-8')
        queried_hostname = msg_in

        print('[TS1]: incoming from client \'{}\' at \'{}\': \'{}\''.format(client_hostname, client_ipaddr, msg_in))

        if table.has_hostname(queried_hostname):
            msg_out = '{} {} {}'.format(queried_hostname, table.ipaddr(queried_hostname), table.flagtype(queried_hostname))
        else:
            """
            msg_out = '{} - {}'.format(queried_hostname, DNS_table.flag.HOST_NOT_FOUND.value)
            """
            msg_out = '__NONE__'

        if msg_out != '__NONE__':
            data_out = msg_out.decode('utf-8')
            ts1_sock.sendto(data_out, client_binding)

            print('[TS1]: outgoing to client \'{}\' at \'{}\': \'{}\'\n'.format(client_hostname, client_ipaddr, msg_out))

    print('')
    return EX_OK

if __name__ == '__main__':
    """
        Program execution begins here.
    """
    retval = main(argv)
