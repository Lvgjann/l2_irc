#!/usr/bin/python3

import logging
import socket
import sys
import threading


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
    'host': '',
    'port': 1459,
}


def __init__():
    """
        Initialize the server socket
    """
    sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((irc['host'], irc['port']))
    sock.listen(5)
    conn, addr = sock.accept()
    # Get data and address
    data = conn.recv(4096)
    data = data.decode()
    # Get the nick from the data (the NICK command is avoided)
    tmp = data.split(' ')
    data = tmp[1]
    users.update({data: addr})
    print ("New user : " + data)
    return sock, data


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


def channel_list():
    """
        Display the channel list.
    """
    print('Active channels : \n')
    for c in channels.keys():
        print(c)


def join_channel(channel):
    """
        Add the current user to the list of joined users for a channel.

    @param channel: The target channel.
    """
    user = usr
    channels[channel].append(user)


def create_channel(channel):
    """
        Create a new channel and add it to the channel list.

    @param channel: Channel to be created
    """
    channels.update({channel: [usr]})


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
            join_channel(channel)
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

def is_admin(user):
    """
        return true if the user is administrator
    @param user: The target user.
    """
    return (user.startswith('@') and user.endswith('@'))

def set_admin(user):
    """
        set a user as admin
    @param user: the target user.
    """
    user = '@' + user + '@'
    return user


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


def start():
    """
        Start and loop the IRC server.

    @param sock: The current socket.
    """
#    sys.setraw(sys.stdin)
    print('Starting server...')
    conn, addr = sock.accept()
    while True: 
    
        sock.listen(5)
        conn, addr = sock.accept()
        print('Listen.')
        # Get data and address
        print(conn)
        print(addr)
        print('Connection accepted.')
        data = conn.recv(4096).decode()
        print('Connection accepted.')
        # Get the ick from the data (the NICK command is avoided)
        tmp = data.split(' ')
        command = tmp[0]
        data = tmp[1]
        print('Command : %s' % command)
        print('Data : %s' % data)
        """
        command = conn.recv(4096).decode("ascii") 
        data = command[0]
        """
        if command == 'LIST':
            print('Entering /list function')
            channel_list()
        elif 'JOIN' in data:
            join(data)
        elif command == 'WHO':
            who(get_channel_from_user(usr))
        elif command == 'PRV_MSG':
            private(data)
        elif command == 'LEAVE':
            leave()
        elif command == 'BYE':
            disconnect()
        elif command == 'KICK':
            kick(data)
        elif command == 'KILL':
            kill(data)
        elif command == 'BAN':
            ban(data)
        else:
            continue


""" MAIN """

sock,usr = __init__()
print ("Init done\n")
start()

