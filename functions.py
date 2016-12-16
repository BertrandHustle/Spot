import os
import socket
import spotipy

#init vars
network = 'irc.devel.redhat.com'
port = 6667
nick = 'Spotty'
channel = '#spotland'
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
    if action_type(data) == 'PRIVMSG' and parse_message(data.decode()).startswith(command):
        return 1
    else:
        return 0


def action_type(data):
    # this returns the type of action seen on the irc server
    # examples: PRIVMSG,NOTICE,MODE
    data = data.decode()
    action = data.split(' ')[1]
    return action

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

#parses incoming irc messages
def parse_message(message):
    #convert to str
    split_on_colon = message.split(':')
    if len(split_on_colon) <= 3:
        #the actual message contained in the irc data
        return split_on_colon[len(split_on_colon)-1]
    #exception handling for messages with extra colons in them, e.g.
    #:towey!~mtowey@10.12.213.6 PRIVMSG bowtie :ping bowtie:'
    elif len(split_on_colon) == 4:
        return split_on_colon[len(split_on_colon)-2]
    else:
        irc.send (bytes('PRIVMSG {} :Slow down on the colons!\r\n'.format(channel), 'UTF-8'))

#salesforce functions

#https://c.na7.visual.force.com/apex/Case_View?sbstr=$CASENUMBER
#for accessing cases replace $CASENUMBER w/ case number

#  :bowtie|24x7|brb!~sgreenbe@10.12.212.97 PRIVMSG #Spot-testing-grounds :!help

#parses case numbers out of irc messages
def parse_case_number(message):

    case_number = 0
    message = parse_message(message)
    #split the message into individual words
    message_words_array = message.split(' ')

    for word in message_words_array:
        try:
            #slice the first digit in case it's a '0'
            case_number = int(word[1:])
            if case_number > 0 and case_number < 2000000:
                #we have to return this as a string so we can use it in the salesforce url
                return str(case_number)
        except ValueError:
            pass

def get_case(data):
    #if it's a private message to Spot
    if action_type(data) == 'PRIVMSG':
        try:
            case_number = parse_case_number(data.decode())
            #TODO: this is gross, clean it up
            if int(case_number):
                if len(case_number) == 8:
                    irc.send (bytes('PRIVMSG {} :https://c.na7.visual.force.com/apex/Case_View?sbstr={}\r\n'.format(channel, case_number), 'UTF-8'))
        except ValueError:
            pass

#lists out Spot's functions to channel
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
