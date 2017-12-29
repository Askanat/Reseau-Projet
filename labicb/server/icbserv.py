from socket import socket, SOL_SOCKET, SO_REUSEADDR

# création du socket
s = socket()
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind(('0.0.0.0',7326))

# écoute
s.listen(3)
print "Listening on port 7326"

# liste des sockets ouvert
socks=[s]

while True:
  # wait for an incoming message
  lin, lout, lex=select(socks, [], []) 
  print "select got %d read events" % (len(lin))
  for t in lin:
    if t==s: # this is an incoming connection
      (sc, addr)=s.accept()
      msg="Hello %s\n" % (addr[0],)
      print msg
      socks.append(c)
      buf = msg.encode('utf-8')
      c.send(buf)

    if t.startswith('/w'):
        if len(t[1:]) > 2:
            print('User Detected: {}'.format(t[2:]))
        else:
            print('General Localtion')

	if t.startswith('/m'):
		if len(t[1:]) > 2:
            print('Username Detected: {}'.format(t[2:]))
        else:
        	print('Missing a Recipient')
        	msg="[=Error=] Missing a Recipient"
			buf = msg.encode('utf-8')
      		c.send(buf)  

	if t.startswith('/g'):
		if len(t[1:]) > 2:
            print('Group name Detected: {}'.format(t[2:]))
        else:
        	print('Missing a Group Name')
        	msg="[=Error=] Missing a Group Name"
			buf = msg.encode('utf-8')
      		c.send(buf) 

	if t.startswith('/name'):
		if len(t[1:]) > 2:
            print('NickName Detected: {}'.format(t[2:]))
        else:
        	print('Missing a Nickname')
        	msg="[=Error=] Missing a New Nickname"
			buf = msg.encode('utf-8')
      		c.send(buf)

	if t.startswith('/topic'):
		if len(t[1:]) > 2:
            print('Topic Detected: {}'.format(t[2:]))
        else:
        	print('Missing a Topic')
        	msg="[=Error=] Missing a Topic"
			buf = msg.encode('utf-8')
      		c.send(buf)

	if t.startswith('/pass'):
		msg="[=Notify=] Server has passed moderation to %s \n" % (addr[0],)
		buf = msg.encode('utf-8')
      	c.send(buf)

	if t.startswith('/?'):
		msg="[=Help=] Server supports following commands:\n" + 
			"[=Help=] beep boot g m name nobeep pass topic w \n"
		buf = msg.encode('utf-8')
      	c.send(buf)

    if t.startswith('/q'):
    	msg="[=Sign-off=] %s JustLeft \n" % (addr[0],)
		buf = msg.encode('utf-8')
      	c.send(buf)
      	socks.remove(t)

    else: # someone is speaking
      who=t.getpeername()[0]
      data=t.recv(1024)
      if data:
        msg="%s: %s\n" % (who, data.strip())
      else: # connection closed
        socks.remove(t)
        msg="[=Sign-off=] Drop Connection %s!\n" % (who,)
      print msg
      for c in socks[1:]:
        c.send(msg)