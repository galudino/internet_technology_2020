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
from socket import gethostbyaddr
from socket import gethostbyname
from select import select

from utils import K
from utils import logstat
from utils import log
from utils import funcname
from utils import logstr

from network import BUFFER_SIZE
from network import udp_socket_open
from network import is_valid_hostname

from dns_module import DNS_table

from ts1 import DEFAULT_PORTNO_TS1
from ts2 import DEFAULT_PORTNO_TS2

DEFAULT_PORTNO_LS = 8345

DEFAULT_HOSTNAME_TS1 = "cp.cs.rutgers.edu"
DEFAULT_HOSTNAME_TS2 = "kill.cs.rutgers.edu"

DEFAULT_TS_TIMEOUT_VALUE = 5.0

__author__ = "Gemuele (Gem) Aludino"
__copyright__ = "Copyright (c) 2020, Gemuele Aludino"
__date__ = "06 Apr 2020"
__license__ = "MIT"
__email0__ = "g.aludino@gmail.com"
__email1__ = "gem.aludino@rutgers.edu"
__status__ = "Debug"

def start_ls(ls_portno, ts1_info, ts2_info):
    """(TODO)

        Args:
            (TODO)
        Returns:
            (TODO)
        Raises:
            (TODO)
    """
    ts1_hostname = ts1_info[0]
    ts1_portno = ts1_info[1]

    ts2_hostname = ts2_info[0]
    ts2_portno = ts2_info[1]

    ls_binding = ('', ls_portno)

    ls_sock = udp_socket_open()
    ls_sock.bind(ls_binding)

    ts1_ipaddr = is_valid_hostname(ts1_hostname)
    ts1_binding = (ts1_hostname, ts1_portno)

    ts1_sock = udp_socket_open()
    ts1_sock.setblocking(False)

    ts2_ipaddr = is_valid_hostname(ts2_hostname)
    ts2_binding = (ts2_hostname, ts2_portno)

    ts2_sock = udp_socket_open()
    ts2_sock.setblocking(False)

    ts_sockets = [ts1_sock, ts2_sock]
    resolved_sockets = []

    query = ''

    data_in = ''
    data_out = ''

    msg_in = ''
    msg_out = ''

    msg_log = ''

    timeout_val = DEFAULT_TS_TIMEOUT_VALUE

    while True:
        # receive data from client, decode for logging
        (data_in, (client_ipaddr, client_portno)) = ls_sock.recvfrom(BUFFER_SIZE)
        client_binding = (client_ipaddr, client_portno)
        query = data_in.decode('utf-8')

        # retrieve client hostname from client_ipaddr
        client_hostname = gethostbyaddr(client_ipaddr)[0]

        msg_log = logstr(client_hostname, client_ipaddr, query)
        log(logstat.IN, funcname(), msg_log)

        # send data to TS1
        ts1_sock.sendto(data_in, ts1_binding)

        msg_log = logstr(ts1_hostname, ts1_ipaddr, query)
        log(logstat.OUT, funcname(), msg_log)

        # send data to TS2
        ts2_sock.sendto(data_in, ts2_binding)

        msg_log = logstr(ts2_hostname, ts2_ipaddr, query)
        log(logstat.OUT, funcname(), msg_log)

        # use select with timeout_val to determine which socket to recv from
        resolved_sockets, _, _ = select(ts_sockets, [], [], timeout_val)

        if resolved_sockets:
            # if TS1 or TS2 received data, we proceed here
            for ts in resolved_sockets:
                hostname = ''
                ipaddr = ''
                
                # receive incoming data from TS socket
                # data received from TS socket will be sent to client
                data_in = ts.recv(BUFFER_SIZE)
                data_out = data_in

                # decode message for logging
                msg_in = data_in.decode('utf-8')
                msg_out = msg_in

                # log incoming data from TS socket
                if ts is ts1_sock:
                    hostname = ts1_hostname
                    ipaddr = ts1_ipaddr
                elif ts is ts2_sock:
                    hostname = ts2_hostname
                    ipaddr = ts2_ipaddr

                msg_log = logstr(hostname, ipaddr, msg_in)
                log(logstat.IN, funcname(), msg_log)
        else:
            # TS1 and TS2 did not receive data after timeout_val seconds, log it
            msg_log = '[Connection timeout]'
            log(logstat.LOG, funcname(), msg_log)

            # prepare 'HOST NOT FOUND' message for client
            msg_out = '{} - {}'.format(query, DNS_table.flag.HOST_NOT_FOUND.value)

            # encode prepared message, will send to client shortly
            data_out = msg_out.encode('utf-8')

        # send outgoing data to client
        ls_sock.sendto(data_out, client_binding)

        msg_log = logstr(client_hostname, client_ipaddr, msg_out)
        log(logstat.OUT, funcname(), msg_log)

        print('')   

def check_args(argv):
    """(TODO)

        Args:
            (TODO)
        Returns:
            (TODO)
        Raises:
            (TODO)
    """
    arg_length = len(argv)

    usage_str = '\nUSAGE:\npython {} [ls_listen_port] [ts1_hostname] [ts1_listen_port] [ts2_hostname] [ts2_listen_port]\n'.format(argv[0])

    ls_portno = DEFAULT_PORTNO_LS

    ts1_hostname = DEFAULT_HOSTNAME_TS1
    ts2_hostname = DEFAULT_HOSTNAME_TS2

    ts1_portno = DEFAULT_PORTNO_TS1
    ts2_portno = DEFAULT_PORTNO_TS2

    # debugging args
    if arg_length is 1:
        pass
    elif arg_length is 2:
        ls_portno = int(argv[1])
    # end debugging args   
    elif arg_length is 3:
        ls_portno = int(argv[1])
        ts1_hostname = argv[2]
    elif arg_length is 4:
        ls_portno = int(argv[1])

        ts1_hostname = argv[2]
        ts1_portno = int(argv[3])
    elif arg_length is 5:
        ls_portno = int(argv[1])

        ts1_hostname = argv[2]
        ts1_portno = int(argv[3])
        
        ts2_hostname = argv[4]
    elif arg_length is 6:
        ls_portno = int(argv[1])

        ts1_hostname = argv[2]
        ts1_portno = int(argv[3])
        
        ts2_hostname = argv[4]
        ts2_portno = argv[5]
    else:
        print(usage_str)
        exit()

    return (ls_portno, (ts1_hostname, ts1_portno), (ts2_hostname, ts2_portno))
    
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

    (ls_portno, ts1_info, ts2_info) = check_args(argv)
    # ts1_info[0] is TS1's hostname
    # ts1_info[1] is TS1's port number
    # ts2_info[0] is TS2's hostname
    # ts2_info[1] is TS2's port number
    print('')
    
    try:
        msg = 'Starting LS server. Hit (Ctrl + c) to quit.\n'
        log(logstat.LOG, funcname(), msg)

        start_ls(ls_portno, ts1_info, ts2_info)
    except KeyboardInterrupt, SystemExit:
        print('')
        msg = 'User terminated program before completion.\n'
        log(logstat.LOG, funcname(), msg)

    print('')
    return EX_OK

if __name__ == '__main__':
    # Program execution begins here.
    retval = main(argv)
