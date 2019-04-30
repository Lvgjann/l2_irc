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


""" IRC FUNCTIONS """


def __log__(e):
    """
        Return the error log.
    """
    logging.exception(e)


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


""" COMMANDS FUNCTIONS """

def nick_first():
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


def nick(n):
    """
        Define a nick for a user.

    :param n:
    """
    try:
        send_data('NICK %s' % n)
    except Exception as e:
        print('Error: nickname cannnot be empty.')
        __log__(e)


def private(n, msg):
    """
        Send a private message to an user

    :param msg: the private message
    :param n: the user 
    """
    try:
        send_data("MSG %s %s" % (n, msg))
    except ValueError as e:
        print('Error: nickname cannot be empty.')
        __log__(e)


def current(channel):
    try:
        send_data("CURRENT %s" % channel)
    except ValueError as e:
        print('Error: channel cannot be empty.')
        __log__(e)


def send(nick, path):
    try:
        send_data("SEND %s %s" % (nick, path))
    except ValueError as e:
        print('Error: nick and path cannot be empty.')
        __log__(e)


def recv(path):
    try:
        send_data("RECV %s %s" % path)
    except ValueError as e:
        print('Error: path cannot be empty.')
        __log__(e)

"""ADMINISTRATOR COMMANDS"""

def kick(n):
    """
        Kick the client from its channel.

    :param u: Target client.
    """
    try:
        send_data("KICK %s" % n)
    except Exception as e:
        print('Error: nickname cannot be empty')
        __log__(e)


def rename(channel):
    """
        Rename channel

    :param channel: The new name of the channel
    """
    try:
        send_data("REN %s" % channel)
    except ValueError as e:
        print('Error: channel cannot be empty')
        __log__(e)


def grant(n):
    """
        Grant admin privileges to as user
    
    :param u: the user to grant
    """
    try:
        send_data("GRANT %s" % n)
    except ValueError as e:
        print('Error: nickname cannot be empty')
        __log__(e)



def revoke(n):
    """
        Revoke admin privilege from a user
    
    :param u: the user to revoke
    """
    try:
        send_data("GRANT %s" %n)
    except Exception as e:
        print('Error: nickname cannot be empty')
        __log__(e)


def send_msg():
    error = False
    tmp = []

    i, o, e = select.select([sys.stdin], [], [], 0.5)

    command = 'ACK' if not i else sys.stdin.readline().strip()

    # entered a command
    if command != 'ACK':
        # is a simple command
        if command == '/HELP':
            send_data("HELP")
        elif command == '/LIST':
            send_data("LIST")
        elif command == '/LEAVE':
            send_data("LEAVE")
        elif command == '/WHO':
            send_data("WHO")
        elif command == '/BYE':
            send_data("BYE")
        elif command == '/HISTORY':
            send_data("HISTORY")
        
        # is a command with parameters
        elif '/' in command:
            tmp.append((command.split()))

            if '/JOIN' in command:
                if len(tmp[0]) != 2:
                    error = True
                else:
                    join(tmp[0][1])

            elif '/MSG' in command:
                if len(tmp[0]) < 3:
                    error = True
                else:
                    tmp_user = []
                    for i in range (1, len(tmp[0]) - 1):
                        print ("i : %d" % i)
                        tmp_user.append(tmp[0][i])
                    private(tmp_user, tmp[0][len(tmp[0]) - 1])

            elif '/KICK' in command:
                if len(tmp[0]) != 2:
                    error = True
                else:
                    kick(tmp[0][1])

            elif '/REN' in command:
                if len(tmp[0]) != 2:
                    error = True
                else:
                    rename(tmp[0][1])
            
            elif '/CURRENT' in command:
                if len(tmp[0]) > 2:
                    error = True
                elif len(tmp[0]) == 1:
                    channel = ''
                    current(channel)
                else:
                    current(tmp[0][1])

            elif '/NICK' in command:
                if len(tmp[0]) != 2:
                    error = True
                else:
                    nick(tmp[0][1])

            elif '/GRANT' in command:
                if len(tmp[0]) != 2:
                    error = True
                else:
                    grant(tmp[0][1])

            elif '/REVOKE' in command:
                if len(tmp[0]) != 2:
                    error = True
                else:
                    revoke(tmp[0][1])

            elif '/SEND' in command:
                if len(tmp[0]) != 3:
                    error = True
                else:
                    send(tmp[0][1], tmp[0][2])

            elif '/RECV' in command:
                if len(tmp[0]) != 2:
                    error = True
                else:
                    recv(tmp[0][1])

            # it's an unkown command
            else:
                error = True
                # send message

            if error:
                send_data("ERROR")
        else:
            send_data(command)
    # send ACK
    else:
        send_data(command)


""" MAIN """

# Opening a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
# Connects to the IRC server
irc_conn()
# Defines a nickname
nickname = nick_first()
print("You choose the nick %s, to see the commands, entered '/HELP' \n" % nickname)

while True:
    message = sock.recv(4096).decode()
    if message != '' and message != 'ACK':
        print(message)
    send_msg()
