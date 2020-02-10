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
CONFIRM_CONNECTED: str = '__CONNECTED__'
END_OF_FILE: str = '__EOF__'

def str_to_ascii_str(src: str, delim: str) -> str:
    """Takes a string and converts it into an ascii-equivalent string,
    with each character (save the last) suffixed with a delimiter

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

def ascii_str_by_socket(sock: socket):
    """Messages are received through sock and converted into ascii equivalent strings using str_to_ascii_str, and sent back via sock

        Args:
            sock: socket
                The socket connection by which communication with the
                client is implemented (AF_INET, SOCK_STREAM)
        Returns:
            (none)
        Raises:
            (none)
    """
    msg_out: str = ' '
    msg_in: str = ' '

    while True:
        msg_in = sock.recv(BUFFER_SIZE)

        if (msg_in.decode(UTF_8) == END_OF_FILE):
            break        

        print('[S]: Message received from client: \'{}\''.format(msg_in.decode(UTF_8)))    

        msg_out = str_to_ascii_str(msg_in.decode(UTF_8), '_')
        print('[S]: Message sending to client: \'{}\''.format(msg_out))
        sock.send(msg_out.encode(UTF_8))

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
        print('[S]: Server socket created.\n')
    except socket.error:
        print('[ERROR]: {} \n'.format('Server socket open error.\n', socket.error))

    server_binding = ('', portno)

    ssock.bind(server_binding)
    ssock.listen(1)

    hostname = socket.gethostname()
    print('[S]: Server host name is:', hostname)
    
    localhost_ip = socket.gethostbyname(hostname)
    print('[S]: Server IP address is: {}\n'.format(localhost_ip))
    
    (csock, addr) = ssock.accept()
    print('[S]: Received connection request from a client at', addr, '\n')

    msg_out = CONFIRM_CONNECTED
    csock.send(msg_out.encode(UTF_8))

    ascii_str_by_socket(csock)
    print('\n[S]: Finished client interaction.')

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
    return EX_OK

if __name__ == '__main__':
    """
        Program execution begins here.
    """
    retval = main(sys.argv)