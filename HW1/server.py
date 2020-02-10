#!/usr/bin/python3
"""server.py
    HW1: Programming Exercise (server socket portion)

    Rutgers University
        School of Arts and Sciences
            (01:198:352) Internet Technology
            Professor Nath Badri
            Section 02

    Assignment synopsis:
        This HW is to let your explore the socket programming interface in
        Python. This exercise will serve as the foundation for the upcoming
        programming projects. A sample working code is given to you in HW1.py.
        The program consists of server code and client code written as two
        separate threads. Understand the functionality implemented in the
        program.

    Copyright © 2020 Gemuele Aludino

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

from os import EX_OK

import sys
import threading
import time
import random
import socket

__author__ = "Gemuele (Gem) Aludino"
__copyright__ = "Copyright © 2020, Gemuele Aludino"
__date__ = "10 Feb 2020"
__license__ = "MIT"
__email0__ = "g.aludino@gmail.com"
__email1__ = "gem.aludino@rutgers.edu"
__status__ = "Debug"

PORTNO: int = 50007
BUFFER_SIZE: int = 128
UTF_8: str = 'utf-8'

TEST_STR: str = 'HELLO'

def strtoascii_str(src: str, delim: str) -> str:
    """Takes a string and converts it into an ascii-equivalent string,
    with each character delimited, save the last

        Args:
            src: str
                The source string
            delim: char
                The delimiter string
        Returns:
            The resultant ascii string, e.g.
                input 'HELLO' returns '72<delim>69<delim>76<delim>76<delim>79'
        Raises:
            (none)
    """
    dst: str = ''
    
    for c in src:
        dst += str(ord(c))

        if c is src[-1]:
            break
        else:
            dst += delim

    return dst    

def server(portno: int) -> int:
    """Creates a server socket and listens for client connection requests

        Args:
            portno: int
                Port number to bind server socket to
        Returns:
            see sys.exit
        Raises:
            (none)
    """
    ssock: tuple
    server_binding: tuple

    hostname: str = ' '
    localhost_ip: str = ' '
    
    msg_out: str = ' '
    msg_in: str = ' '
    buff_out: bytes = []
    buff_in: bytes = []

    try:
        ssock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('[S]: Server socket created\n')
    except socket.error:
        print('{} \n'.format('Server socket open error\n', socket.error))

    server_binding = ('', portno)

    ssock.bind(server_binding)
    ssock.listen(1)

    hostname = socket.gethostname()

    print('[S]: Server host name is:', hostname)
    
    localhost_ip = socket.gethostbyname(hostname)
    print('[S]: Server IP address is: {}\n'.format(localhost_ip))
    
    (csock, addr) = ssock.accept()
    
    print('[S]: Received connection request from a client at', addr, '\n')

    msg_out = 'hello, from server to client'
    print('[C]: Message sending to client: \'{}\''.format(msg_out))
    csock.send(msg_out.encode(UTF_8))

    msg_in = csock.recv(BUFFER_SIZE)

    print('[C]: Message received from client: \'{}\''.format(msg_in.decode(UTF_8)))

    msg_out = strtoascii_str(TEST_STR, '_')
    print('[C]: Message sending to client: \'{}\''.format(msg_out))
    csock.send(msg_out.encode(UTF_8))

    print('')
    ssock.close()
    return exit()

def main(argv: [str]) -> int:
    """Main function, where server function is called

        Args:
            Command line arguments (as per sys.argv)
        Returns:
            Exit status, by default, 0 upon exit
        Raises:
            (none)
    """
    server(PORTNO)
    #print(strtoascii_str(TEST_STR, '_'))
    return EX_OK

if __name__ == '__main__':
    """
        Program execution begins here.
    """
    retval = main(sys.argv)

