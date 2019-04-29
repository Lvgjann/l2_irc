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
    # Client[string] : Nick[string]
}
users = {
    # Nick[string] : IP[string]      
}
dead = []
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


def get_user(n):
    """
        Return the user from the user list.

     :param n: Searched user.
    """
    try:
        return users[n]
    except Exception as e:
        print('Error: Cannot find the user %s.' % n)
        logging.exception(e)


def get_client_from_user(user):
    """
        Return the client matching to its user.

    :param user: User to match
    """
    try:
        for c, n in client_to_user.items():
            if n == user:
                return c
        return ""
    except Exception as e:
        print('Error: Cannot find the matching user.')
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


def is_in_channel(user):
    for k, v in channels.items():
        if user in v:
            return True
        elif (set_admin(user)) in v:
            return True
    return False


def get_channel_from_user(user):
    """
        Return the channel from an user.

    :param user: Searched user.
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


def is_error_get(f, param):
    try:
        f(param)
        return False
    except Exception as e:
        logging.exception(e)
        return True


def is_unique_nick(n):
    if n in users:
        return False
    return True


def is_admin(user):
    try:
        channel = get_channel_from_user(user)
        if set_admin(user) in channels[channel]:
            return True
        return False
    except Exception as e:
        print('Error: Cannot find user %s.' % user)
        logging.exception(e)


def test_admin(user):
    """
        return true if the user is administrator
    :param user: The target user.
    """
    try:
        return user.startswith('@') and user.endswith('@')
    except Exception as e:
        print('Error: Cannot find user %s.' % user)
        logging.exception(e)


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
    msg = ''
    for c in channels.keys():
        print(c)
        msg = msg + c + '\n'
    if msg == '':
        msg = "There is no channel active on this server."
    return msg


def join(channel, user):
    """
        Add an user to a channel

    :param user: Joining user.
    :param channel: Target channel.
    """
    try:
        if channel not in channels:
            channels.update({channel: [set_admin(user)]})
            print('Created channel %s.' % channel)
        else:
            channels[channel].append(user)
    except Exception as e:
        print('Error: Cannot join or create the channel %s.' % channel)
        logging.exception(e)


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
        print('Error: Cannot find the channel %s' % channel)
        logging.exception(e)


def set_admin(user):
    """
        set a user as admin
    :param user: the target user.
    """
    user = '@' + user + '@'
    return user


def revoke(user):
    try:
        if is_admin(user):
            return user.split('@')[1]
    except Exception as e:
        print('Error: %s is not administrator.' % user)
        logging.exception(e)


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
        if is_admin(user):
            delete_channel(channel)
        else:
            list_user = get_users_from_channel(channel)
            if user in list_user:
                list_user.remove(user)
            elif set_admin(user) in list_user:
                list_user.remove(set_admin(user))
            channels[channel] = list_user
    except Exception as e:
        print('Error : Cannot find user or channel.')
        logging.exception(e)


def rename(name, client):
    try:
        message = ''
        if name in channels:
            message = ("This channel already exist, please try again with another name.\n")
        channel = get_channel_from_user(get_user_from_client(client))
        list_users = channels[channel]
        delete_channel(channel)
        channels.update({name: list_users})
        return (message)
    except Exception as e:
        print('Error : Cannot find user or channel.')
        logging.exception(e)

def disconnect(client):
    """
        Close the connection with the IRC server
    """
    # TODO : Correct this shit
    try:
        if get_channel_from_user(client):
            leave(client)
        users.pop(get_user_from_client(client))
        client.shutdown(1)
    except Exception as e:
        logging.exception(e)


def kick(user, channel):
    """
        Remove an user from a channel

    :param user: The target user.
    :param channel: The target channel.
    """
    channels[channel].remove(user)


"""def kill(client):
    try:
        usr = get_user_from_client(client)
        c = get_channel_from_user(client)
        c.remove(usr)
        # Close connection
        disconnect(client)
    except Exception as e:
        print('Error: cannot find target client.')
        logging.exception(e)"""


"""def ban(client):
    try:
        usr = get_user_from_client(client)
        c = get_channel_from_user(client)
        c.remove(usr)
        # Close connection
        banlist.update(usr)
        disconnect(client)
    except Exception as e:
        print('Error: cannot find target client.')
        logging.exception(e)"""


def private(client, msg, sender):
    try:
        message = '<%s> is wispering you - ' % sender
        message = message + msg
        client.sendall(message.encode())
    except Exception as e:
        print ('Error: the client didn\'t exit.\n')
        logging.exception(e)


def send_msg_channel(msg, user):
    channel = get_channel_from_user(user)
    message = '<%s> - ' % user
    message = message + msg

    if channel is not None:
        list_user = get_users_from_channel(channel)
        for c in list_user:
            if (c != user) and (c != set_admin(user)):
                if is_admin(c):
                    c = revoke(c)
                client = get_client_from_user(c)
                client.sendall(message.encode())


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


def start():
    """
        Start and loop the IRC server.
    """
    # tty.setraw(sys.stdin)
    global alive
    print('Starting server...')
    connected_clients = []
    while True:
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
                for p in range (1, len(tmp)):
                    param.append(tmp[p])
                # Read the command and the possible parameters

                if command == 'NICK':
                    print('Entering /NICK function')
                    if is_unique_nick(param[0]):
                        nick(param[0], client)
                        message = 'Your nick is : %s\n' % param[0]

                    else:
                        message = 'Error : Nickname already used.'
                        print(message)

                elif command == 'LIST':
                    print('Entering /LIST function')
                    message = channel_list()
                    print("list : " + message)

                elif command == 'JOIN':
                    join(param[0], get_user_from_client(client))
                    message = "You joined the channel %s\n" % param[0]
                    print('<%s> has joined the channel %s.' % (get_user_from_client(client), param[0]))

                elif command == 'WHO':
                    print('Entering /WHO function')
                    if is_in_channel(get_user_from_client(client)):
                        message = who(get_channel_from_user(get_user_from_client(client)))
                        print(message)
                    else:
                        message = 'You are not in a channel.'

                elif command == 'MSG':
                    private(get_client_from_user(param[0]), param[1], get_user_from_client(client))

                elif command == 'LEAVE':
                    print('Entering /LEAVE function')
                    old_channel = get_channel_from_user(get_user_from_client(client))
                    leave(get_user_from_client(client))
                    message = "You leave the channel %s\n" % old_channel
                    print('<%s> has left the channel %s.' % (get_user_from_client(client), old_channel))

                elif command == 'BYE':
                    dead.append(client)
                    connected_clients.remove(client)
                    break

                elif command == 'KICK':
                    kick(param[0], param[1])

                elif command == 'KILL':
                    kill(param[0])

                elif command == 'BAN':
                    ban(param[0])

                elif command == 'HELP':
                    message = help_command()

                elif command == 'REN':
                    test = rename(param[0], client)
                    channel = get_channel_from_user(get_user_from_client(client))
                    if test == '': 
                        message = "Channel %s was rename to %s" % (channel, param[0])
                        print(message)

                elif command == 'ERROR':
                    print('Entering wrong function')
                    message = 'Error. Unknown command, try "/HELP" to see the commands\n'

                elif command == 'ACK':
                    message = 'ACK'

                else:
                    message = data
                    channel_msg = True

                if channel_msg:
                    send_msg_channel(message, get_user_from_client(client))
                    message = ''

                client.sendall(message.encode())
        for d in dead:
            d.close()


""" MAIN """

main_connection = __init__()
print("Initialization done.\n")
start()
main_connection.close()
