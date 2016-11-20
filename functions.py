import os
import socket
#import requests

#init vars
network = 'irc.devel.redhat.com'
port = 6667
nick = 'Spot'
channel = '#kankore'
creator = 'bowtie'
trigger = '!'
irc = socket.socket (socket.AF_INET, socket.SOCK_STREAM)

#bash commands (on which to punish!)
bash_commands = ['cd', 'ls', 'll', 'cat']

#init functions
def irc_connect(network,port):
    print ('connecting to %s' % network)
    irc.connect (( network, port ))
    print (irc.recv(4096),)

def set_nick(nickname):
    irc.send (bytes('NICK %s\r\n' % nick, 'UTF-8'))
    irc.send (bytes('USER %s 8 * :bowtie\'s IRC bot\r\n'  % nick, 'UTF-8'))

def join_channel(channel):
    if not channel[0] == '#':
        channel = '#' + channel
    raw_send ('JOIN ' + channel)
    irc.send (bytes('PRIVMSG %s :Hello, my name is Spot\r\n' % creator, 'UTF-8'))

#send/receive
def raw_send(data):
    print (data)
    irc.send (bytes(data + '\r\n', 'UTF-8'))

def action_type(data):
    # this returns the type of action seen on the irc server
    # examples: PRIVMSG,NOTICE,MODE
    data = data.decode()
    action = data.split(' ')[1]
    return action

#:towey!~mtowey@10.12.213.6 PRIVMSG bowtie :ping bowtie
#irc message format

#TODO: make help/list of commands feature (possibly by having a description = var via OOP?)

#  :bowtie|24x7|brb!~sgreenbe@10.12.212.97 PRIVMSG #Spot-testing-grounds :!help
#lists viable commands (i.e. 'help')
def list_protocol(data):
    if action_type(data) == 'PRIVMSG':
        try:
            split_data = data.decode().split(' ')
            #get the actual command from the incoming irc
            command = split_data[len(split_data)-1]
            print(command)
            #slicing [1:] gets rid of the colon ':'
            if command[1:] == trigger + 'help':
            #name of person who pinged me
                irc.send (bytes('PRIVMSG {} :Here is a list of my commands:\r\n'.format(channel), 'UTF-8'))
        except IndexError:
            pass

#TODO: generalize this into one function!
def reply(data):
    #if it's a private message to Spot
    if action_type(data) == 'PRIVMSG':
        try:
            data.decode().split(' ')[4] == nick
            #name of person who pinged me
            name = data.decode().split('!')[0][1:]
            irc.send (bytes('PRIVMSG {} :Hello {}, my name is Spot.  Pleased to meet you.\r\n'.format(channel, name), 'UTF-8'))
        except IndexError:
            pass

def print_data(data):
    #decodes incoming irc data into str form
    data = data.decode()
    try:
        print(data)
    except TypeError:
        pass

def ping_pong(data):
    #TODO: unify single/double quotes
    if data.find (bytes('PING', 'UTF-8')) != -1:
        #there's probably a more elegant way to do this
        raw_send('PONG ' + data.decode().split()[1])

#salesforce functions

#https://c.na7.visual.force.com/apex/Case_View?sbstr=$CASENUMBER
#for accessing cases replace $CASENUMBER w/ case number

#  :bowtie|24x7|brb!~sgreenbe@10.12.212.97 PRIVMSG #Spot-testing-grounds :!help

#parses case numbers out of irc messages
def parse_case_number(message):

    #this is the case number to return
    case_number = ' '
    #TODO: Fix error where message ending in ':' throws IndexError
    split_on_colon = message.split(':')
    split_into_words = split_on_colon[len(split_on_colon)-1].split(' ')
    for word in split_into_words:
        if word[len(word)-1] == '!' or word[len(word)-1] == '?':
            try:
                print(word)
                #check if it's a number, slice off the last char in case it's a '?' or '!'
                int(word[:-1])
                #NOTE: this if more than one number is in the message, the last will be our result
                case_number = word[:-1]
            except ValueError:
                pass
        elif len(split_into_words) > 0:
            try:
                print(word)
                #check if it's a number, slice off the last char in case it's a '?' or '!'
                int(word)
                #NOTE: this if more than one number is in the message, the last will be our result
                case_number = word
            except ValueError:
                pass

    return case_number

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

#response formatting

#[01738903] Physical server that's using Storix for backup, after doing p2v test migration, the server won't boot.
#: WoRH, WoOwn : [Sev 3, SBT:-2919, Pri:1402] [Anaconda]
#https://c.na7.visual.force.com/apex/Case_View?sbstr=01738903

#TODO: make function to detect and shame bash commands
