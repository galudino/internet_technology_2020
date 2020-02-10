#!/usr/bin/python3
"""client.py
    HW1: Programming Exercise (client socket portion)
 
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

def client(hostname: str, portno: int):
    """Creates a client socket and establishes a connection with a predefined server socket
        
        Args:
            hostname: str
                The desired hostname to connect to
            portno: int
                The desired port number to bind the client socket
        Returns:
            see sys.exit
        Raises:
            (none)
    """
    csock: tuple
    server_binding: tuple
    status: int = -1

    msg_out: str = ' '
    msg_in: str = ' '
    buff_out: bytes = []
    buff_in: bytes = []
    
    try:
        csock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('[C]: Client socket created\n')
    except socket.error:
        print('{} \n'.format('Client socket open error', socket.error))
    
    server_binding = (hostname, portno)
    status = csock.connect(server_binding)

    msg_in = csock.recv(BUFFER_SIZE)

    if msg_in:
        print('[C]: Client socket connected to server\n')

    print('[C]: Message received from server: \'{}\''.format(msg_in.decode('utf-8')))

    msg_out = TEST_STR
    print('[C]: Message sending to server: \'{}\''.format(msg_out))
    csock.send(msg_out.encode(UTF_8))

    msg_in = csock.recv(BUFFER_SIZE)
    print('[C]: Message received from server: \'{}\''.format(msg_in.decode('utf-8')))

    print('')
    csock.close()
    return exit()


def main(argv: [str]) -> int:
    """Main function, where client function is called

        Args:
            Command line arguments (as per sys.argv)
        Returns:
            Exit status, by default, 0 upon exit
        Raises:
            (none)
    """
    client('localhost', PORTNO)
    return EX_OK

if __name__ == '__main__':
    """
        Program execution begins here.
    """
    retval = main(sys.argv)

