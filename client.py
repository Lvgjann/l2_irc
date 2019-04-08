#!/usr/bin/python3

import socket
import sys

irc = {
    'host': 'localhost',
    'port': 1459,
    'channel': '#channel',
    'namesinterval': 5
}

user = {
    'nick': 'nick',
    'username': 'botuser',
    'hostname': 'localhost',
    'servername': 'localhost',
    'realname': 'Raspberry Pi Names Bot'
}


# open a connection with the server
def irc_conn():
    try:
        print('Connecting to {host}:{port}...'.format(**irc))
        s.connect((irc['host'], irc['port']))
    except socket.error:
        print('Error connecting to IRC server {host}:{port}'.format(**irc))
        sys.exit(1)


# simple function to send data through the socket
def send_data(data):
    s.send(data + '\n')


# join the channel

def join(channel):
    if not channel:
        print('Error. You must specify a channel to join.')
    else:
        send_data("JOIN %s" % channel)


# create and send username
def nick():
    nickname = input('Choose a nickname:')
    send_data("NICK " + nickname)


# Displays the channel list
def channel_list():
    send_data("LIST")


# Sees who is in the channel
def who():
    send_data("WHO")


# Private message
def private(message):
    if not message:
        print('Error. Empty message.')
    else:
        send_data("PRV_MSG %s" % message)


# Leaves the current channel
def leave():
    send_data("LEAVE")


# Disconnects
def disconnect():
    send_data("BYE")


### ADMINISTRATOR COMMANDS ###

# Checks if the client parameter is valid
def is_client_valid(client):
    if not client:
        print("Error. You must specify a client.")
        return False
    return True


# Kicks the client client
def kick(client):
    if is_client_valid(client):
        send_data("KICK %s" % client)


# Kicks the client client from the IRC
def kill(client):
    if is_client_valid(client):
        send_data("KILL %s" % client)


# Kicks the client client from the IRC and bans its IP
def ban(client):
    if is_client_valid(client):
        send_data("BAN %s" % client)


#### MAIN ####


# Opening a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
# Connects to the IRC server
irc_conn()
# Defines a nickname
nick()

while True:
    command = input('')
    if command == '/LIST':
        channel_list()
    elif '/JOIN' in command:
        tmp = command.split(' ')
        join(tmp[1])
    elif command == '/WHO':
        who()
    elif command == 'PRV_MSG':
        tmp = command.split(' ')
        private(tmp[1])
    elif command == '/LEAVE':
        leave()
    elif command == '/BYE':
        disconnect()
    elif command == '/KICK':
        tmp = command.split(' ')
        kick(tmp[1])
    elif command == '/KILL':
        tmp = command.split(' ')
        kill(tmp[1])
    elif command == '/BAN':
        tmp = command.split(' ')
        ban(tmp[1])
    elif command == '/HELP':
        print('/LIST : Displays the current channels ;\n'
              '/JOIN + channel : Join the channel "channel". If it doesn\'t exist, create and join ;\n'
              '/WHO : Displays the current user of the channel ;\n'
              '/PRV_MSG + user : Sends a private message to the user "user" ;\n'
              '/LEAVE : Leaves the channel ;\n'
              '/BYE : Quits the server ;\n'
              '/KICK + user : Leaves the user "user" of the current channel ;\n'
              '/KILL + user : Disconnects the user "user" ;\n'
              '/BAN + user : Disconnects the user "user" and blacklists the IP adress ;\n')
    elif command.find('/'):
        print('Error. Unknown command')
    else:
        send_data(command)
