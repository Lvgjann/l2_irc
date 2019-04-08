#!/usr/bin/python3

import socket
import sys
import thread


def __init__():
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return s

users = {}
channels = {}
irc = {
    'host': '127.0.0.1',
    'port': 1459,
}

def get_user(user):
    command = s.recvfrom(4096)
    user.update({command[0] : command[1]})

def channel_list():
    for c in channels:
        print (channels.keys(c)
        
def join_channel(channel):
    ## TO DO
    
def create_channel(channel):
    
        
def join(channel):
    c = 0
    while (channels.values(c) != channel && c <= len(channels)):
        c = c + 1
    if (c > len(channels)):
        create_channel(channel)
    join_channel(channel)
    
def who():
    for u in users:
        print (users.values(u))
        
def private(data):
    ## TO DO

def leave():
    ## TO DO

def disconnect():
    ## TO DO
    
def kick(user):
    ## TO DO
    
def kill(user):
    ## TO DO
    
def ban(user):
    ## TO DO

def start(s):
    s.bind((irc['host'], irc['port']))
    while True :
        s.listen(5)
        command = s.recvfrom(4096)
        data = command[0]
        if data == '/LIST':
            channel_list()
        elif '/JOIN' in data:
            tmp = data.split(' ')
            join(tmp[1])
        elif data == '/WHO':
            who()
        elif data == 'PRV_MSG':
            tmp = data.split(' ')
            private(tmp[1])
        elif data == '/LEAVE':
            leave()
        elif data == '/BYE':
            disconnect()
        elif data == '/KICK':
            tmp = data.split(' ')
            kick(tmp[1])
        elif data == '/KILL':
            tmp = data.split(' ')
            kill(tmp[1])
        elif data == '/BAN':
            tmp = data.split(' ')
            ban(tmp[1])
        else:
            break # A MODIFIER ASAP
            



### MAIN ###

s = __init__()
start(s)

