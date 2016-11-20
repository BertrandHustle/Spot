#!/usr/bin/env python3


#for some reason this needs to be run as
#sudo python3.5 ./main.py

import functions
import os
import socket
import threading
import sys
import requests

author = 'Scott Greenberg'
email = 'sgreenbe@redhat.com'
github = 'https://github.com/BertrandHustle/Spot'

network = functions.network
port = functions.port
nick = functions.nick
channel = functions.channel
irc = functions.irc
greeting = 'Hello, my name is Spot.  Try typing a message with a case number in it!'


#group of functions to be run in main loop
main_functions = ()

def main():

    functions.irc_connect(network, port)
    functions.set_nick(nick)
    functions.join_channel(channel)
    irc.send (bytes('PRIVMSG {} :{}\r\n'.format(channel, greeting), 'UTF-8'))

    while True:
        data = irc.recv(4096)
        data = data[:-2]
        print(data.decode())

        #functions
        functions.ping_pong(data)
        #functions.reply(data)
        functions.list_protocol(data)
        functions.get_case(data)

if __name__ == '__main__':
    main()
