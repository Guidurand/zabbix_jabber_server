#!/usr/bin/python

import socket,os,sys,xmpp,time
import ConfigParser
from pwd import getpwnam
from config_parser import ReadParameters

parameters = ReadParameters("server.conf")

#switch uid process
uid=getpwnam(parameters['process_user']).pw_uid
os.setuid(uid)

s=socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
try:
    os.remove(parameters['socket_path'])
except OSError:
    pass
s.bind(parameters['socket_path'])

jid=xmpp.protocol.JID(parameters['username'] + "@" + parameters["domain"])
cl=xmpp.Client(jid.getDomain(),debug=[])

con=cl.connect(server=(parameters["domain"], 5223),secure=1,use_srv=False)
if not con:
    print 'could not connect to Jabber server!' #debug
    sys.exit()
#print 'connected with server',con #debug
auth=cl.auth(parameters['username'],parameters['password'], resource=parameters['resource'], sasl=0)
if not auth:
    print 'could not authenticate!' #debug
    sys.exit()
#print 'authenticated using',auth #debug

# # while 1:
s.listen(1)
# conn, addr = s.accept()

while 1:
    # s.listen(1)
    print "titi"
    conn, addr = s.accept()
    data = conn.recv(1024)
    if data:
        print("totot")
        splitted=data.split()
        recipient=splitted[0]
        message=' '.join(splitted[1:])
        presence=cl.send(xmpp.Presence(to="%s/%s" % (recipient, parameters['surname'])))
        if not presence:
            print 'fail presence',presence
        print 'presence',presence
        msg = xmpp.protocol.Message(body=message)
        msg.setTo(recipient)
        msg.setType('groupchat')

        send=cl.send(msg)
        # if not send:
        #     print 'send ',send
        # print 'send ',send
        #conn.send(data)
    time.sleep(1)

conn.close()
cl.disconnect()
