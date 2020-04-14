#!/usr/bin/python2.7
"""network.py
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
    SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from socket import socket
from socket import AF_INET
from socket import SOCK_DGRAM
from socket import SOL_SOCKET
from socket import SO_REUSEADDR
from socket import gethostname
from socket import gethostbyname

from utils import K
from utils import logstat
from utils import log
from utils import funcname
from utils import logstr

BUFFER_SIZE = 256

__author__ = "Gemuele (Gem) Aludino"
__copyright__ = "Copyright (c) 2020, Gemuele Aludino"
__date__ = "06 Apr 2020"
__license__ = "MIT"
__email0__ = "g.aludino@gmail.com"
__email1__ = "gem.aludino@rutgers.edu"
__status__ = "Release"

def udp_socket_open():
    """Opens a UDP (datagram) socket, with a call to setsockopt (so the hostname can be immediately reused after a disconnect)

        Args:
            (none)
        Returns:
            An open UDP (datagram) socket
        Raises:
            EnvironmentError if socket fails to open
    """
    sock = 0
    msg = ''

    try:
        sock = socket(AF_INET, SOCK_DGRAM)
    except EnvironmentError:
        msg = 'Socket open error.\n'
        log(logstat.ERR, funcname(), msg)

        exit()

    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    msg = 'Opened new datagram socket.\n'
    log(logstat.OK, funcname(), msg)

    hostname = gethostname()
    ipaddr = gethostbyname(hostname)

    msg = 'Hostname is \'{}{}{}\'.'.format(K.color.bold.WHT, hostname, K.NRM)
    log(logstat.LOG, funcname(), msg)

    msg = 'IP address is \'{}{}{}\'.\n'.format(K.color.bold.WHT, ipaddr, K.NRM)
    log(logstat.LOG, funcname(), msg)

    return sock

def is_valid_hostname(hostname):
    """Uses gethostbyname to determine if hostname valid, or not

        Args:
            hostname: str
                desired hostname to verify
        Returns:
            str representing the IP address of the validated hostname;
            if hostname is invalid, returns None
        Raises:
            EnvironmentError if hostname is invalid (gethostbyname fails)
    """
    try:
        ipaddr = gethostbyname(hostname)
    except EnvironmentError:
        msg = 'Host by name \'{}{}{}\' is not available.\n'.format(K.color.bold.WHT, ls_hostname, K.NRM)
        log(logstat.ERR, funcname(), msg)

        return None
    
    msg = 'Verified hostname and IP address ({}{}{} : {}{}{})\n'.format(K.color.CYN, hostname, K.NRM, K.color.CYN, ipaddr, K.NRM)

    log(logstat.OK, funcname(), msg)

    return ipaddr
