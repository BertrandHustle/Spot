#!/usr/bin/env python3

#for some reason this needs to be run as
#sudo python3.5 ./main.py

import functions
import db_functions
import os
import socket
import threading
import sys
import requests

author = 'Scott Greenberg'
email = 'sgreenbe@redhat.com'
github = 'https://github.com/BertrandHustle/Spot'

#irc init
network = functions.network
port = functions.port
nick = functions.nick
channel = functions.channel
irc = functions.irc
greeting = 'Hello, my name is Spot.  Try typing a message with a case number in it! Or try to kill me!'

#database init
karma_db = db_functions.karma_db
karma_cursor = db_functions.karma_cursor
case_db = db_functions.case_db
case_cursor = db_functions.case_cursor

#group of functions to be run in main loop
main_functions = ()

def main():

    functions.irc_connect(network, port)
    functions.set_nick(nick)
    functions.join_channel(channel)
    functions.send_to_channel(channel, greeting)
    db_functions.init_dbs()

    while True:
        data = irc.recv(4096)
        data = data[:-2]
        print(data.decode())

        #functions
        functions.ping_pong(data)
        functions.reply(data)
        functions.help(data)
        functions.listen_for_spotify(data)
        functions.get_case(data)
        db_functions.listen_for_karma(data)

if __name__ == '__main__':
    main()
