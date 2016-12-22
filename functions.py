import os
import socket
import spotipy
import re

#init vars
network = 'irc.devel.redhat.com'
port = 6667
nick = 'Spot'
channel = '#kankore'
creator = 'bowtie'

#irc boilerplate
irc = socket.socket (socket.AF_INET, socket.SOCK_STREAM)

#bash commands (on which to punish!)
bash_commands = ['cd', 'ls', 'll', 'cat', 'vim', 'tail']

#init functions
def irc_connect(network,port):
    print ('connecting to %s' % network)
    irc.connect ((network, port))
    print (irc.recv(4096),)

def set_nick(nickname):
    send_to_irc('NICK ' + nick)
    send_to_irc('USER ' + nick + ' 8 *', 'bowtie\'s IRC bot')
    #irc.send (bytes('NICK %s\r\n' % nick, 'UTF-8'))
    #irc.send (bytes('USER %s 8 * :bowtie\'s IRC bot\r\n'  % nick, 'UTF-8'))

def join_channel(channel):
    if not channel[0] == '#':
        channel = '#' + channel
    send_to_irc('JOIN ' + channel)
    send_to_irc('PRIVMSG' + creator, 'Hello, my name is Spot')
    #irc.send (bytes('PRIVMSG %s :Hello, my name is Spot\r\n' % creator, 'UTF-8'))

#send/receive
#data == type of data we're sending (e.g. PRIVMSG)
#message == the message we're sending in plain text

def send_to_irc(data, message = None):
    #print for debugging/dev purposes
    if message:
        irc.send (bytes(data + ' :' + message + '\r\n', 'UTF-8'))
        print (data + ' :' + message + '\r\n', 'UTF-8')
    else:
        irc.send (bytes(data + '\r\n', 'UTF-8'))
        print (data + '\r\n', 'UTF-8')

#address irc channel directly
def send_to_channel(channel, message):
    irc.send (bytes('PRIVMSG {} :{}\r\n'.format(channel, message), 'UTF-8'))

#as the name says: listens for a command from channel
def hear(data, command):
    try:
        if action_type(data) == 'PRIVMSG' and parse_message(data.decode()).startswith(command):
            return 1
        else:
            return 0
    except AttributeError:
        pass

#same as hear, but for tail commands (e.g. name++)
def reverse_hear(data, command):
    try:
        if action_type(data) == 'PRIVMSG' and parse_message(data.decode()).endswith(command):
            return 1
        else:
            return 0
    except AttributeError:
        pass

def action_type(data):
    # this returns the type of action seen on the irc server
    # examples: PRIVMSG,NOTICE,MODE
    try:
        data = data.decode()
        action = data.split(' ')[1]
        return action
    except IndexError:
        pass

#irc message format

#TODO: make help/list of commands feature (possibly by having a description = var via OOP?)
#TODO: generalize this into one function!

def reply(data):
    #if it's a private message to Spot
    if action_type(data) == 'PRIVMSG':
        try:
            if data.decode().split(' ')[4] == nick:
                #name of person who pinged me
                name = data.decode().split('!')[0][1:]
                irc.send (bytes('PRIVMSG {} :Hello {}, my name is Spot.  Pleased to meet you.\r\n'.format(channel, name), 'UTF-8'))
        except IndexError:
            pass

def ping_pong(data):
    if data.find (bytes('PING', 'UTF-8')) != -1:
    #TODO: test below to see if it's a cleaner solution
    #if 'PING' in data:
        #there's probably a more elegant way to do this
        send_to_irc('PONG ' + data.decode().split()[1])

#:towey!~mtowey@10.12.213.6 PRIVMSG bowtie :ping bowtie hey can you look at 01732845? it\'s about to breach'
#:bowtie!~sgreenbe@10.12.212.97 PRIVMSG #kankore :message

#parses incoming irc messages
def parse_message(message):
    split_on_colon = message.split(':')
    if len(split_on_colon) <= 3:
        #the actual message contained in the irc data
        return split_on_colon[len(split_on_colon)-1]
    #exception handling for messages with extra colons in them, e.g.
    #:towey!~mtowey@10.12.213.6 PRIVMSG bowtie :ping bowtie:'
    elif len(split_on_colon) == 4:
        return split_on_colon[len(split_on_colon)-2]
    else:
        print('incorrect message format')

#parses name out of incoming irc message
def parse_name(message):
    try:
        split_on_bang = message.split('!')
        #slice to remove the colon
        name = split_on_bang[0][1:]
        return name
    except IndexError:
        pass

#salesforce functions

#https://c.na7.visual.force.com/apex/Case_View?sbstr=$CASENUMBER
#for accessing cases replace $CASENUMBER w/ case number

#parses case numbers out of irc messages
def parse_case_number(message):
    message = parse_message(message)
    #split the message into individual words
    message_words_array = message.split(' ')
    for word in message_words_array:
        regex_results = re.findall('[0-9]{8}', word)
        #TODO: fix this to work for multiple case numbers
        if len(regex_results) == 1:
            return regex_results[0]

def get_case(data):
    #if it's a private message to Spot and not unifiedbot0 (temporary clause till I can do proper error handling here)
    if action_type(data) == 'PRIVMSG' and parse_name(data.decode()) != 'unifiedbot0':
        try:
            case_number = parse_case_number(data.decode())
            #TODO: this is gross, clean it up
            if int(case_number):
                if len(case_number) == 8:
                    send_to_channel(channel, 'https://c.na7.visual.force.com/apex/Case_View?sbstr=' + case_number)
        except ValueError:
            pass
        except TypeError:
            pass



#lists out Spot's functions to channel
#TODO: add all functions to this
def help(data):
    if hear(data, '!help'):
        send_to_channel(channel, '!spotify == request Spotify track')

def get_spotify_track(track_name):
    #spotipy init/boilerplate
    spotify_fetcher = spotipy.Spotify()
    #this returns a json from spotify
    search_result = spotify_fetcher.search(track_name, limit=1, offset=0, type='track')
    #ridiculous json drilling
    track_url =  search_result.get('tracks').get('items')[0].get('external_urls').get('spotify')
    return track_url

def listen_for_spotify(data):
    if hear(data, '!spotify'):
        track_name = parse_message(data.decode())[8:]
        track_url = get_spotify_track(track_name)
        if track_url.startswith('https'):
            send_to_irc('PRIVMSG ' +  channel, track_url)
        else:
            send_to_irc('Sorry, I couldn\'t find that song')




#response formatting

#[01738903] Physical server that's using Storix for backup, after doing p2v test migration, the server won't boot.
#: WoRH, WoOwn : [Sev 3, SBT:-2919, Pri:1402] [Anaconda]
#https://c.na7.visual.force.com/apex/Case_View?sbstr=01738903

#TODO: make function to detect and shame bash commands
