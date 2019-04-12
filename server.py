#!/usr/bin/python3

import logging
import socket
import sys
import threading


def __init__():
    """
        Initialize the server socket
    """
    sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return s


def __user__():
    """
        Get the current user nickname and IP.
    """
    command = s.recvfrom(4096)
    users.update({command[0]: command[1]})
    return command[0]


banlist = {
    # Nick[string] : IP[string]
}
users = {
    # Nick[string] : IP[string]      
}
channels = {
    # Name channel[string] : List of users[list]
}
irc = {
    'host': '127.0.0.1',
    'port': 1459,
}


def get_channel(channel):
    """
        Returns the channel from the channel list.

    @param channel: Searched channel.
    """
    try:
        return channels[channel]
    except Exception as e:
        print('Error: Channel not found.')
        logging.exception(e)


def get_user(user):
    """
        Return the user from the user list.

     @param user: Searched user.
    """
    try:
        return users[user]
    except Exception as e:
        print('Error: User not found.')
        logging.exception(e)


def get_user_from_channel(channel):
    """
        Return the users from a channel.

    @param channel: Searched channel.
    """
    try:
        c = channels.get(channel)
        return c
    except Exception as e:
        print('Error: User not found.')
        logging.exception(e)


def get_channel_from_user(user):
    """
        Return the channel from an user.

    @param user: Searched user.
    """
    try:
        for c in channels:
            if user in c:
                return c
    except Exception as e:
        print('Error: Channel not found')
        logging.exception(e)


def is_error_get(f, param):
    try:
        f(param)
        return False
    except Exception as e:
        logging.exception(e)
        return True


def is_admin(user):
    """
        return true if the user is administrator
    @param user: The target user.
    """
    # TODO: complete the function


def channel_list():
    """
        Display the channel list.
    """
    for c in channels.keys():
        print(c)


def join_channel(channel):
    """
        Add the current user to the list of joined users for a channel.

    @param channel: The target channel.
    """
    user = __user__()
    channels[channel].append(user)


def create_channel(channel):
    """
        Create a new channel and add it to the channel list.

    @param channel: Channel to be created
    """
    user = __user__()
    channels[channel] = user


def join(channel):
    """
        Add an user to a channel

    @param channel: Target channel.
    """
    try:
        if channel in channels:
            join_channel(channel)
        else:
            create_channel(channel)
    except Exception as e:
        print('Error: Cannot join or create the channel.')
        logging.exception(e)


def who(channel):
    """
        Display the present users in a channel.

    @param channel: The target channel.
    """
    current_users = get_user_from_channel(channel)
    for u in current_users:
        print(u)


def set_admin(user):
    """
        set a user as admin
    @param user: the target user.
    """

    # TODO: complete the function


def private(user):
    """
        Sends a private message to an user.

    @param user: The target user.
    """
    # TODO : complete the function


def delete_channel(channel):
    """
        Removes a channel.
        
    @param channel: The target channel.
    """
    del channels[channel]


def leave():
    """
        Remove an user from a channel

    @param
    """
    # TODO : complete the function


def disconnect():
    """
        Close the connection with the IRC server
    """
    # TODO : complete the function


def kick(user, channel):
    """
        Remove an user from a channel

    @param user: The target user.
    @param channel: The target channel.
    :return:
    """
    channels[channel].remove(user)


def kill(user):
    """
        Remove an user from its current channel and close its connection.

    @param user: The target user.
    """
    # TODO : complete the function
    c = get_channel_from_user(user)
    c.remove(user)
    # Close connection


def ban(user):
    """
        Force the disconnection of a user and ban its IP address.

    @param user: The target user.
    """
    # TODO : complete the function
    c = get_channel_from_user(user)
    c.remove(user)
    # Close connection
    banlist.update(user)


def start(sock):
    """
        Start and loop the IRC server.

    @param sock: The current socket.
    """
    sock.bind((irc['host'], irc['port']))
    while True:
        sock.listen(5)
        command = sock.recvfrom(4096)
        data = command[0]
        if data == '/LIST':
            channel_list()
        elif '/JOIN' in data:
            tmp = data.split(' ')
            join(tmp[1])
        elif data == '/WHO':
            who(get_channel_from_user(usr))
        elif data == 'PRV_MSG':
            tmp = data.split(' ')
            private(tmp[1])
        elif data == '/LEAVE':
            leave()
        elif data == '/BYE':
            disconnect()
        elif data == '/KICK':
            tmp = data.split(' ')
            kick(tmp[1], tmp[2])
        elif data == '/KILL':
            tmp = data.split(' ')
            kill(tmp[1])
        elif data == '/BAN':
            tmp = data.split(' ')
            ban(tmp[1])
        else:
            pass


""" MAIN """

s = __init__()
usr = __user__()
start(s)
