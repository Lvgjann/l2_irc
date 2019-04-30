#!/usr/bin/python3

import logging
import select
import socket
import sys
import threading
import tty

clients = {
    # Client[string] : Nick[string]
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
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((irc['host'], irc['port']))
    sock.listen(5)
    return sock


""" GETTERS AND CHECKERS """


def __log__(err, e):
    print('Error: %s' % err)
    logging.exception(e)


def get_channel(channel):
    """
    :param channel: Searched channel.
    :return: channel from the channel list.
    """
    try:
        return channels[channel]
    except Exception as e:
        __log__('Cannot find the channel %s.' % channel, e)


def get_user(u):
    """
     :param u: Searched user.
     :return: the user from the usr list.
    """
    try:
        return users[u]
    except Exception as e:
        __log__('Cannot find the user %s.' % u, e)


def get_client_from_user(user):
    """
    :param user: User to match
    :return: client matching to its user
    """
    try:
        for c, n in clients.items():
            if n == user:
                return c
        return ""
    except Exception as e:
        __log__('Cannot find the target client.', e)


def get_user_from_client(client):
    """
    :param client: Client to match
    :return: the user matching to its client.
    """
    try:
        usr = clients.get(client)
        return usr if usr else ""
    except Exception as e:
        __log__('Cannot find the target user.', e)


def get_users_from_channel(channel):
    """
    @:param channel: Searched channel.
    :return: the users from a channel.
    """
    try:
        c = channels.get(channel)
        return c
    except Exception as e:
        __log__('Cannot find the target users.', e)


def get_channel_from_user(user):
    """
    :param user: Searched user.
    :return: the channel from a user in it.
    """
    try:
        for k, v in channels.items():
            if user in v:
                return k
            elif set_admin(user) in v:
                return k
    except Exception as e:
        print('Error: Cannot find the matching channel')
        logging.exception(e)


def is_in_channel(u):
    """
    :return: if the user u is in the channel.
    """
    for k, v in channels.items():
        if u in v:
            return True
        elif (set_admin(u)) in v:
            return True
    return False


def is_error_get(f, param):
    """
    :return: if something is going wrong. Basically, it should not, let's just hope it keeps going on this way. Please.
    """
    try:
        f(param)
        return False
    except Exception as e:
        __log__('Just. Error.', e)


def is_unique_nick(n):
    """
    :return: if the nick n is unique.
    """
    try:
        return n in users.keys()
    except Exception as e:
        __log__('Cannot find any user with nickname %s' % n, e)


def is_admin(user):
    """
    :return: if the user u is an administrator.
    """
    try:
        channel = get_channel_from_user(user)
        return set_admin(user) in channels[channel]
    except Exception as e:
        __log__('Cannot find user %s.' % user, e)


def test_admin(user):
    """
        Return true if the user is administrator
    :param user: The target user.
    """
    try:
        return user.startswith('@') and user.endswith('@')
    except Exception as e:
        __log__('Cannot find the target user %s' % user, e)


""" IRC FUNCTIONS """


def nick(nickname, client):
    """
        Define or redefine a nickname for a client
    :param nickname: Nickname to update.
    :param client: Client to update.
    """
    try:
        clients.update({client: nickname})
        users.update({nickname: "127.0.0.1"})
        print('<%s> is connected.' % nickname)
    except Exception as e:
        __log__('Invalid client or nickname.', e)


def channel_list():
    """
        Display the channel list.
    """
    print('Active channels : \n')
    if channels:
        msg = ''
        for c in channels.keys():
            msg = msg + c + '\n'
    else:
        msg = "There is no active channel on this server."
    return msg


def join(channel, user):
    """
        Add an user to a channel
    :param user: Joining user.
    :param channel: Target channel.
    """
    try:
        if channel in channels:
            channels[channel].append(user)
        else:
            channels.update({channel: [set_admin(user)]})
            print('Created channel %s.' % channel)
    except Exception as e:
        __log__('Cannot join or create the channel %s.' % channel, e)


def who(channel):
    """
        Display the present users in a channel.
    :param channel: The target channel.
    """
    msg = 'Users in the channel ' + channel + ':\n'
    try:
        current_users = get_users_from_channel(channel)
        for u in current_users:
            msg = msg + u + '\n'
        return msg
    except Exception as e:
        __log__('Cannot find target channel.', e)


def set_admin(user):
    """
        Set a user as admin
    :param user: The target user.
    """
    try:
        user = '@' + user + '@'
        return user
    except Exception as e:
        __log__('Invalid user.', e)


def set_new_admin(user):
    """
        Set a user as admin
    :param user: The target user.
    """
    try:
        channel = get_channel_from_user(user)
        new_user = set_admin(user)
        channels[channel].remove(user)
        channels[channel].append(new_user)
    except Exception as e:
        __log__('Invalid user.', e)


def revoke(user):
    """
        Set an admin to simple user.
    :param user: The target user.
    """
    try:
        return user.split('@')[1]
    except Exception as e:
        __log__('Invalid user.', e)


def delete_channel(channel):
    """
        Remove a channel.
    :param channel: The target channel.
    """
    try:
        del channels[channel]
    except Exception as e:
        __log__('Invalid channel.', e)


def remove_user_from_channel(user):
    channel = get_channel_from_user(user)
    list_user = get_users_from_channel(channel)

    if user in list_user:
        list_user.remove(user)
    elif set_admin(user) in list_user:
        list_user.remove(set_admin(user))


def leave(user):
    """
        Remove an user from a channel.
    :param user: User to remove.
    """
    try:
        new_admin = False
        channel = get_channel_from_user(user)

        if is_admin(user):
            new_admin = True

        remove_user_from_channel(user)
        list_user = get_users_from_channel(channel)

        if not list_user:
            delete_channel(channel)
        elif new_admin:
            set_new_admin(list_user[0])
            channels[channel] = list_user
        else:
            channels[channel] = list_user

    except Exception as e:
        __log__('Cannot find user or channel.', e)


def remove_client_user(client):
    try:
        user = get_user_from_client(client)
        del users[user]
        del clients[clients]
    except Exception as e:
        __log__('Error : This client didn\'t exist.', e)


def rename(name, client):
    """
        Rename a channel.
    :param name: New channel name.
    :param client: Client currently in the channel.
    """
    try:
        if not is_admin(get_user_from_client(client)):
            message = "You have to be the admin to rename the channel."
        else:
            if name in channels:
                message = "This channel already exist, please try again with another name.\n"
            else:
                channel = get_channel_from_user(get_user_from_client(client))
                users_to_keep = channels[channel]
                delete_channel(channel)
                channels.update({name: users_to_keep})
                message = "Channel %s was rename to %s" % (channel, name)
        return message
    except Exception as e:
        __log__('Cannot find user or channel.', e)


def disconnect(client):
    """
        Close the connection with the IRC server
    """
    try:
        if get_channel_from_user(client):
            leave(client)
        users.pop(get_user_from_client(client))
        client.shutdown(1)
    except Exception as e:
        __log__("Cannot find targe client.", e)


def kick(user_admin, user_to_kick):
    """
        Remove an user from its channel
    :param user_admin: The kicker user.
    :param user_to_kick: The target user.
    """
    try:
        a = True
        channel = get_channel_from_user(user_admin)
        if not is_admin(user_admin):
            message = "You must be the admin to kick someone from the channel."
            a = False
        else:
            leave(user_to_kick)
            message = "%s was removed from %s by the admin" % (user_to_kick, channel)
        return message,a
    except Exception as e:
        __log__("Invalid user or channel.", e)


"""def kill(client):
    try:
        usr = get_user_from_client(client)
        c = get_channel_from_user(client)
        c.remove(usr)
        # Close connection
        disconnect(client)
    except Exception as e:
        __log__('Cannot find target client.', e)"""

"""def ban(client):
    try:
        usr = get_user_from_client(client)
        c = get_channel_from_user(client)
        c.remove(usr)
        # Close connection
        banlist.update(usr)
        disconnect(client)
    except Exception as e:
        __log__('Cannot find target client.', e)"""


def private_message(client, msg, sender):
    """
        Send a private to an user.
    :param client: Target client.
    :param msg: Message to send.
    :param sender: Client who sends the message.
    """
    try:
        message = '<%s> is wispering to you - ' % sender + msg
        client.sendall(message.encode())
    except Exception as e:
        __log__('Cannot find target client.', e)


def send(client, path, sender):
    """
        Send a file to an user
    :param client:
    :param path:
    :param sender:
    """


def channel_message(msg, channel, user):
    message = '<%s> - ' % user + msg

    if channel is not None:
        list_user = get_users_from_channel(channel)
        for c in list_user:
            if (c != user) and (c != set_admin(user)):
                if test_admin(c):
                    c = revoke(c)
                client = get_client_from_user(c)
                client.sendall(message.encode())


def current(client):
    try:
        return get_channel_from_user(get_user_from_client(client))
    except Exception as e:
        __log__('Cannot find target channel. The client may not be in a channel.', e)


def grant_client(admin, user):
    try:
        a = True
        if not is_admin(admin):
            message = "You must be the admin to grant someone in the channel."
            a = False
        else:
            set_new_admin(user)
            message = "Welcome to the new admin : %s" % user
        return message, a
    except Exception as e:
        __log__('Invalid user.', e)


def help_command():
    return ('\n\nThis is the list of the commands available on this server :\n'
            '-> /HELP: print this message ;\n'
            '-> /LIST: list all available channels on server ;\n'
            '-> /JOIN <channel>: join (or create) a channel ;\n'
            '-> /LEAVE: leave current channel ;\n'
            '-> /WHO: list users in current channel ;\n'
            '-> <message>: send a message in current channel ;\n'
            '-> /MSG <nick> <message>: send a private message in current channel ;\n'
            '-> /BYE: disconnect from server ;\n'
            '\nIf you\'re admin on your channel :\n'
            '--> /KICK <nick>: kick user from current channel [admin] ;\n'
            '--> /REN <channel>: change the current channel name [admin] ;\n')


# TODO : This function must be the if/elif block treating the command sent in the start()
# def get_data(client, command, parameters):



def start():
    """
        Start and loop the IRC server.
    """
    # tty.setraw(sys.stdin)
    print('Starting server...')
    connected_clients = []
    while True:
        dead = []
        message = ''
        channel_msg = False
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
                for p in range(1, len(tmp)):
                    param.append(tmp[p])
                # Read the command and the possible parameters

                # TODO : get_data() expected call
                if command == 'NICK':
                    print('Entering /NICK function')
                    if not is_unique_nick(param[0]):
                        nick(param[0], client)
                        message = 'Your nick is : %s\n' % param[0]
                    else:
                        message = 'Error : Nickname already used, please try again with the command /NICK <nick>.'
                        print(message)

                elif command == 'LIST':
                    print('Entering /LIST function')
                    message = channel_list()
                    print("list : " + message)

                elif command == 'JOIN':
                    join(param[0], get_user_from_client(client))
                    message = 'has joined the channel %s.' % param[0]
                    print(message)
                    channel_message(message, get_channel_from_user(get_user_from_client(client)),
                                    get_user_from_client(client))
                    message = "You joined the channel %s\n" % param[0]

                elif command == 'WHO':
                    print('Entering /WHO function')
                    if is_in_channel(get_user_from_client(client)):
                        message = who(get_channel_from_user(get_user_from_client(client)))
                        print(message)
                    else:
                        message = 'You are not in a channel.'

                elif command == 'GRANT':
                    grant_client(client, param [0])

                elif command == 'MSG':
                    private_message(get_client_from_user(param[0]), param[1], get_user_from_client(client))

                elif command == 'LEAVE':
                    old_channel = get_channel_from_user(get_user_from_client(client))
                    leave(get_user_from_client(client))
                    message = "has left the channel %s." % old_channel
                    print(message)
                    channel_message(message, old_channel, get_user_from_client(client))
                    message = 'You left the channel %s' % old_channel

                elif command == 'BYE':
                    dead.append(client)
                    connected_clients.remove(client)
                    break

                elif command == 'KICK':
                    message,a = kick(get_user_from_client(client), param[0])
                    print(message)
                    if a:
                        msg = "You've been kicked from %s by the admin" % get_channel_from_user(
                        get_user_from_client(client))
                    else:
                        msg = 'ACK'
                    param[0].sendall(msg.encode())
                    channel_msg = True

                elif command == 'HELP':
                    message = help_command()

                elif command == 'REN':
                    old_channel = get_channel_from_user(get_user_from_client(client))
                    message = rename(param[0], client)
                    print(message)
                    channel_message(message, old_channel, get_user_from_client(client))

                elif command == '/CURRENT':
                    message = current(client)

                elif command == 'ERROR':
                    print('Error case. Something has gone wrong.')
                    message = 'Error. Unknown command, try "/HELP" to see the commands\n'

                elif command == 'ACK':
                    message = 'ACK'

                else:
                    message = data
                    channel_msg = True

                if channel_msg:
                    channel_message(message, get_channel_from_user(get_user_from_client(client)),
                                    get_user_from_client(client))
                    message = ''

                # TODO : get_data() end of call
                client.sendall(message.encode())
        for d in dead:
            remove_client_user(d)
            d.close()


""" MAIN """

main_connection = __init__()
print("Initialization done.\n")
start()
main_connection.close()
