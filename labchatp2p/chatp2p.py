# !/usr/bin/env python3
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

ips     = []
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
                print("This IP {} is ban!\n".format(ip))
                return

    print(ip)
    
    s = socket()
    s.connect((ip, DEFAULT_PORT))
    serv_print('Connection on: {}'.format(ip), 'Debug')
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
        serv_printing += '[={}=] '.format(subj)
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
    msg = '[=Sign-off=] {} JustLeft \n'.format(who)
    c.send(msg.encode(ENCODING))

    socks['name'].remove(who)
    socks['socket'].remove(t)
    socks['c'].remove(c)

    serv_print('Has left: {}'.format(t[2:]), 'Debug')

def ips_cmd(c):
    """Command /w
    Attributes:
        c : permite to send message
    """
    for i in range (socks['name']):
        msg = format(ips.append(socks[i]))
    c.send(msg.encode(ENCODING))

def name_cmd(t, c):
    """Command /name
    Attributes:
        t : incoming information
        c : permite to send message
    """
    if len(t[1:]) < 2:
        msg = '[=Name=] Your nickname is {}\n'.format(t.getpeername()[0])
        c.send(msg.encode(ENCODING))
        serv_print('Missing a Nickname or check his name', 'Debug')
        return

    oldNick = t.getpeername()[0]
    t.getpeername()[0] = format(t[2:])
    msg = '[=Name=] {} changed nicname to {}\n'.format(oldNick, t.getpeername()[0])
   
    serv_print('NickName Detected: {}'.format(t[2:]), 'Debug')

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
        serv_print('Username Detected: {}'.format(t[2:]), 'Debug')

    for i in range (socks['name']):
        if format(t[2:]) in socks['name']:
            c = socks[format(t[2:])]['c']
    
    data = t.recv(BUFF_SZ)
    who  = t.getpeername()[0]
    msg  = '<* Private Message From : {} *> {}\n'.format(who, data.strip())
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
                    msg  = '<* {} *> {}\n'.format(who, data.strip())
                    c.send(msg.encode(ENCODING))
        else:
            c    = socks[i]['c']
            data = t.recv(BUFF_SZ)
            who  = t.getpeername()[0]
            msg  = '<* BroadCast Message From : {} *> {}\n'.format(who, data.strip())
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
        serv_print('Username Detected: {}'.format(t[2:]), 'Debug')

    for i in range (socks['name']):
        if socks[i] == format(t[2:]):
            ipsban.append(format(t[2:]))
            socks['name'].remove(format(t[2:]))
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
        serv_print('Username Detected: {}'.format(t[2:]), 'Debug')

    for i in range (ipsban):
        if ipsban[i] == format(t[2:]):
            ipsban.remove(format(t[2:]))


"""
    MAIN
"""
if __name__ == '__main__':
    
    name = raw_input("What is your name?")

    if sys.argv[1:]:
        ip = str(sys.argv[1:])
        s = create_sock_ip(ip)
        s.listen(PENDING_SLOTS)
        serv_print('Listening on port {}'.format(DEFAULT_PORT),'Waiting')
        # Socket list
        socks['socket']=[s]
    else:
        # creat socket
        s = create_sock()
        s.listen(PENDING_SLOTS)
        serv_print('Listening on port {}'.format(DEFAULT_PORT),'Waiting')
        # Socket list
        socks['socket']=[s]

    while True:
      # wait for an incoming message
      lin, lout, lex = select(socks['socket'], [], []) 
      serv_print('select got {} read events'.format(len(lin)))
      read_config_file()

      for t in lin:
        socks['name'].append(t.getpeername()[0])

        if t == s: # this is an incoming connection
            c, addr = s.accept()
            if t.startswith('START'):
                serv_print('START {}\n'.format(CODE_START), 'Debug')
                socks['c'].append(c)
                msg = 'START'
                c.send(msg.encode(ENCODING))

            elif t.startswith('HELLO'):
                serv_print('HELLO {}\n'.format(CODE_HELLO), 'Debug')
                name_cmd(name,c)
                serv_print('HELLO {}\n'.format(addr[0]))
                msg = 'HELLO I am {}\n'.format(addr[0])
                c.send(msg.encode(ENCODING))
           
        # Command /ips
            if t.startswith(CMD_IPS):
                ips_cmd(c)
                serv_print('Ips List', 'Debug')
                serv_print('IPS {}\n'.format(CODE_IPS), 'Debug')

        # Command /pm
            elif t.startswith(CMD_PM):
                msgp_cmd(t, c)
                serv_print('PM {}\n'.format(CODE_PM), 'Debug')

        # Command /bm
            elif t.startswith(CMD_BM):
                msgb_cmd(t, c)
                serv_print('BM {}\n'.format(CODE_BM), 'Debug')

        # Command /ban
            elif t.startswith(CMD_BAN):
                ban_cmd(t, c)

        # Command /unban
            elif t.startswith(CMD_UNBAN):
                unban_cmd(t, c)
                
        # Command /?
            elif t.startswith(CMD_HELP):
                display_help(c)
                serv_print ('Help command {}!\n', 'Debug')

        # Command /quit
            elif t.startswith(CMD_QUIT):
                quit_cmd(t, c, socks)
                serv_print ('Drop Connection {}!\n'.format(who), 'Debug')

        # Standart message
            else: # someone is speaking
                data = t.recv(BUFF_SZ)
                who  = t.getpeername()[0]

                if not data:
                    socks['name'].remove(who)
                    socks['socket'].remove(t)
                    socks['c'].remove(c)
                    msg = '[=Sign-off=] Drop Connection {}!\n'.format(who)
                else:
                    msg = '{}: {}\n'.format(who, data.strip())
                
                serv_print (msg)
                for c in socks['c']:
                    c.send(msg)
