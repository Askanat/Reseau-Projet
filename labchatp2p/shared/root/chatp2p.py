#!/usr/bin/python
# -*- coding: utf-8 -*-

import select
from select import select

import socket
from socket import socket
from socket import SOL_SOCKET
from socket import SO_REUSEADDR

import sys

socks = {
    'name'  : '',
    'socket': '',
    'c'     : ''
}

ipsv4   = []
ipsban  = []

BUFF_SZ       = 1024
CONFIG_FILE   = None
DEFAULT_PORT  = 1664
ENCODING      = 'utf-8'
IP_NO_FILTER  = '0.0.0.0'
PENDING_SLOTS = 999
TAB_SZ        = 5
CODE_START    = 1152
CODE_HELLO    = 2152
CODE_IPS      = 3152
CODE_PM       = 4152
CODE_BM       = 5152

CMD_BAN     = '/ban'
CMD_UNBAN   = '/unban'
CMD_QUIT    = '/quit'
CMD_PM      = '/pm'
CMD_BM      = '/bm'
CMD_IPS     = '/ips'
CMD_HELP    = '/?'


"""
    Server
"""
def create_sock():
    """Socket creator
    Attributes:
        None
    """
    s = socket()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind((IP_NO_FILTER, DEFAULT_PORT))
    return s

def create_sock_ip(ip):
    """Socket creator
    Attributes:
        ip : specific IP
    """
    if len(ipsban)>0:
        for i in range (ipsban):
            if ip == ipsban[i]:
                print("This IP %s is ban!\n"%(ip))
                return
    s = socket()
    s.connect((ip, DEFAULT_PORT))
    serv_print('Connection on: %s'%(ip), 'Debug')
    msg = "START\n"
    s.send(msg)
    return s

def serv_print(msg='', subj=''):
    """Create debug message
    Attributes:
        msg  : message for the user
        subj : header of message 
    """
    serv_printing = ''
    if subj != '' :
        serv_printing += '[=%s=] '%(subj)
    print(serv_printing + msg)


"""
    Server Command
"""
def display_help(c):
    """Command /?
    Attributes:
        c : permite to send message
    """
    msg='[=Help=] Server supports following commands:\n'
    c.send(msg.encode(ENCODING))
    msg='[=Help=] /ban /unban /quit /pm /bm /ips \n'
    c.send(msg.encode(ENCODING))

def quit_cmd(t, c, socks):
    """Command /nq
    Attributes:
        t : incoming information
        c : permite to send message
    """
    who = t.getpeername()[0]
    msg = '[=Sign-off=] %s JustLeft \n'%(who)
    c.send(msg.encode(ENCODING))

    socks['name'].remove(who)
    socks['socket'].remove(t)
    socks['c'].remove(c)

    serv_print('Has left: %s'%(t[2:]), 'Debug')

def ips_cmd(c):
    """Command /w
    Attributes:
        c : permite to send message
    """
    for i in range (socks['name']):
        msg = (ipsv4.append(socks[i]))
    c.send(msg.encode(ENCODING))

def name_cmd(t, c):
    """Command /name
    Attributes:
        t : incoming information
        c : permite to send message
    """
    if len(t[1:]) < 2:
        msg = '[=Name=] Your nickname is %s\n'%(t.getpeername()[0])
        c.send(msg.encode(ENCODING))
        serv_print('Missing a Nickname or check his name', 'Debug')
        return

    oldNick = t.getpeername()[0]
    t.getpeername()[0] = (t[2:])
    msg = '[=Name=] %s changed nicname to %s\n'%(oldNick, t.getpeername()[0])
   
    serv_print('NickName Detected: %s'%(t[2:]), 'Debug')

def msgp_cmd(t, c):
    """Command /pm
    Attributes:
        t : incoming information
        c : permite to send message
    """
    if len(t[1:]) < 2:
        msg = '[=Error=] Missing a Recipient'
        c.send(msg.encode(ENCODING))
        serv_print('Missing a Recipient', 'Debug')
        return
    else:
        serv_print('Username Detected: %s'%(t[2:]), 'Debug')

    for i in range (socks['name']):
        if (t[2:]) in socks['name']:
            c = socks[(t[2:])]['c']
    
    data = t.recv(BUFF_SZ)
    who  = t.getpeername()[0]
    msg  = '<* Private Message From : %s *> %s\n'%(who, data.strip())
    c.send(msg.encode(ENCODING))

def msgb_cmd(t, c):
    """Command /bm
    Attributes:
        t : incoming information
        c : permite to send message
    """
    for i in range (socks['name']):
        if len(ipsban) != 0:
            for j in range (ipsban):
                if socks[i] == ipsban[j]:
                    c    = socks[i]['c']
                    data = t.recv(BUFF_SZ)
                    who  = t.getpeername()[0]
                    msg  = '<* %s *> %s\n'%(who, data.strip())
                    c.send(msg.encode(ENCODING))
        else:
            c    = socks[i]['c']
            data = t.recv(BUFF_SZ)
            who  = t.getpeername()[0]
            msg  = '<* BroadCast Message From : %s *> %s\n'%(who, data.strip())
            c.send(msg.encode(ENCODING))

def ban_cmd(t, c):
    """Command /ban
    Attributes:
        t : incoming information
        c : permite to send message
    """
    if len(t[1:]) < 2:
        msg = '[=Error=] Missing a Name'
        c.send(msg.encode(ENCODING))
        serv_print('Missing a Name', 'Debug')
        return
    else:
        serv_print('Username Detected: %s'%(t[2:]), 'Debug')

    for i in range (socks['name']):
        if socks[i] == (t[2:]):
            ipsban.append((t[2:]))
            socks['name'].remove((t[2:]))
            socks['socket'].remove(t)
            socks['c'].remove(c)

def unban_cmd(t, c):
    """Command /unban
    Attributes:
        t : incoming information
        c : permite to send message
    """
    if len(t[1:]) < 2:
        msg = '[=Error=] Missing a Name'
        c.send(msg.encode(ENCODING))
        serv_print('Missing a Name', 'Debug')
        return
    else:
        serv_print('Username Detected: %s'%(t[2:]), 'Debug')

    for i in range (ipsban):
        if ipsban[i] == (t[2:]):
            ipsban.remove((t[2:]))


"""
    MAIN
"""
if __name__ == '__main__':

    name = raw_input("What is your name?")
    client = 0

    if sys.argv[1:]:
        ip = sys.argv[1:]
        s = create_sock_ip(ip[0])
        # Socket list
        socks['socket']=[s]
        client = 1
    else:
        # creat socket
        s = create_sock()
        s.listen(PENDING_SLOTS)
        serv_print('Listening on port %d'%(DEFAULT_PORT),'Waiting')
        # Socket list
        socks['socket']=[s]

    if client == 1:
        while True:
            # wait for an incoming message
            lin, lout, lex = select(socks['socket'], [], []) 
            serv_print('select got %s read events'%(len(lin)))

            for t in lin:
            # Command /ipsv4
                if t == CMD_IPS:
                    ips_cmd(c)
                    serv_print('Ips List', 'Debug')
                    serv_print('IPS %d\n'%(CODE_IPS), 'Debug')

            # Command /pm
                elif t == CMD_PM:
                    msgp_cmd(t, c)
                    serv_print('PM %d\n'%(CODE_PM), 'Debug')

            # Command /bm
                elif t == CMD_BM:
                    msgb_cmd(t, c)
                    serv_print('BM %d\n'%(CODE_BM), 'Debug')

            # Command /ban
                elif t == CMD_BAN:
                    ban_cmd(t, c)

            # Command /unban
                elif t == CMD_UNBAN:
                    unban_cmd(t, c)
                    
            # Command /?
                elif t == CMD_HELP:
                    display_help(c)
                    serv_print ('Help command!\n', 'Debug')

            # Command /quit
                elif t == CMD_QUIT:
                    quit_cmd(t, c, socks)
                    serv_print ('Drop Connection %s!\n'%(who), 'Debug')

            # Standart message
                else: # someone is speaking
                    data = t
                    who  = name
                    if not data:
                        socks['name'].remove(who)
                        socks['socket'].remove(t)
                        socks['c'].remove(c)
                        msg = '[=Sign-off=] Drop Connection %s!\n'%(who)
                    else:
                        msg = '%s: %s!\n'%(who, data)
                    
                    serv_print (msg)

    if client == 0:
        while True:
          # wait for an incoming message
          lin, lout, lex = select(socks['socket'], [], []) 
          serv_print('select got %s read events'%(len(lin)))

          for t in lin:
            if t == s: # this is an incoming connection
                c, addr = s.accept()
                serv_print('Hello\n')
                socks['c']=c
                msg = 'Hello'
                c.send(msg.encode(ENCODING))
                #socks['name']=t.getpeername()[0]
                if t == 'START':
                    serv_print('START %d\n'%(CODE_START), 'Debug')
                    socks['c'].append(c)
                    msg = 'START'
                    c.send(msg.encode(ENCODING))
                    socks['name']=t.getpeername()[0]

                elif t == 'HELLO':
                    serv_print('HELLO %d\n'%(CODE_HELLO), 'Debug')
                    name_cmd(name,c)
                    serv_print('HELLO %d\n'%(name))
                    msg = 'HELLO I am %d\n'%(name)
                    c.send(msg.encode(ENCODING))
            
            # Command /ipsv4
                if t == CMD_IPS:
                    ips_cmd(c)
                    serv_print('Ips List', 'Debug')
                    serv_print('IPS %d\n'%(CODE_IPS), 'Debug')

            # Command /pm
                elif t == CMD_PM:
                    msgp_cmd(t, c)
                    serv_print('PM %d\n'%(CODE_PM), 'Debug')

            # Command /bm
                elif t == CMD_BM:
                    msgb_cmd(t, c)
                    serv_print('BM %d\n'%(CODE_BM), 'Debug')

            # Command /ban
                elif t == CMD_BAN:
                    ban_cmd(t, c)

            # Command /unban
                elif t == CMD_UNBAN:
                    unban_cmd(t, c)
                    
            # Command /?
                elif t == CMD_HELP:
                    display_help(c)
                    serv_print ('Help command!\n', 'Debug')

            # Command /quit
                elif t == CMD_QUIT:
                    quit_cmd(t, c, socks)
                    serv_print ('Drop Connection %s!\n'%(who), 'Debug')

            # Standart message
                else: # someone is speaking
                    data = t
                    who  = name

                    if not data:
                        socks['name'].remove(who)
                        socks['socket'].remove(t)
                        socks['c'].remove(c)
                        msg = '[=Sign-off=] Drop Connection %s!\n'%(who)
                    else:
                        msg = '%s: %s!\n'%(who, data)
                    
                    serv_print (msg)