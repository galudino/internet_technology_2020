#!/usr/bin/python2.7
"""dns_module.py
    Project 2: Load-balancing DNS servers (DNS_table code)

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

from os import path
from enum import Enum
from collections import namedtuple

from utils import K
from utils import logstat
from utils import log
from utils import funcname
from utils import logstr
from utils import file_to_list
from utils import str_to_list

__author__ = "Gemuele (Gem) Aludino"
__copyright__ = "Copyright (c) 2020, Gemuele Aludino"
__date__ = "06 Apr 2020"
__license__ = "MIT"
__email0__ = "g.aludino@gmail.com"
__email1__ = "gem.aludino@rutgers.edu"
__status__ = "Release"

HOST_NOT_FOUND_STR = 'Error:HOST NOT FOUND'

class DNS_table:
    """ADT that wraps a dictionary representing mappings of hostnames to namedtuples called addrflag."""
    __table = {}
    __ts_hostname = ''

    class flag(Enum):
        """Subclass of Enum that represents 3 distinct states - HOST_NOT_FOUND, A, or NS -- these are of type [str]."""
        HOST_NOT_FOUND = HOST_NOT_FOUND_STR
        A = 'A'
        NS = 'NS'
    
    """addrflag is the value that a hostname maps to within DNS_table."""
    addrflag = namedtuple('addrflag', ['ipaddr', 'flagtype'])

    def __init__(self):
        self.__ts_hostname = '__NONE__'

    @property
    def dictionary(self):
        return self.__table

    @property
    def ts_hostname(self):
        return self.__ts_hostname

    def has_hostname(self, query):
        found = False  
        q = query.lower()

        for key, value in self.__table.iteritems():
            if key.lower() == q:
                found = True

                msg = 'Found queried hostname \'{}{}{}\' with value \'{}({}, {}){}\' in table.'.format(K.color.bold.WHT, query, K.NRM, K.color.bold.WHT, value[0], value[1], K.NRM)

                log(logstat.OK, funcname(), msg)

                break

        if not found:
            msg = 'Unable to find hostname \'{}{}{}\' in table.'.format(K.color.bold.WHT, query, K.NRM)

            log(logstat.LOG, funcname(), msg)

        return found  
    
    def ipaddr(self, key):
        return self.__table[key.lower()][0]
    
    def flagtype(self, key):
        return self.__table[key.lower()][1]

    def append(self, hostname, addrflag_pair):
        self.__table[hostname] = addrflag_pair

    def append_from_file(self, input_file_str):
        linelist = file_to_list(input_file_str)

        for line in linelist:
            result = [word.strip() for word in line.split(' ')]

            if len(result) != 3:
                self.__table['ERROR'] = self.addrflag('MALFORMED', 'ENTRY')
                
                msg = 'Input \'{}{}{}\' from file \'{}{}{}\' is malformed. Unable to add entry to table.\n'.format(K.color.bold.WHT, line, K.NRM, K.color.bold.WHT, input_file_str, K.NRM)

                log(logstat.ERR, funcname(), msg)
            else:
                if result[2] == DNS_table.flag.NS.value and self.__ts_hostname == '__NONE__':
                    self.__ts_hostname = result[0]

                    msg = 'ts_hostname assigned as \'{}{}{}\'.'.format(K.color.bold.WHT, result[0], K.NRM)

                    log(logstat.LOG, funcname(), msg)
                elif result[2] == DNS_table.flag.A.value:
                    self.__table[result[0]] = self.addrflag(result[1], result[2])

                    msg = '{}\'{} : ({}, {}){}\' added to table from file {}\'{}\'{}.'.format(K.color.bold.WHT, result[0], result[1], result[2], K.NRM, K.color.bold.WHT, input_file_str, K.NRM)

                    log(logstat.LOG, funcname(), msg)
        
        print('')       

    def append_from_str(self, input_str):
        result = str_to_list(input_str, ' ')

        if len(result) != 3:
            self.__table['ERROR'] = self.addrflag('MALFORMED', 'ENTRY')
        else:
            if result[2] == DNS_table.flag.NS.value and self.__ts_hostname == '__NONE__':
                self.__ts_hostname = result[0]

                msg = 'ts_hostname assigned as \'{}{}{}\'.'.format(K.color.bold.WHT, result[0], K.NRM)

                log(logstat.LOG, funcname(), msg)
            elif result[2] == DNS_table.flag.A.value:
                self.__table[result[0]] = self.addrflag(result[1], result[2])
    
                msg = '{}\'{} : ({}, {}){}\' added to table from string {}\'{}\'{}.'.format(K.color.bold.WHT, result[0], result[1], result[2], K.NRM, K.color.bold.WHT, input_str, K.NRM)

                log(logstat.LOG, funcname(), msg)

    def remove(self, hostname):
        self.__table.pop(hostname.lower())

    def clear(self):
        self.__table.clear()

    def empty(self):
        return len(self.__table) == 0   
    