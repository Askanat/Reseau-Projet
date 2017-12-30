from socket import socket, SOL_SOCKET, SO_REUSEADDR
from select import select

# création du groupe par défaut
# dict[nom] : [[modo] [user] [topic]]
dict = {'group': 'agora','user':'','modo':'(None)','topic': '(None)'}

# création du socket
s = socket()
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind(('0.0.0.0',7326))

# écoute
s.listen(3)
print ("Listening on port 7326")

# liste des sockets ouvert
socks=[s]

while True:
  # wait for an incoming message
  lin, lout, lex=select(socks, [], []) 
  print ("select got %d read events" % (len(lin)))
  for t in lin:
    dict['group']['user'].append(t.getpeername()[0])
    if t==s: # this is an incoming connection
      (sc, addr)=s.accept()
      msg="Hello %s\n" % (addr[0],)
      print (msg)
      socks.append(c)
      buf = msg.encode('utf-8')
      c.send(buf)

    # Command /whois
    if t.startswith('/w'):
        for i in range (dict['group']):
            msg="Group : %s     Modo: %s    Topic: %s\n" % (dict[group], 
                dict['group']['modo'], dict['group']['topic'])
            buf = msg.encode('utf-8')
            c.send(buf)
            msg="%s\n" % (dict[i]['user'])
            buf = msg.encode('utf-8')
            c.send(buf)
        # Debug
        print('[=Debug=] General Localtion')

    # Command /message
    if t.startswith('/m'):
        if len(t[1:]) > 2:
            who=t.getpeername()[0]
            data=t.recv(1024)
            msg="<* %s *> %s\n" % (who, data.strip())
            buf = msg.encode('utf-8')
            c.send(buf)
            # Debug
            print('[=Debug=] Username Detected: {}'.format(t[2:]))
        else:
            msg="[=Error=] Missing a Recipient"
            buf = msg.encode('utf-8')
            c.send(buf)
            # Debug
            print('[=Debug=] Missing a Recipient')  

# Command /group
    if t.startswith('/g'):
        if len(t[1:]) > 2:
            for i in range (dict['group']):
                    if t.getpeername()[0] in dict[i][[user]]:
                        dict[i]['user'].remove(t.getpeername()[0])
                        msg="[=Depart=] %s just left\n" % (t.getpeername()[0])
                        buf = msg.encode('utf-8')
                        c.send(buf)

            dict['group'].append(format(t[2:]))
            dict[format(t[2:])]['user'].append(t.getpeername()[0])

            msg="[=Status=] You are now in dict %s as moderator\n" % (format(t[2:]))
            buf = msg.encode('utf-8')
            c.send(buf)

            # Debug
            print('[=Debug=] Group name Detected: {}'.format(t[2:]))
        else:
            msg="[=Error=] Missing a Group Name"
            buf = msg.encode('utf-8')
            c.send(buf)
            # Debug
            print('[=Debug=] Missing a Group Name') 

# Command /name
    if t.startswith('/name'):
        if len(t[1:]) > 2:
            oldNick = t.getpeername()[0]
            t.getpeername()[0] = format(t[2:])
            msg="[=Name=] %s changed nicname to %s\n" % (oldNick, t.getpeername()[0])
            for i in range (dict['group']):
                if oldNick in dict[i]['user']:
                    dict[i]['user'].remove(oldNick)
                    dict[i]['user'].append(format(t[2:]))
            # Debug
            print('[=Debug=] NickName Detected: {}'.format(t[2:]))
        else:
            msg="[=Name=] Your nickname is %s\n" % (t.getpeername()[0])
            buf = msg.encode('utf-8')
            c.send(buf)
            # Debug
            print('[=Debug=] Missing a Nickname or check his name')

# Command /topic
    if t.startswith('/topic'):
        if len(t[1:]) > 2:
            who=t.getpeername()[0]
            for i in range (dict['group']):
                if who in dict[i]['user']:
                    dict[i]['topic'] = format(t[2:])
            # Debug
            print('[=Debug=] Topic Detected: {}'.format(t[2:]))
        else:
            msg="[=Error=] Missing a Topic"
            buf = msg.encode('utf-8')
            c.send(buf)
            # Debug
            print('[=Debug=] Missing a Topic')

# Command /pass
    if t.startswith('/pass'):
        who=t.getpeername()[0]
        for i in range (dict['group']):
            if who in dict[i]['user']:
                if dict[i]['modo'] == "":
                    dict[i]['modo'] = who
        msg="[=Notify=] Server has passed moderation to %s \n" % (who)
        buf = msg.encode('utf-8')
        c.send(buf)
        # Debug
        print ("[=Debug=] Server has passed moderation to %s!\n" % (who))

# Command /?
    if t.startswith('/?'):
        msg="[=Help=] Server supports following commands:\n"
        buf = msg.encode('utf-8')
        c.send(buf)
        msg="[=Help=] beep boot g m name nobeep pass topic w \n"
        buf = msg.encode('utf-8')
        c.send(buf)
        # Debug
        print ("[=Debug=] Help command %s!\n")

# Command /quit
    if t.startswith('/q'): # connection closed
        who=t.getpeername()[0]
        msg="[=Sign-off=] %s JustLeft \n" % (who)
        buf = msg.encode('utf-8')
        c.send(buf)
        socks.remove(t)
        for i in range (dict['group']):
            if who in dict[i]['user']:
                dict[i]['user'].remove(who)
        # Debug
        print ("[=Debug=] Drop Connection %s!\n" % (who))

# Standart message
    else: # someone is speaking
      who=t.getpeername()[0]
      data=t.recv(1024)
      if data:
        msg="%s: %s\n" % (who, data.strip())
      else: # connection closed
        socks.remove(t)
        msg="[=Sign-off=] Drop Connection %s!\n" % (who,)
      print (msg)
      for c in socks[1:]:
        c.send(msg)