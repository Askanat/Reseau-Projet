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
	if t=="/w":

	if t=="/m":

	if t=="/g":

	if t=="/name":

	if t=="/topic":

	if t=="/pass":

	if t=="/?":
		msg="[=Help=] Server supports following commands:\n" + 
			"[=Help=] beep boot g m name nobeep pass topic w \n"
		buf = msg.encode('utf-8')
      	c.send(buf)
    if t=="/q":
    	msg="[=Sign-off] %s JustLeft C\n" % (addr[0],)
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
        msg="[=Sign-off] Drop Connection %s!\n" % (who,)
      print msg
      for c in socks[1:]:
        c.send(msg)