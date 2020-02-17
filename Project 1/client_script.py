#!/usr/bin/python2.7
"""client_script.py
    Project 1: Recursive DNS client and DNS servers (client program automator)
 
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

from client import main
from sys import argv

"""
    Run this script using the following at the command prompt:
        $ python client_script.py 
            # for default input file name, DEFAULT_INPUT_FILE_HOSTNAMES

        $ python client_script.py [filename]
            # for custom input filename
            # e.g. python client_script.py your_file.txt
"""

DEFAULT_INPUT_FILE_HOSTNAMES = 'PROJI-HNS.txt'
DEFAULT_RS_PORTNO = 8345
DEFAULT_TS_PORTNO = 50007

input_file_str = ' '

len_argv = len(argv)

if len_argv == 1:
    input_file_str = DEFAULT_INPUT_FILE_HOSTNAMES
elif len_argv == 2:
    input_file_str = argv[1]
else:
    print('\nUSAGE:\n\t(for default input file name {})\n\tpython {}\n\n\t(for custom input file name)\n\tpython {} [filename]\n'.format(DEFAULT_INPUT_FILE_HOSTNAMES, argv[0], argv[0]))
    exit()

with open(input_file_str, 'r') as input_file:
    input_lines = [line.rstrip() for line in input_file]

args = []

for line in input_lines:
    a = []
    a.append('{}.py'.format(main.__name__))
    a.append(line)
    a.append(str(DEFAULT_RS_PORTNO))
    a.append(str(DEFAULT_TS_PORTNO))

    args.append(a)

len_args = len(args)

for i in range(len_args):
    main(args[i])
