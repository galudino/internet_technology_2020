import network
from network import udp_socket_open
from network import is_valid_hostname
import utils

import socket
import threading
import time
import random

from sys import argv
from os import EX_OK

from utils import CHAIN_LINK
from utils import funcname
from utils import log
from utils import logstat
from utils import logstr

from dns_module import DNS_table

import select

def start_ls(ls_portno, ts1_hostname, ts1_portno, ts2_hostname, ts2_portno):
    ls_binding = ('', ls_portno)

    ls_sock = network.udp_socket_open()
    ls_sock.bind(ls_binding)

    ts1_sock = udp_socket_open()
    ts1_ipaddr = is_valid_hostname(ts1_hostname)
    ts1_binding = (ts1_hostname, ts1_portno)

    ts2_sock = udp_socket_open()
    ts2_ipaddr = is_valid_hostname(ts2_hostname)
    ts2_binding = (ts2_hostname, ts2_portno)

    ts_sockets = [ts1_sock, ts2_sock]
    resolved_sockets = []

    queried_hostname = ''

    msg_log = ''

    msg_in = ''
    msg_out = ''

    data_in = ''
    data_out = ''

    timeout_val = 1.0

    ## set ts sockets as non-blocking
    ts1_sock.setblocking(False)
    ts2_sock.setblocking(False)

    while True:
        ## receive incoming data from client
        data_in, (client_ipaddr, client_portno) = ls_sock.recvfrom(128)
        client_binding = (client_ipaddr, client_portno)

        ## retrieve client hostname from client_ipaddr
        client_hostname = socket.gethostbyaddr(client_ipaddr)[0]

        ## decode incoming data
        msg_in = data_in.decode('utf-8')
        queried_hostname = msg_in

        ## log incoming data
        msg_log = logstr(client_hostname, client_ipaddr, queried_hostname)
        log(logstat.IN, funcname(), msg_log)

        ## log outgoing data to TS1
        msg_log = logstr(ts1_hostname, ts1_ipaddr, queried_hostname)
        log(logstat.OUT, funcname(), msg_log)

        ## send outgoing data to TS1
        ts1_sock.sendto(queried_hostname.encode('utf-8'), ts1_binding)

        ## log outgoing data to TS2
        msg_log = logstr(ts2_hostname, ts2_ipaddr, queried_hostname)
        log(logstat.OUT, funcname(), msg_log)

        ## send outgoing data to TS2
        ts2_sock.sendto(queried_hostname.encode('utf-8'), ts2_binding)

        ## use select with timeout_val to determine which socket to recv from
        resolved_sockets, _, _ = select.select(ts_sockets, [], [], timeout_val)
    
        if resolved_sockets:
            for ts in resolved_sockets:
                ## receive incoming data from TS socket
                data_in = ts.recv(128)
                msg_in = data_in.decode('utf-8')

                ## consolidated code for logging
                hostname = ''
                ipaddr = ''
                
                if ts is ts1_sock:
                    hostname = ts1_hostname
                    ipaddr = ts1_ipaddr
                elif ts is ts2_sock:
                    hostname = ts2_hostname

                ## log incoming data from TS socket
                msg_log = logstr(hostname, ipaddr, msg_in)
                log(logstat.IN, funcname(), msg_log)

                ## data from TS socket will be sent to client shortly
                msg_out = msg_in
        else:
            ## log connection timeout
            msg_log = '[Connection timeout]'
            log(logstat.LOG, funcname(), msg_log)

            ## prepare 'HOST NOT FOUND' message for client
            msg_out = '{} - {}'.format(queried_hostname, DNS_table.flag.HOST_NOT_FOUND.value)

        ## log outgoing data to client
        msg_log = logstr(client_hostname, client_ipaddr, msg_out)
        log(logstat.OUT, funcname(), msg_log)

        ## send outgoing data to client
        ls_sock.sendto(msg_out.encode('utf-8'), client_binding)

        print('')    

def main(argv):
    start_ls(8345, 'cp.cs.rutgers.edu', 50007, 'kill.cs.rutgers.edu', 50009)
    return EX_OK

if __name__ == '__main__':
    retval = main(argv)

