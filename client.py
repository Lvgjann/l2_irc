#!/usr/bin/python3

import logging
import socket
import sys

irc = {
    'host': '',
    'port': 1459,
}

user = {
    'nick': 'nick',
    'ip': 'userIp',
}


def __log__(e):
    """
        Return the error log.
    """
    logging.exception(e)


def is_client_valid(client):
    """
        Check if the client is valid.
    @param client: Target client.
    """
    if not client:
        print("Error. You must specify a client.")
        return False
    return True


def irc_conn():
    """
        Establish connection with the IRC server.
    """
    try:
        print('Connecting to the server : {port}...'.format(**irc))
        s.connect((irc['host'], irc['port']))
    except socket.error:
        print('Error connecting to IRC server {host}:{port}'.format(**irc))
        sys.exit(1)


def send_data(data):
    """
        Send a data to the server.

    @param data: Data block to send
    """
    s.send(data.encode())


def join(channel):
    """
        Join a channel

    @param channel: Target channel.
    """
    try:
        send_data("JOIN %s" % channel)
    except ValueError as e:
        print('Error. You must specify a channel to join.')
        __log__(e)


def nick():
    """
        Define a nick for a user.

    """
    try:
        nickname = input('Choose a nickname:')
        send_data('NICK %s' % nickname)
        return nickname
    except Exception as e:
        __log__(e)
    


def channel_list():
    """
        Display the channel list.
    """
    send_data("LIST")


def who():
    """
        Display the users in the current channel.
    """
    send_data("WHO")


def private(usr):
    """
        Send a private message to an user
    @:param user
    """
    try:
        send_data("MSG %s" % usr)
    except ValueError as e:
        print('Error. Empty message.')
        __log__(e)


def leave():
    """
        Leave the current channel
    """
    send_data("LEAVE")


def disconnect():
    """
        Leave the server
    """
    send_data("BYE")
    
def rename(channel):
    """
        Rename channel
    @param channel: The new name of the channel
    """
    send_data("REN %s" % channel)

"""ADMINISTRATOR COMMANDS"""


def kick(client):
    """
        Kick the client from its channel.

    @param client: Target client.
    """
    if is_client_valid(client):
        send_data("KICK %s" % client)


def kill(client):
    """
        Kick the client from the server.

    @param client: Target client.
    """
    if is_client_valid(client):
        send_data("KILL %s" % client)


def ban(client):
    """
        Kick the client from the server and ban its IP

    @param client: Target client
    """
    if is_client_valid(client):
        send_data("BAN %s" % client)

def help():
    print('/LIST : Display the current channels ;\n'
              '/JOIN + channel : Join the channel "channel". If it doesn\'t exist, create and join ;\n'
              '/WHO : Display the current user of the channel ;\n'
              '/MSG + user : Send a private message to the user "user" ;\n'
              '/LEAVE : Leave the channel ;\n'
              '/BYE : Quit the server ;\n\n'
              'IF YOU\'RE ADMIN : \n'
              '-> /KICK + user : Leave the user "user" of the current channel ;\n'
              '-> /KILL + user : Disconnect the user "user" ;\n'
              '-> /BAN + user : Disconnect the user "user" and blacklists the IP address ;\n')

""" MAIN """

# Opening a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
# Connects to the IRC server
irc_conn()
# Defines a nickname
nickname = nick()
print ("You choose the nick %s, you can use the command below : \n" % nickname)
help()

while True:
    command = input('')
    if command == '/LIST':
        channel_list()
    elif '/JOIN' in command:
        tmp = command.split(' ')
        join(tmp[1])
    elif command == '/WHO':
        who()
    elif command == 'MSG':
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
    elif command == '/REN':
        tmp = command.split(' ')
        rename(tmp[1])
    elif command == '/HELP':
        help()
    elif command.find('/'):
        print('Error. Unknown command, try "/HELP" to see the commands\n')
    else:
        send_data(command)
