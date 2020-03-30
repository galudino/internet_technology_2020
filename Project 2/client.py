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

from os import EX_OK
from os import path
from sys import argv
from enum import Enum
from socket import timeout

from utils import file_to_list
from utils import str_to_list
from utils import write_to_file_from_list
from utils import K
from utils import logstat
from utils import log
from utils import funcname
from utils import logstr

from network import BUFFER_SIZE
from network import udp_socket_open
from network import is_valid_hostname

from dns_module import DNS_table

from ls import DEFAULT_PORTNO_LS
from ls import DEFAULT_TS_TIMEOUT_VALUE

DEFAULT_INPUT_FILE_STR_HNS = 'PROJ2-HNS.txt'
DEFAULT_OUTPUT_FILE_STR_RESOLVED = 'RESOLVED.txt'

DEFAULT_HOSTNAME_LS = 'pwd.cs.rutgers.edu'

__author__ = "Gemuele (Gem) Aludino"
__copyright__ = "Copyright (c) 2020, Gemuele Aludino"
__date__ = "06 Apr 2020"
__license__ = "MIT"
__email0__ = "g.aludino@gmail.com"
__email1__ = "gem.aludino@rutgers.edu"
__status__ = "Release"

def query_ls(ls_info, hostname_list):
    """Starts the client routine by opening a socket so that it can communicate with the LS server, and send it the contents of hostname_list. Client will then receive replies from LS; each reply will be appended to a resolved_list and returned from this function.

        Args:
            ls_info: tuple
                consists of ls_hostname (LS hostname) and ls_portno (LS port number)
            hostname_list: list
                consists of hostnames (each a [str]) to query, which LS server will receive from client
        Returns:
            a [str] of replies from LS
        Raises:
            socket.timeout if no data is received from LS by timeout_val seconds.
    """
    ls_hostname = ls_info[0]
    ls_portno = ls_info[1]

    ls_ipaddr = is_valid_hostname(ls_hostname)
    ls_binding = (ls_hostname, ls_portno)

    timeout_val = DEFAULT_TS_TIMEOUT_VALUE * 2

    ls_sock = udp_socket_open()
    ls_sock.settimeout(timeout_val)

    resolved_list = []

    if ls_ipaddr:
        # if ls_hostname yields a valid ip address
        data_in = ''
        msg_in = ''
        
        msg_log = ''

        for query in hostname_list:       
            # log query
            msg_log = 'Querying hostname \'{}{}{}\'...'.format(K.color.bold.WHT, query, K.NRM)
            log(logstat.LOG, funcname(), msg_log)

            # send encoded query to LS
            ls_sock.sendto(query.encode('utf-8'), ls_binding)

            msg_log = logstr(ls_hostname, ls_ipaddr, query)
            log(logstat.OUT, funcname(), msg_log)
            
            # upon the next recv call,
            # we are expecting the query results from LS

            # receive data from LS, decode it
            try:
                data_in = ls_sock.recv(BUFFER_SIZE)
            except timeout:
                # LS is given a maximum of 10 sec to respond --
                # since TS1 and TS2 have a max of 5 secs to respond,
                # RTT must be accounted for
                msg_log = '[Connection timeout]'
                log(logstat.LOG, funcname(), msg_log + '\n')

            msg_in = data_in.decode('utf-8')

            msg_log = logstr(ls_hostname, ls_ipaddr, msg_in)
            log(logstat.IN, funcname(), msg_log)

            # append query result to resolved_list
            resolved_list.append(msg_in)

            msg_log = 'Added \'{}{}{}\' to resolved_list.'.format(K.color.bold.WHT, msg_in, K.NRM)
            log(logstat.LOG, funcname(), msg_log)

            print('')

    return resolved_list

def check_args(argv):
    """Examines the elements of argv to determine if the proper command line arguments were provided

        Args:
            argv: [str]
                Command line arguments
        Returns:
            a tuple consisting of
                ((ls_hostname, ls_portno), (input_file_str, output_file_str))
                or simply:
                (ls_info, file_io_info)
        Raises:
            (TODO)
    """
    arg_length = len(argv)

    usage_str = '\nUSAGE:\npython {} [ls_hostname] [ls_listen_port]\npython {} [ls_hostname] [ls_listen_port] [input_file_name]\npython {} [ls_hostname] [ls_listen_port] [input_file_name] [output_file_name]\n'.format(argv[0], argv[0], argv[0])

    ls_hostname = DEFAULT_HOSTNAME_LS
    ls_portno = DEFAULT_PORTNO_LS

    input_file_str = DEFAULT_INPUT_FILE_STR_HNS
    output_file_str = DEFAULT_OUTPUT_FILE_STR_RESOLVED

    # debugging args
    if arg_length is 1:
        pass
    elif arg_length is 2:
        ls_hostname = argv[1]
    # end debugging args
    elif arg_length is 3:
        ls_hostname = argv[1]
        ls_portno = int(argv[2])
    elif arg_length is 4:
        ls_hostname = argv[1]
        ls_portno = int(argv[2])

        input_file_str = argv[3]
    elif arg_length is 5:
        ls_hostname = argv[1]
        ls_portno = int(argv[2])

        input_file_str = argv[3]
        output_file_str = argv[4]
    else:
        print(usage_str)
        exit()

    return (ls_hostname, ls_portno), (input_file_str, output_file_str)

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
            KeyboardInterrupt
                if user terminates program with (Ctrl + c) before completion
            SystemExit
                causes program to exit upon KeyboardInterrupt
    """
    (ls_info, file_str) = check_args(argv)
    # ls_info[0] is LS's hostname
    # ls_info[1] is LS's port number

    # file_str[0] is the query input file string
    # file_str[1] is the query output file string
    print('')

    # read the input file into a list
    hostname_list = file_to_list(file_str[0])

    if len(hostname_list) > 0:
        resolved_list = []
        
        # if the hostname list has at least one element, proceed to LS server
        try:
            msg = 'Starting client routine. Hit (Ctrl + c) to quit.\n'
            log(logstat.LOG, funcname(), msg)

            resolved_list = query_ls(ls_info, hostname_list)
        except KeyboardInterrupt, SystemExit:
            print('')
            msg = 'User terminated program before completion.\n'
            log(logstat.LOG, funcname(), msg)

        if len(resolved_list) > 0:
            # if the resolved_list has at least one element, write to file
            write_to_file_from_list(file_str[1], resolved_list, 'w')
    else:
        # if the hostname list is empty, notify the user
        log(logstat.ERR, funcname(), 'No data was read from \'{}{}{}\'.\n'.format(K.color.bold.WHT, file_str[0], K.NRM))

    print('')
    return EX_OK

if __name__ == '__main__':
    # Program execution begins here.
    retval = main(argv)
