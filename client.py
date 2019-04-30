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


def __log__(err, e):
    """
        Return the error log.
    """
    print('Error : %s' % err)
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


""" IRC FUNCTIONS """


def nick_first():
    """
        Define a nick for a user.
    """
    try:
        n = input('Choose a nickname:')
        send_data('NICK %s' % n)
        return n
    except Exception as e:
        __log__('You must specify a nickname.', e)


def join(channel):
    """
        Join a channel
    :param channel: Target channel.
    """
    try:
        send_data("JOIN %s" % channel)
    except ValueError as e:
        __log__('You must specify a channel to join.', e)


def nick(n):
    """
        Define a nickname for a user.
    :param n: Nickname to attribute.
    """
    try:
        send_data('NICK %s' % n)
    except Exception as e:
        __log__('You must specify a nickname.', e)


def private(n, msg):
    """
        Send a private message to an user.
    :param msg: the private message.
    :param n: the user .
    """
    try:
        send_data("MSG %s %s" % (n, msg))
    except ValueError as e:
        __log__('You must specify a receiver nickname.', e)


def current(channel):
    send_data("CURRENT %s" % channel)


def send(n, path):
    """
        Send a file to an user.
    :param n: Target user's nickname.
    :param path: File path.
    """
    try:
        send_data("SEND %s %s" % (n, path))
    except ValueError as e:
        __log__('You must specify a receiver nickname.', e)


def recv(path):
    """
        Receive a file.
    :param path: File path.
    """
    try:
        send_data("RECV %s %s" % path)
    except ValueError as e:
        __log__('You must specify a path.', e)


"""ADMINISTRATOR COMMANDS"""


def kick(n):
    """
        Kick the client from its channel.
    :param n: Target nickname.
    """
    try:
        send_data("KICK %s" % n)
    except Exception as e:
        __log__('You must specify a nickname.', e)


def rename(channel):
    """
        Rename channel
    :param channel: The new name of the channel
    """
    try:
        send_data("REN %s" % channel)
    except ValueError as e:
        print('Error: channel cannot be empty')
        __log__('You must specify a channel.', e)


def grant(n):
    """
        Grant admin privileges to as user
    :param n: the user to grant
    """
    try:
        send_data("GRANT %s" % n)
    except ValueError as e:
        __log__('You must specify a nickname', e)


def revoke(n):
    """
        Revoke admin privilege from a user
    :param n: the user to revoke
    """
    try:
        send_data("REVOKE %s" % n)
    except Exception as e:
        __log__('You must specify a nickname', e)


def read_command_light(command):
    """
        Command without parameter treatment.
    """
    try:
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
    except Exception as e:
        __log__('Invalid command.', e)


def read_command(command):
    """
        Comment with parameters treatment.
    """
    try:
        err = False
        tmp = [(command.split())]

        if '/JOIN' in command:
            if len(tmp[0]) != 2:
                err = True
            else:
                join(tmp[0][1])

        elif '/MSG' in command:
            if len(tmp[0]) < 3:
                err = True
            else:
                tmp_user = ''
                for i in range(1, len(tmp[0]) - 1):
                    tmp_user = tmp_user + (tmp[0][i])
                private(tmp_user, tmp[0][len(tmp[0]) - 1])

        elif '/KICK' in command:
            if len(tmp[0]) != 2:
                err = True
            else:
                kick(tmp[0][1])

        elif '/REN' in command:
            if len(tmp[0]) != 2:
                err = True
            else:
                rename(tmp[0][1])

        elif '/CURRENT' in command:
            if len(tmp[0]) > 2:
                err = True
            elif len(tmp[0]) == 1:
                channel = 'ACK'
                current(channel)
            else:
                current(tmp[0][1])

        elif '/NICK' in command:
            if len(tmp[0]) != 2:
                err = True
            else:
                nick(tmp[0][1])

        elif '/GRANT' in command:
            if len(tmp[0]) != 2:
                err = True
            else:
                grant(tmp[0][1])

        elif '/REVOKE' in command:
            if len(tmp[0]) != 2:
                err = True
            else:
                revoke(tmp[0][1])

        elif '/SEND' in command:
            if len(tmp[0]) != 3:
                err = True
            else:
                send(tmp[0][1], tmp[0][2])

        elif '/RECV' in command:
            if len(tmp[0]) != 2:
                err = True
            else:
                recv(tmp[0][1])

        else:
            err = True
            # send message

        if err:
            print('Error: Invalid arguments.')
            send_data("ERROR")
    except Exception as e:
        __log__('Invalid command or arguments.', e)


def send_msg():
    i, o, e = select.select([sys.stdin], [], [], 0.5)
    command = 'ACK' if not i else sys.stdin.readline().strip()

    # Reading a command
    if command != 'ACK' and '/' in command:
        read_command_light(command)
        read_command(command)
    else:
        send_data(command)


""" MAIN """

# Opening a socket and IRC connection
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
irc_conn()
# Defines a nickname
nickname = nick_first()
print("To see the commands, entered '/HELP' \n")

while True:
    message = sock.recv(4096).decode()

    if message.startswith('ACK'):
        message = message.split('ACK')[1]
    if message.endswith('ACK'):
        message = message.split('ACK')[0]

    if message != '':
        print(message)
    send_msg()
