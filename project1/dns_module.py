#!/usr/bin/python2.7
"""dns_module.py
    Project 1: Recursive DNS client and DNS servers (DNS_table code)
 
    Rutgers University
        School of Arts and Sciences
            (01:198:352) Internet Technology
            Professor Nath Badri
            Section 02

    Assignment synopsis:
        The goal of this project is to implement a simplified DNS system consisting of a client program and two server programs: RS (a simplified root DNS server) and TS (a simplified top-level DNS server). In project 0 (your first HW), you have already seen a client-server program with one socket each in the client and the server. In this project, you will extend that implementation to have two sockets in the client program. One socket will be used to communicate with RS and the other with TS.

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
__date__ = "04 Mar 2020"
__license__ = "MIT"
__email0__ = "g.aludino@gmail.com"
__email1__ = "gem.aludino@rutgers.edu"
__status__ = "Release"

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
    