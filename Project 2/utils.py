#!/usr/bin/python2.7
"""utils.py
    Project 2: Load-balancing DNS servers (miscellaneous utilities)

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

from sys import _getframe
from os import path
from datetime import datetime
from enum import Enum

__author__ = "Gemuele (Gem) Aludino"
__copyright__ = "Copyright (c) 2020, Gemuele Aludino"
__date__ = "06 Apr 2020"
__license__ = "MIT"
__email0__ = "g.aludino@gmail.com"
__email1__ = "gem.aludino@rutgers.edu"
__status__ = "Debug"

CHAIN_LINK = '-------------------------------------------------------------------------------'

DCHAIN_LINK = '==============================================================================='

STAR_LINK = '*******************************************************************************'

class K:
    NRM = '\033[00m'
    
    class color:
        GRY = '\033[0;02m'
        RED = '\033[0;31m'
        GRN = '\033[0;32m'
        YEL = '\033[0;33m'
        BLU = '\033[0;34m'
        MAG = '\033[0;35m'
        CYN = '\033[0;36m'
        WHT = '\033[0;37m'
        
        class bold:
            GRY = '\033[1;02m'
            RED = '\033[1;31m'
            GRN = '\033[1;32m'
            YEL = '\033[1;33m'
            BLU = '\033[1;34m'
            MAG = '\033[1;35m'
            CYN = '\033[1;36m'
            WHT = '\033[1;37m'

    class italic:
        ITL = '\033[0;03m'
    
    class underline:
        ULN = '\033[0;04m'
    
    class special:
        BNK = '\033[0;05m'
        HIL = '\033[0;07m'

class logstat(Enum):
    IN = 'IN'
    OUT = 'OUT'
    OK = 'OK'
    ERR = 'ERR'
    WRN = 'WRN'
    LOG = 'LOG'
    BUG = 'BUG'

def log(stat, header, msg):
    """Returns a [str], used for debugging/logging, formatted with a descriptor (based on a [logstat]), timestamp, header (usually a call to funcname()), and msg
        Args:
            stat: logstat
                denotes the color/descriptor of the log message
            header: str
                usually used for the calling function name, but up to user
            msg: str
                body of logging message, can also be used with logstr() to create a more detailed header for the message body
        Returns:
            A [str] consisting of the formatted log message
        Raises:
            (none)
    """
    color = K.NRM

    if stat == stat.IN:
        color = K.color.bold.BLU
    elif stat == stat.OUT:
        color = K.color.bold.RED
    elif stat == stat.OK:
        color = K.color.bold.GRN
    elif stat == stat.ERR:
        color = K.color.bold.MAG
    elif stat == stat.WRN:
        color = K.color.bold.YEL
    elif stat == stat.LOG:
        color = K.color.bold.CYN
    elif stat == stat.BUG:
        color = K.color.bold.GRY

    ## With colors
    print('{}[{}]{} {}{}{} <{}{}{}> {}'.format(color, stat.value, K.NRM, K.color.GRY, datetime.now(), K.NRM, K.color.bold.WHT, header, K.NRM, msg))
    
    ## No colors
    """
    print('[{}] {} <{}> {}'.format(stat.value, datetime.now(), header, msg))
    """

def funcname():
    """Returns a [str] of the calling function
        Args:
            (none)
        Returns:
            string of the calling function
        Raises:
            (none)
    """
    return _getframe().f_back.f_code.co_name

def logstr(x, y, z):
    """Returns a [str] using x, y, and z - purpose determined by user,
    best for describing a tuple, paired to another value.
        Args:
            x: str
                The 'key' of the tuple
            y: str
                The 'value' of the tuple
            z: str
                The 'value' of the tuple described by (x, y)
        Returns:
            A [str] consisting of '(x : y) z'
        Raises:
            (none)
    """
    ## With colors
    return '({}{}{} : {}{}{}) {}->{} {}'.format(K.color.CYN, x, K.NRM, K.color.CYN, y, K.NRM, K.color.bold.YEL, K.NRM, z)
    
    ## No colors
    """
    return '({} : {}) -> {}'.format(x, y, z)
    """

def file_to_list(input_file_str):
    """Creates a [str] using lines taken from a file named input_file_str;
    each element in the [str] will be suffixed with a linebreak

        Args:
            input_file_str: str
                The name of the desired file to open
        Returns:
            A [str] of lines from file input_file_str
        Raises:
            IOError if input_file_str does not exist
    """
    output_list = []
    msg = ''
    
    try:
        with open(input_file_str, 'r') as input_file:
            output_list = [line.rstrip() for line in input_file]

            msg = 'Input file \'{}{}{}\' opened.\n'.format(K.color.bold.WHT, input_file_str, K.NRM)

            log(logstat.OK, funcname(), msg)

            for elem in output_list:
                msg = 'Appending \'{}{}{}\' to list.'.format(K.color.bold.WHT, elem, K.NRM)

                log(logstat.LOG, funcname(), msg)
            print('')

            input_file.close()
    except IOError:
        msg = 'Input file \'{}{}{}\' not found.\n'.format(K.color.bold.WHT, input_file_str, K.NRM)
        
        log(logstat.ERR, funcname(), msg)
    
    return output_list

def str_to_list(input_str, delim):
    """(TODO)

        Args:
            (TODO)
        Returns:
            (TODO)
        Raises:
            (TODO)
    """
    output_list = []
    
    output_list = [word.strip() for word in input_str.split(delim)]

    for elem in output_list:
        msg = 'Stripped \'{}{}{}\' from \'{}{}{}\' by delimiter \'{}{}{}\''.format(K.color.bold.WHT, elem, K.NRM, K.color.bold.WHT, input_str, K.NRM, K.color.bold.WHT, delim, K.NRM)

        log(logstat.LOG, funcname(), msg)
    print('')

    return output_list

def write_to_file_from_list(output_file_str, input_list, flag):
    """Writes/appends each str from input_list to a file named output_file_str, with each
    appendage suffixed with a linebreak

        Args:
            output_file_str: str
                The name of the desired output file to write to
            
            input_list: str
                The name of a list of str
            
            flag: str
                For open() call, should be 'w' for write or 'a' for append
        Returns:
            (none)
        Raises:
            (none)
    """
    message = []
    msg = ''

    if len(input_list) == 0:
        msg = 'Cannot use this function with an empty input_list.\n'
        
        log(logstat.ERR, funcname(), msg)
        return

    if flag is 'w':
        message = ('overwrite', 'written')
    elif flag is 'a':
        message = ('append to', 'appended')
    else:
        msg = 'Flag must be \'{}w{}\' for write or \'{}a{}\' for append.\n'.format(K.color.bold.WHT, K.NRM, K.color.bold.WHT, K.NRM)

        log(logstat.ERR, funcname(), msg)
        return

    if path.isfile(output_file_str):
        msg = 'Output file \'{}{}{}\' exists. Will {} existing contents.\n'.format(K.color.bold.WHT, output_file_str, K.NRM, message[0])
    else:
        msg = 'Will create new file \'{}{}{}\'.'.format(K.color.bold.WHT, output_file_str, K.NRM)

    log(logstat.LOG, funcname(), msg)

    with open(output_file_str, flag) as output_file:
        for line in input_list:
            output_file.write(line + '\n')

            msg = 'Writing \'{}{}{}\' to output file \'{}{}{}\'.'.format(K.color.bold.WHT, line, K.NRM, K.color.bold.WHT, output_file_str, K.NRM)

            log(logstat.LOG, funcname(), msg)
        print('')

    msg = 'Contents of input_list successfully {} to \'{}{}{}\'.\n'.format(message[1], K.color.bold.WHT, output_file_str, K.NRM)
    
    log(logstat.OK, funcname(), msg)
