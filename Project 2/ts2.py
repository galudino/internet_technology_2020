#!/usr/bin/python2.7
"""README
    Project 2: Load-balancing DNS servers (top-level DNS server socket 2)

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

from utils import K
from utils import logstat
from utils import log
from utils import funcname
from utils import logstr

from network import udp_socket_open
from network import is_valid_hostname

from dns_module import DNS_table

DEFAULT_INPUT_FILE_STR_TS2 = "PROJ2-DNSTS2.txt"
DEFAULT_PORTNO_TS2 = 50009

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

def start_ts2(ts2_portno, table):
    ts2_binding = ('', ts2_portno)

    ts2_sock = udp_socket_open()
    ts2_sock.bind(ts2_binding)

    queried_hostname = ''

    msg_log = ''

    msg_in = ''
    msg_out = ''

    data_in = ''
    data_out = ''

    while True:
        ## receive incoming data from LS
        data_in, (ls_ipaddr, ls_portno) = ts2_sock.recvfrom(128)
        ls_binding = (ls_ipaddr, ls_portno)

        ls_hostname = socket.gethostbyaddr(ls_ipaddr)[0]

        msg_in = data_in.decode('utf-8')
        queried_hostname = msg_in

        ## log incoming data
        msg_log = logstr(ls_hostname, ls_ipaddr, queried_hostname)
        log(logstat.IN, funcname(), msg_log)

        ## search table for queried_hostname
        if table.has_hostname(queried_hostname):
            ## if queried_hostname is resolved, reply to LS
            
            ## prepare outgoing data to LS
            msg_out = '{} {} {}'.format(queried_hostname, table.ipaddr(queried_hostname), table.flagtype(queried_hostname))

            ## log outgoing data to LS
            msg_log = logstr(ls_hostname, ls_ipaddr, msg_out)
            log(logstat.OUT, funcname(), msg_log)

            ## send outgoing data to LS
            ts2_sock.sendto(msg_out.encode('utf-8'), ls_binding)
        else:
            ## if queried_hostname is not resolved, log to stdout
            log(logstat.LOG, funcname(), 'No outgoing data will be sent for this query.')

        print('')  

def main(argv):
    """Main function, where client function is called

        Args:
            Command line arguments (as per sys.argv)
                argv[1] - ts2_listen_port
                    desired port number for TS2 program
                argv[2] - input_file (OPTIONAL)
                    desired name of input file of entries for TS2 program
        Returns:
            Exit status, by default, 0 upon exit
        Raises:
            (none)
    """
    arg_length = len(argv)

    usage_str = '\nUSAGE:\npython {} [ts2_listen_port]\npython {} [ts2_listen_port] [input_file]\n'.format(argv[0], argv[0])

    ts2_portno = DEFAULT_PORTNO_TS2

    input_file_str = '__NONE__'
    table = {}

    ### debugging args
    if arg_length is 1:
        ts2_portno = DEFAULT_PORTNO_TS2
        input_file_str = DEFAULT_INPUT_FILE_STR_TS2
    ### end debugging args
    elif arg_length is 2:
        ts2_portno = int(argv[1])
        input_file_str = DEFAULT_INPUT_FILE_STR_TS2
    elif arg_length is 3:
        ts2_portno = int(argv[1])
        input_file_str = argv[2]
    else:
        print(usage_str)
        exit()

    print('')

    table = DNS_table()
    table.append_from_file(input_file_str)

    start_ts2(ts2_portno, table)

    return EX_OK

if __name__ == '__main__':
    """
        Program execution begins here.
    """
    retval = main(argv)
