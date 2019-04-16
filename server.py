#!/usr/bin/python3

import logging
import select
import socket
import sys
import threading
import tty

banlist = {
    # Nick[string] : IP[string]
}
client_to_user = {
    # Client[string] : Nickname[string]
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
    return sock


def get_channel(channel):
    """
        Returns the channel from the channel list.

    :param channel: Searched channel.
    """
    try:
        return channels[channel]
    except Exception as e:
        print('Error: Cannot find the channel %s.' % channel)
        logging.exception(e)


def get_user(user):
    """
        Return the user from the user list.

     :param user: Searched user.
    """
    try:
        return users[user]
    except Exception as e:
        print('Error: Cannot find the user %s.' % user)
        logging.exception(e)


def get_user_from_client(client):
    """
        Return the user matching to its client.

    :param client: Client to match
    """
    try:
        usr = client_to_user.get(client)
        if usr:
            return usr
        else:
            return ""
    except Exception as e:
        print('Error: Cannot find the matching user.')
        logging.exception(e)


def get_users_from_channel(channel):
    """
        Return the users from a channel.

    @:param channel: Searched channel.
    """
    try:
        c = channels.get(channel)
        return c
    except Exception as e:
        print('Error: Cannot find the matching channel.')
        logging.exception(e)


def get_channel_from_user(user):
    """
        Return the channel from an user.

    :param user: Searched user.
    """
    try:
        for k, v in channels.items():
            if user in v:
                return v
    except Exception as e:
        print('Error: Cannot find the matching channel')
        logging.exception(e)


def is_error_get(f, param):
    try:
        f(param)
        return False
    except Exception as e:
        logging.exception(e)
        return True


def nick(nickname, client):
    try:
        client_to_user.update({client: nickname})
        users.update({nickname: "ffff:127.0.0.1"})
        print('<%s> is connected.' % nickname)
    except Exception as e:
        print('Error: Invalid client or nickname.')
        logging.exception(e)


def channel_list():
    """
        Display the channel list.
    """
    print('Active channels : \n')
    for c in channels.keys():
        print(c)


def join(channel, user):
    """
        Add an user to a channel

    :param user: Joining user.
    :param channel: Target channel.
    """
    try:
        if channel not in channels:
            channels.update({channel: [user]})
            print(channel)
            print('Created channel %s.' % channel)
        else:
            channels[channel].append(user)
        print('<%s> has joined the channel %s.' % (user, channel))
    except Exception as e:
        print('Error: Cannot join or create the channel %s.' % channel)
        logging.exception(e)


def who(channel):
    """
        Display the present users in a channel.

    :param channel: The target channel.
    """
    try:
        print('Users in the channel %s ' % channel)
        current_users = get_users_from_channel(channel)
        for u in current_users:
            print(u)
    except Exception as e:
        print('Error: Cannot find the channel %s' % channel)
        logging.exception(e)


def is_admin(user):
    """
        return true if the user is administrator
    :param user: The target user.
    """
    try:
        return user.startswith('@') and user.endswith('@')
    except Exception as e:
        print('Error: Cannot find user %s.' % user)
        logging.exception(e)


def set_admin(user):
    """
        set a user as admin
    :param user: the target user.
    """
    user = '@' + user + '@'
    return user


def private(user, message):
    """
        Sends a private message to an user.

    :param user: The target user.
    """
    # TODO : complete the function


def delete_channel(channel):
    """
        Removes a channel.
        
    :param channel: The target channel.
    """
    del channels[channel]


def leave(user):
    """
        Remove an user from a channel

    :param user: User to remove.
    """
    try:
        channel = get_channel_from_user(user)
        channel.remove(user)
    except Exception as e:
        print('Error : Cannot find user or channel.')
        logging.exception(e)


def disconnect(client):
    """
        Close the connection with the IRC server
    """
    client.shutdown(1)
    client.close()


def kick(user, channel):
    """
        Remove an user from a channel

    :param user: The target user.
    :param channel: The target channel.
    """
    channels[channel].remove(user)


def kill(client):
    """
        Remove an user from its current channel and close its connection.

    :param client: The target client.
    """
    try:
        usr = get_user_from_client(client)
        c = get_channel_from_user(client)
        c.remove(usr)
        # Close connection
        disconnect(client)
    except Exception as e:
        print('Error: cannot find target client.')
        logging.exception(e)


def ban(client):
    """
        Force the disconnection of a user and ban its IP address.

    :param client: The target user.
    """
    try:
        usr = get_user_from_client(client)
        c = get_channel_from_user(client)
        c.remove(usr)
        # Close connection
        banlist.update(usr)
        disconnect(client)
    except Exception as e:
        print('Error: cannot find target client.')
        logging.exception(e)


def start():
    """
        Start and loop the IRC server.
    """
    # tty.setraw(sys.stdin)
    print('Starting server...')
    connected_clients = []
    while True:
        # Verifying if new clients want to connect.
        # Listen to the irc connection, initialized in __init()__, and we wait 50ms
        asked_connections, wlist, xlist = select.select([main_connection], [], [], 0.05)
        for connection in asked_connections:
            client_connection, infos_connection = connection.accept()
            connected_clients.append(client_connection)
        # Listen the connected clients list. The clients returned by select are those which have to be read (recv)
        try:
            waiting_clients, wlist, xlist = select.select(connected_clients, [], [], 0.05)
        except select.error as e:
            logging.exception(e)
            pass
        else:
            # Get through the waitingclients
            for client in waiting_clients:
                data, ip = client.recvfrom(4096)
                data = data.decode()
                # Split the received data into 'command + parameter[i..n]' format
                tmp = data.split()
                command = tmp[0]
                param = []
                for p in tmp[1:]:
                    param.append(p)
                # Read the command and the possible parameters
                print('Command %s' % command)
                if command == 'NICK':
                    nick(param[0], client)
                elif command == 'LIST':
                    print('Entering /list function')
                    channel_list()
                elif command == 'JOIN':
                    join(param[0], get_user_from_client(client))
                elif command == 'WHO':
                    who(get_channel_from_user(client))
                elif command == 'MSG':
                    private(param[0], param)
                elif command == 'LEAVE':
                    leave(get_user_from_client(client))
                elif command == 'BYE':
                    disconnect(client)
                elif command == 'KICK':
                    kick(param[0], param[1])
                elif command == 'KILL':
                    kill(param[0])
                elif command == 'BAN':
                    ban(param[0])
                else:
                    continue


""" MAIN """

main_connection = __init__()
print("Init done\n")
start()
