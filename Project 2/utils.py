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

from os import path

__author__ = "Gemuele (Gem) Aludino"
__copyright__ = "Copyright (c) 2020, Gemuele Aludino"
__date__ = "06 Apr 2020"
__license__ = "MIT"
__email0__ = "g.aludino@gmail.com"
__email1__ = "gem.aludino@rutgers.edu"
__status__ = "Debug"

CHAIN_LINK = '--------------------------------------------------------------'

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
    
    try:
        with open(input_file_str, 'r') as input_file:
            output_list = [line.rstrip() for line in input_file]
            print('[utils]: SUCCESS - Input file \'{}\' opened.\n'.format(input_file_str))

            input_file.close()
    except IOError:
        print('[utils]: ERROR - Input file \'{}\' not found.\n'.format(input_file_str))
    
    return output_list

def str_to_list(input_str, delim):
    output_list = []
    
    output_list = [word.strip() for word in input_str.split(delim)]
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

    if len(input_list) == 0:
        print('[utils]: ERROR - cannot use write_to_file_from_list using empty input_list.')
        return

    if flag is 'w':
        message = ('overwrite', 'written')
    elif flag is 'a':
        message = ('append to', 'appended')
    else:
        print('[utils]: ERROR - flag must be \'w\' for write or \'a\' for append.')
        return

    if path.isfile(output_file_str):
        print('[utils]: NOTE - Output file {} exists. Will {} existing contents.'.format(output_file_str, message[0]))
    else:
        print('[utils]: NOTE - New file {} will be created for output.'.format(output_file_str))

    with open(output_file_str, flag) as output_file:
        for line in input_list:
            output_file.write(line + '\n')

    print('[utils]: SUCCESS - Contents of successfully {} to {}.'.format(message[1], output_file_str))

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
    