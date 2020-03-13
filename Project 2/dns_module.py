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

from utils import file_to_list
from utils import str_to_list

from os import path
from enum import Enum
from collections import namedtuple

__author__ = "Gemuele (Gem) Aludino"
__copyright__ = "Copyright (c) 2020, Gemuele Aludino"
__date__ = "06 Apr 2020"
__license__ = "MIT"
__email0__ = "g.aludino@gmail.com"
__email1__ = "gem.aludino@rutgers.edu"
__status__ = "Debug"

HOST_NOT_FOUND_STR = 'Error:HOST NOT FOUND'

class DNS_table:
    __table = {}
    __ts_hostname = ''

    class flag(Enum):
        HOST_NOT_FOUND = 'Error:HOST NOT FOUND'
        A = 'A'
        NS = 'NS'
    
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
                print('[dns_module]: Found queried hostname \'{}\' with value \'({}, {})\' in table.'.format(query, value[0], value[1]))
                break

        if not found:
            print('[dns_module]: Unable to find hostname \'{}\' in table.'.format(query))

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
                
                print('[dns_module]: Input \'{}\' from file \'{}\' is malformed. Unable to add entry to table.\n'.format(line, input_file_str))
            else:
                if result[2] == DNS_table.flag.NS.value and self.__ts_hostname == '__NONE__':
                    self.__ts_hostname = result[0]

                    print('[dns_module]: ts_hostname assigned as \'{}\'.'.format(result[0]))

                elif result[2] == DNS_table.flag.A.value:
                    self.__table[result[0]] = self.addrflag(result[1], result[2])

                    print('[dns_module]: \'{} : ({}, {})\' added to table from file \'{}\'.'.format(result[0], result[1], result[2], input_file_str))
        
        print('')       

    def append_from_str(self, input_str):
        result = str_to_list(input_str, ' ')

        if len(result) != 3:
            self.__table['ERROR'] = self.addrflag('MALFORMED', 'ENTRY')
        else:
            if result[2] == DNS_table.flag.NS.value and self.__ts_hostname == '__NONE__':
                self.__ts_hostname = result[0]

                print('[dns_module]: ts_hostname assigned as \'{}\'.'.format(result[0]))
            elif result[2] == DNS_table.flag.A.value:
                self.__table[result[0]] = self.addrflag(result[1], result[2])

                print('[dns_module]: \'{} : ({}, {})\' added to table from string \'{}\'.'.format(result[0], result[1], result[2], input_str))

    def remove(self, hostname):
        self.__table.pop(hostname.lower())

    def clear(self):
        self.__table.clear()

    def empty(self):
        return len(self.__table) == 0   
    