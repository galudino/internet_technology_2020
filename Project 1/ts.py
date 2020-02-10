#!/usr/bin/python2.7
"""ts.py
    Project 1: Recursive DNS client and DNS servers (top-level DNS server)
 
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

# remember to remove unused imports
from os import EX_OK
from enum import Enum

import os
import sys
import socket
import threading
import time
import random

__author__ = "Gemuele (Gem) Aludino"
__copyright__ = "Copyright (c) 2020, Gemuele Aludino"
__date__ = "04 Mar 2020"
__license__ = "MIT"
__email0__ = "g.aludino@gmail.com"
__email1__ = "gem.aludino@rutgers.edu"
__status__ = "Debug"

class flag(Enum):
    A = str
    RS = str

def main(argv):
    """Main function, where client function is called

        Args:
            Command line arguments (as per sys.argv)
        Returns:
            Exit status, by default, 0 upon exit
        Raises:
            (none)
    """



    return EX_OK

if __name__ == '__main__':
    """
        Program execution begins here.
    """
    retval = main(sys.argv)
