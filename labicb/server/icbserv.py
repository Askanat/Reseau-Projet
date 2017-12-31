# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import select
from select import select

import socket
from socket import socket
from socket import SOL_SOCKET
from socket import SO_REUSEADDR


# chanel[nom] : [[modo] [user] [topic]]
chanel = {
    'group': 'agora',
    'user' : '',
    'modo' : '(None)',
    'topic': '(None)'
}

socks = {
    'name'  : '',
    'socket': '',
    'c'     : ''
}

BUFF_SZ       = 1024
CONFIG_FILE   = None
DEFAULT_PORT  = 7326
ENCODING      = 'utf-8'
IP_NO_FILTER  = '0.0.0.0'
M_LOGIN       = 'a'
PENDING_SLOTS = 1
TAB_SZ        = 5

CMD_GROUP = '/g'
CMD_HELP  = '/?'
CMD_LOGIN = 'login'
CMD_MSG   = '/m'
CMD_NAME  = '/name'
CMD_PASS  = '/pass'
CMD_QUIT  = '/q'
CMD_TOPIC = '/topic'
CMD_WHOIS = '/w'


def create_sock():
    """Socket creator
    Attributes:
        None
    """
    s = socket()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind((IP_NO_FILTER, DEFAULT_PORT))
    return s

def display_help(c):
    """Command /?
    Attributes:
        c : permite to send message
    """
    msg='[=Help=] Server supports following commands:\n'
    c.send(msg.encode(ENCODING))
    msg='[=Help=] beep boot g m name nobeep pass topic w \n'
    c.send(msg.encode(ENCODING))

def group_cmd(t, c):
    """Command /g
    Attributes:
        t : incoming information
        c : permite to send message
    """
    if len(t[1:]) < 2:
        msg = '[=Error=] Missing a Group Name'
        c.send(msg.encode(ENCODING))
        serv_print('Missing a Group Name', 'Debug')
        return
    else:
        serv_print('Group name Detected: {}'.format(t[2:]), 'Debug')

    for i in range (chanel['group']):
        if t.getpeername()[0] in chanel[i]['user']:
            chanel[i]['user'].remove(t.getpeername()[0])
            msg = '[=Depart=] {} just left\n'.format(t.getpeername()[0])
            c.send(msg.encode(ENCODING))

    chanel['group'].append(format(t[2:]))
    chanel[format(t[2:])]['user'].append(t.getpeername()[0])

    msg = '[=Status=] You are now in chanel {} as moderator\n'.format(format(t[2:]))
    c.send(msg.encode(ENCODING))

def msg_cmd(t, c):
    """Command /m
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
    else:
        serv_print('Group name Detected: {}'.format(t[2:]), 'Debug')

    oldNick = t.getpeername()[0]
    t.getpeername()[0] = format(t[2:])
    msg = '[=Name=] {} changed nicname to {}\n'.format(oldNick, t.getpeername()[0])
    for i in range (chanel['group']):
        if oldNick in chanel[i]['user']:
            chanel[i]['user'].remove(oldNick)
            chanel[i]['user'].append(format(t[2:]))

    serv_print('NickName Detected: {}'.format(t[2:]), 'Debug')

def pass_cmd(t, c):
    """Command /pass
    Attributes:
        t : incoming information
        c : permite to send message
    """
    who=t.getpeername()[0]
    for i in range (chanel['group']):
        if who in chanel[i]['user']:
            if chanel[i]['modo'] == '':
                chanel[i]['modo'] = who
    msg='[=Notify=] Server has passed moderation to {} \n'.format(who)
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

    for i in range (chanel['group']):
        if who in chanel[i]['user']:
            chanel[i]['user'].remove(who)
            if group[i]['user'] == '':
                groupName = group[i]
                group['group']['modo'].remove(who)
                group['group'].remove(groupName)
    serv_print('Has left: {}'.format(t[2:]), 'Debug')

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

def topic_cmd(t, c):
    """Command /topic
    Attributes:
        t : incoming information
        c : permite to send message
    """
    if len(t[1:]) < 2:
        msg='[=Error=] Missing a Topic'
        c.send(msg.encode(ENCODING))

        serv_print('Missing a Topic', 'Debug')
        return
    else:
        serv_print('Topic Detected: {}'.format(t[2:]), 'Debug')

    who=t.getpeername()[0]
    for i in range (chanel['group']):
        if who in chanel[i]['user']:
            chanel[i]['topic'] = format(t[2:])

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

def login(self, command = 'login'):
    """Allow login
    Attributes:
        self    : tell him self
        command : take login information
    """
    self.send([self.M_LOGIN, self.logid,
        self.nickname, self.group, command, ''])

def read_config_file(CONFIG_FILE = None):
    """Read information in config file
    Attributes:
        CONFIG_FILE : constant locoation of file
    """
    if CONFIG_FILE == None:
        CONFIG_FILE = CONFIG_FILE
    try:
        f = open(CONFIG_FILE, "r")
    except:
        msg=("warning: can't read config file, using defaults.\n")
        c.send(msg.encode(ENCODING))
        return

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
        chanel['group']['user'].append(t.getpeername()[0])
        socks['name'].append(t.getpeername()[0])

        if t == s: # this is an incoming connection
            c, addr = s.accept()
            serv_print('Hello {}\n'.format(addr[0]))
            socks['c'].append(c)
            c.send(msg.encode(ENCODING))

        # Command login
            if t.startswitht(CMD_LOGIN):
                self.login(CMD_LOGIN)
                serv_print('Login', 'Debug')

        # Command /whois
            elif t.startswith(CMD_WHOIS):
                whois(c)
                serv_print('General Location', 'Debug')

        # Command /message
            elif t.startswith(CMD_MSG):
                msg_cmd(t, c)

        # Command /group
            elif t.startswith(CMD_GROUP):
                group_cmd(t, c)

        # Command /name
            elif t.startswith(CMD_NAME):
                name_cmd(t, c)

        # Command /topic
            elif t.startswith(CMD_TOPIC):
                topic_cmd(t, c)
                
        # Command /pass
            elif t.startswith(CMD_PASS):
                pass_cmd(t, c)
                serv_print ('Server has passed moderation to {}!\n'.format(who), 'Debug')

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