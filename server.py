#!/usr/bin/python3
import socket
import select
import threading

s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 7777))
s.listen(1)

def f(s2, lock, l):
    lock.acquire()
    l.append(s2)
    lock.release()
    while True:
        string = s2.recv(1500)
        if len(string) == 0:
            print("client déconnecté")
            lock.acquire()
            s2.close()
            l.remove(s2)
            lock.release()
            break
        lock.acquire()
        for s3 in l:
            if s3 != s2:
                s3.send(string)
        lock.release()

l = []
lock = threading.Lock()
while True:
    s2, a = s.accept()
    print("nouveau client:", a)

    threading.Thread(target=f, args=(s2, lock, l)).start()
