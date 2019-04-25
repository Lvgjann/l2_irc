#!/usr/bin/python3

import logging
import socket
import sys
import select

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
    :param client: Target client.
    """
    if not client:
        print('Error: client cannot be empty.')
        return False
    return True


def irc_conn():
    """
        Establish connection with the IRC server.
    """
    try:
        print('Connecting to the server : {port}...'.format(**irc))
        sock.connect((irc['host'], irc['port']))
    except socket.error:
        print('Error: Unable to connect to IRC server {host}:{port}'.format(**irc))
        sys.exit(1)


def send_data(data):
    """
        Send a data to the server.

    :param data: Data block to send
    """
    sock.send(data.encode())


def join(channel):
    """
        Join a channel

    :param channel: Target channel.
    """
    try:
        send_data("JOIN %s" % channel)
    except ValueError as e:
        print('Error: channel cannot be empty.')
        __log__(e)


def nick():
    """
        Define a nick for a user.

    """
    try:
        n = input('Choose a nickname:')
        send_data('NICK %s' % n)
        return n
    except Exception as e:
        print('Error: nickname cannnot be empty.')
        __log__(e)


def private(usr):
    """
        Send a private message to an user
    :param usr
    """
    try:
        send_data("MSG %s" % usr)
    except ValueError as e:
        print('Error: user cannot be empty.')
        __log__(e)


def rename(channel):
    """
        Rename channel
    @param channel: The new name of the channel
    """
    try:
        send_data("REN %s" % channel)
    except ValueError as e:
        print('Error: channel cannot be empty')
        __log__(e)


"""ADMINISTRATOR COMMANDS"""


def kick(client):
    """
        Kick the client from its channel.

    :param client: Target client.
    """
    if is_client_valid(client):
        send_data("KICK %s" % client)


def kill(client):
    """
        Kick the client from the server.

    :param client: Target client.
    """
    if is_client_valid(client):
        send_data("KILL %s" % client)


def ban(client):
    """
        Kick the client from the server and ban its IP

    :param client: Target client
    """
    if is_client_valid(client):
        send_data("BAN %s" % client)


def help_command():
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


def send_msg():
    command = input('')
    
    if command == '/LIST':
        send_data("LIST")
    elif '/JOIN' in command:
        tmp = command.split()
        if (len(tmp) == 1):
            print ('Please enter a channel :')
            new = input('')
            join(new)
        else:
            join(tmp[1])
    elif command == '/WHO':
        send_data("WHO")
    elif command == 'MSG':
        tmp = command.split()
        if (len(tmp) == 1):
            print ('Please enter a name :')
            new = input('')
            private(new)
        else:
            private(tmp[1])
    elif command == '/LEAVE':
        send_data("LEAVE")
    elif command == '/BYE':
        send_data("BYE")
    elif command == '/KICK':
        tmp = command.split()
        if (len(tmp) == 1):
            print ('Please enter a name :')
            new = input('')
            kick(new)
        else:
            kick(tmp[1])
    elif command == '/KILL':
        tmp = command.split()
        if (len(tmp) == 1):
            print ('Please enter a name :')
            new = input('')
            kill(new)
        else:
            kill(tmp[1])
    elif command == '/BAN':
        tmp = command.split()
        if (len(tmp) == 1):
            print ('Please enter a name :')
            new = input('')
            ban(new)
        else:
            ban(tmp[1])
    elif command == '/REN':
        tmp = command.split()
        if (len(tmp) == 1):
            print ('Please enter a new name :')
            new = input('')
            rename(new)
        else:
            rename(tmp[1])
    elif command == '/HELP':
        help_command()
    elif command.find('/') == 0:
        print('Error. Unknown command, try "/HELP" to see the commands\n')
    else:
        send_data(command)


""" MAIN """

# Opening a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
# Connects to the IRC server
irc_conn()
# Defines a nickname
nickname = nick()
print("You choose the nick %s, you can use the command below : \n" % nickname)
help_command()
tmp = []

while True:
    message = sock.recv(4096).decode()
    if (message != ''):
        print (message)
    
    send_msg()
