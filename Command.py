#denotes commands which Spot understands and can list

#example irc message for reference
#  :bowtie|24x7|brb!~sgreenbe@10.12.212.97 PRIVMSG #Spot-testing-grounds :!help

class Command:
    def __init__(self, name):
    #description of the command (these are enumerated by the 'help' command)
        self.description = ''
        #this is what we're listening for
        self.name = ''
        #what to send via irc
        self.message = ''

    #this is how we listen
    def listen_for(data):
        if action_type(data) == 'PRIVMSG':
            split_data = data.decode().split(' ')
            #get the actual command from the incoming irc
            command = split_data[len(split_data)-1]
            print(command)
            #slicing [1:] gets rid of the colon ':'
            if command[1:] == trigger + name:
                irc.send(bytes("PRIVMSG {} :{}\r\n".format(channel, message), "UTF-8"))
                    
