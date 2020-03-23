#!/usr/bin/python2.7
"""ls.py
    Project 2: Load-balancing DNS servers (load-balancing server)

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

from ts1 import DEFAULT_PORTNO_TS1
from ts2 import DEFAULT_PORTNO_TS2

DEFAULT_PORTNO_LS = 8345

DEFAULT_HOSTNAME_TS1 = "cp.cs.rutgers.edu"
DEFAULT_HOSTNAME_TS2 = "kill.cs.rutgers.edu"

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

def start_ls(ls_portno, ts1_hostname, ts1_portno, ts2_hostname, ts2_portno):
    ls_binding = ('', ls_portno)

    ls_sock = udp_socket_open()
    ls_sock.bind(ls_binding)

    ts1_sock = udp_socket_open()
    ts1_ipaddr = is_valid_hostname(ts1_hostname)
    ts1_binding = (ts1_hostname, ts1_portno)

    ts2_sock = udp_socket_open()
    ts2_ipaddr = is_valid_hostname(ts2_hostname)
    ts2_binding = (ts2_hostname, ts2_portno)

    tval = 0.0025

    queried_hostname = ''

    msg_log = ''

    msg_in = ''
    msg_out = ''

    data_in = ''
    data_out = ''

    ts1_sock.settimeout(tval)
    ts2_sock.settimeout(tval)

    while True:
        ## receive incoming data from client
        data_in, (client_ipaddr, client_portno) = ls_sock.recvfrom(128)
        client_binding = (client_ipaddr, client_portno)

        client_hostname = socket.gethostbyaddr(client_ipaddr)[0]

        msg_in = data_in.decode('utf-8')
        queried_hostname = msg_in

        ## log incoming data
        msg_log = logstr(client_hostname, client_ipaddr, queried_hostname)
        log(logstat.IN, funcname(), msg_log)

        ## log outgoing data to TS1
        msg_log = logstr(ts1_hostname, ts1_ipaddr, queried_hostname)
        log(logstat.OUT, funcname(), msg_log)

        ## send outgoing data to TS1
        ts1_sock.sendto(data_in, ts1_binding)

        ## log outgoing data to TS2
        msg_log = logstr(ts2_hostname, ts2_ipaddr, queried_hostname)
        log(logstat.OUT, funcname(), msg_log)

        ## send outgoing data to TS2
        ts2_sock.sendto(data_in, ts2_binding)

        try:
            data_in = ts1_sock.recv(128)
        except socket.timeout:
            msg_log = logstr(ts1_hostname, ts1_ipaddr, '[Connection timeout]')
            log(logstat.LOG, funcname(), msg_log)
            
            try:
                data_in = ts2_sock.recv(128)
            except socket.timeout:
                msg_log = logstr(ts2_hostname, ts2_ipaddr, '[Connection timeout]')
                log(logstat.LOG, funcname(), msg_log)
            
                msg_out = '{} - {}'.format(queried_hostname, DNS_table.flag.HOST_NOT_FOUND.value)

                msg_log = logstr(client_hostname, client_ipaddr, msg_out)
                log(logstat.OUT, funcname(), msg_log)
                ls_sock.sendto(msg_out.encode('utf-8'), client_binding)

                print('')
                continue
            
            ## log incoming data from TS2
            msg_log = logstr(ts2_hostname, ts2_ipaddr, data_in.decode('utf-8'))
            log(logstat.IN, funcname(), msg_log)

            ## log outgoing data to client
            msg_log = logstr(client_hostname, client_ipaddr, data_in.decode('utf-8'))
            log(logstat.OUT, funcname(), msg_log)

            ## send outgoing data to client
            ls_sock.sendto(data_in, client_binding)
            
            print('')
            continue
        
        ## log incoming data from TS1
        msg_log = logstr(ts1_hostname, ts1_ipaddr, data_in.decode('utf-8'))
        log(logstat.IN, funcname(), msg_log)

        ## log outgoing data to client
        msg_log = logstr(client_hostname, client_ipaddr, data_in.decode('utf-8'))
        log(logstat.OUT, funcname(), msg_log)

        ## send outgoing data to client
        ls_sock.sendto(data_in, client_binding)
        
        print('')

def main(argv):
    """Main function

        Args:
            Command line arguments (as per sys.argv)
                argv[1] - ls_listen_port
                    desired port number for LS program
                argv[2] - ts1_hostname
                    hostname for desired TS1 server
                argv[3] - ts1_listen_port
                    port number for desired TS1 server, corresponds to ts1_hostname
                argv[4] - ts2_hostname
                    hostname for desired TS2 server
                argv[5] - ts2_listen_port
                    port number for desired TS2 server, corresponds to ts2_hostname
    """
    arg_length = len(argv)

    usage_str = '\nUSAGE:\npython {} [ls_listen_port] [ts1_hostname] [ts1_listen_port] [ts2_hostname] [ts2_listen_port]\n'.format(argv[0])

    ls_portno = 0

    ts1_hostname = ''
    ts2_hostname = ''

    ts1_portno = 0
    ts2_portno = 0

    if arg_length is 1:
        ls_portno = DEFAULT_PORTNO_LS

        ts1_hostname = DEFAULT_HOSTNAME_TS1
        ts1_portno = DEFAULT_PORTNO_TS1

        ts2_hostname = DEFAULT_HOSTNAME_TS2
        ts2_portno = DEFAULT_PORTNO_TS2
    elif arg_length is 2:
        ls_portno = int(argv[1])

        ts1_hostname = DEFAULT_HOSTNAME_TS1
        ts1_portno = DEFAULT_PORTNO_TS1

        ts2_hostname = DEFAULT_HOSTNAME_TS2
        ts2_portno = DEFAULT_PORTNO_TS2        
    elif arg_length is 3:
        ls_portno = int(argv[1])

        ts1_hostname = argv[2]
        ts1_portno = DEFAULT_PORTNO_TS1

        ts2_hostname = DEFAULT_HOSTNAME_TS2
        ts2_portno = DEFAULT_PORTNO_TS2
    elif arg_length is 4:
        ls_portno = int(argv[1])

        ts1_hostname = argv[2]
        ts1_portno = int(argv[3])
        
        ts2_hostname = DEFAULT_HOSTNAME_TS2
        ts2_portno = DEFAULT_PORTNO_TS2
    elif arg_length is 5:
        ls_portno = int(argv[1])

        ts1_hostname = argv[2]
        ts1_portno = int(argv[3])
        
        ts2_hostname = argv[4]
        ts2_portno = DEFAULT_PORTNO_TS2
    elif arg_length is 6:
        ls_portno = int(argv[1])

        ts1_hostname = argv[2]
        ts1_portno = int(argv[3])
        
        ts2_hostname = argv[4]
        ts2_portno = argv[5]
    else:
        print(usage_str)
        exit()

    print('')
    
    start_ls(ls_portno, ts1_hostname, ts1_portno, ts2_hostname, ts2_portno)

    print('')
    return EX_OK

if __name__ == '__main__':
    """
        Program execution begins here.
    """
    retval = main(argv)
