# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import select
from select import select

import socket
from socket import socket
from socket import SOL_SOCKET
from socket import SO_REUSEADDR

#IPS[name] : [[]]

socks = {
    'name'  : '',
    'socket': '',
    'c'     : ''
}

BUFF_SZ       = 1024
CONFIG_FILE   = None
DEFAULT_PORT  = 1664
ENCODING      = 'utf-8'
IP_NO_FILTER  = '0.0.0.0'

CMD_BAN 	= '/ban'
CMD_UNBAN 	= '/unban'
CMD_QUIT	= '/quit'
CMD_PM		= '/pm'
CMD_BM		= '/bm'
CMD_LIST	= '/ips'

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

def whois(c):
    """Command /w
    Attributes:
        c : permite to send message
    """
    msg = 'Group : {}\tModo: {}\tTopic: {}\n'
    msg = msg.format(
            chanel['group'], 
            chanel['group']['modo'], 
            chanel['group']['topic']
        )
    msg.expandtabs(TAB_SZ)
    c.send(msg.encode(ENCODING))

    for i in range (chanel['group']):
        msg = '{}\n'.format(chanel[i]['user'])
        c.send(msg.encode(ENCODING))

    msg = 'Total : {} users in {} groups\n' 
    msg = msg.format(
            len(chanel['user']),
            len(chanel['group'])
        )
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

def msg_cmd(t, c):
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
    msg  = '<* {} *> {}\n'.format(who, data.strip())
    c.send(msg.encode(ENCODING))



if __name__ == '__main__':
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
            serv_print('Hello {}\n'.format(addr[0]))
            socks['c'].append(c)
            c.send(msg.encode(ENCODING))

        # Command /whois
            elif t.startswith(CMD_WHOIS):
                whois(c)
                serv_print('General Location', 'Debug')

        # Command /message
            elif t.startswith(CMD_PM):
                msg_cmd(t, c)

        # Command /name
            elif t.startswith(CMD_NAME):
                name_cmd(t, c)
                
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