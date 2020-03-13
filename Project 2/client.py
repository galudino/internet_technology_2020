#!/usr/bin/python2.7
"""client.py
    Project 2: Load-balancing DNS servers (client socket)

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

from utils import file_to_list
from utils import str_to_list
from utils import write_to_file_from_list
from utils import CHAIN_LINK

from dns_module import DNS_table

from ls import DEFAULT_PORTNO_LS

from os import EX_OK
from os import path
from sys import argv
from enum import Enum

DEFAULT_INPUT_FILE_STR_HNS = 'PROJ2-HNS.txt'
DEFAULT_OUTPUT_FILE_STR_RESOLVED = 'RESOLVED.txt'

DEFAULT_HOSTNAME_LS = 'pwd.cs.rutgers.edu'

DEFAULT_BUFFER_SIZE = 128

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

def query_ls(ls_hostname, ls_portno, hostname_list):
    """Opens UDP client socket and connects to LS server

        Args:
            ls_hostname
                hostname for desired LS server
            ls_portno
                port number for desired LS server, corresponds to ls_hostname
            hostname_list
                list of hostnames populated by calling function to query
                (will be sent to LS server)
        Returns:
            resolved_list
                list of hostnames mappings resolved by LS
                (LS reply messages)
        Raises:
            (none)
    """
    client_ipaddr = ''
    client_hostname = ''

    cl_sock_ls = 0

    ls_ipaddr = ''
    ls_binding = ('', '')

    resolved_list = []
    queried_hostname = ''

    msg_in = ''
    msg_out = ''

    data_in = ''
    data_out = ''

    delimiter = ' '

    """
        Opening datagram (UDP) client socket
    """
    try:
        cl_sock_ls = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except EnvironmentError:
        print('[client]: ERROR - client socket open error.\n')
        exit()

    cl_sock_ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    print('[client]: Opened new datagram socket.\n')

    ls_binding = (ls_hostname, ls_portno)

    try:
        socket.gethostbyname(ls_hostname)
        cl_sock_ls.connect(ls_binding)
    except EnvironmentError:
        print('[client]: ERROR - unable to connect to LS server \'{}\'\n'.format(ls_hostname))
        exit()

    client_hostname = socket.gethostname()
    client_ipaddr = socket.gethostbyname(client_hostname)

    print('[client]: Client hostname is \'{}\'.'.format(client_hostname))
    print('[client]: Client IP address is \'{}\'.\n'.format(client_ipaddr))
    
    """
        Begin routine
    """
    ## think about this:
    ## send entire hostname_list, message by message, to LS,
    ## then, receive all replies from LS. LS will then send '__DONE__' flag

    for elem in hostname_list:
        queried_hostname = elem

        print('{}\n[client]: Querying hostname \'{}\'...\n{}\n'.format(CHAIN_LINK, queried_hostname, CHAIN_LINK))

        ls_ipaddr = socket.gethostbyname(ls_hostname)

        msg_out = queried_hostname
        data_out = msg_out.encode('utf-8')
        cl_sock_ls.send(data_out)
        print('[client]: outgoing to LS server \'{}\' at \'{}\': \'{}\''.format(ls_hostname, ls_ipaddr, queried_hostname))
        
        try:
            data_in = cl_sock_ls.recv(DEFAULT_BUFFER_SIZE)
        except EnvironmentError:
            print('[client]: ERROR - LS server by hostname \'{}\' not available.'.format(ls_binding[0]))
            return resolved_list

        msg_in = data_in.decode('utf-8')
        print('[client]: incoming from LS server \'{}\' at \'{}\': \'{}\''.format(ls_hostname, ls_ipaddr, msg_in))

        resolved_list.append(msg_in)

    return resolved_list

def main(argv):
    """Main function, where client function is called

        Args:
            Command line arguments (as per sys.argv)
                argv[1] - ls_hostname
                    desired hostname for LS machine
                argv[2] - ls_listen_port
                    desired port number for LS machine
                argv[3] - input_file_name (OPTIONAL)
                    desired name of input file (queried hostnames)
                argv[4] - output_file_name (OPTIONAL)
                    desired name of output file (resolved host names)
        Returns:
            Exit status, by default, 0 upon exit
        Raises:
            (none)
    """
    arg_length = len(argv)

    usage_str = '\nUSAGE:\npython {} [ls_hostname] [ls_listen_port]\npython {} [ls_hostname] [ls_listen_port] [input_file_name]\npython {} [ls_hostname] [ls_listen_port] [input_file_name] [output_file_name]\n'.format(argv[0], argv[0], argv[0])

    ls_hostname = ''
    ls_portno = ''

    input_file_str = DEFAULT_INPUT_FILE_STR_HNS
    output_file_str = DEFAULT_OUTPUT_FILE_STR_RESOLVED

    hostname_list = []
    resolved_list = []

    len_hostname_list = -1

    ### debugging args
    if arg_length is 1:
        ls_hostname = DEFAULT_HOSTNAME_LS
        ls_portno = DEFAULT_PORTNO_LS
    elif arg_length is 2:
        ls_hostname = argv[1]
        ls_portno = DEFAULT_PORTNO_LS
    ### end debugging args
    elif arg_length is 3:
        ls_hostname = argv[1]
        ls_portno = argv[2]
    elif arg_length is 4:
        ls_hostname = argv[1]
        ls_portno = argv[2]

        input_file_str = argv[3]
    elif arg_length is 5:
        ls_portno = argv[1]
        ls_portno = argv[2]

        input_file_str = argv[3]
        output_file_str = argv[4]
    else:
        print(usage_str)
        exit()

    print('')
    hostname_list = file_to_list(input_file_str)
    len_hostname_list = len(hostname_list)
    
    if len_hostname_list > 0:
        resolved_list = query_ls(ls_hostname, ls_portno, hostname_list)
        write_to_file_from_list(output_file_str, resolved_list, 'w')
        
    print('')
    return EX_OK

if __name__ == '__main__':
    """
        Program execution begins here.
    """
    retval = main(argv)
