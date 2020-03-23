import network
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

def main(argv):
    ## Do this for each incoming or outgoing message
    hostname = 'pwd.cs.rutgers.edu'
    ipaddr = '192.153.2.1'
    message = 'message to you, read me!'

    
    """
    s = log(logstat.IN, funcname(), '({} : {}) {}'.format(hostname, ipaddr, message))
    """
    
    log(logstat.OUT, funcname(), logstr(hostname, ipaddr, message))

    l = utils.file_to_list('PROJ2-HNS.txt')

    utils.write_to_file_from_list('out.txt', l, 'w')

    table = DNS_table()
    table.append_from_str('amazon.com 1923.1 A')
    table.has_hostname('google.com')
    table.has_hostname('googloe.com')
    return EX_OK

if __name__ == '__main__':
    retval = main(argv)


"""
def query_ls(ls_hostname, ls_portno, hostname_list):

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
"""
