#!/usr/bin/python

# Echo server program
import socket,os,sys,xmpp,time

os.setuid(108)

s=socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
try:
    os.remove("/etc/zabbix/jabber_server/.socket")
except OSError:
    pass
s.bind("/etc/zabbix/jabber_server/.socket")


jidparams={}
jidparams['domain']="test.domain"  #Zabbix Jabber user account domain eg @jabberdomain.org
jidparams['username']="zabbix" #Zabbix Jabber user account name
jidparams['surname']="Zabbix"
jidparams['password']="password"  #Zabbix Jabber user account password
jidparams['resource']="ZabbixServer"

#Do not modify below this line
#########################################

# if len(sys.argv) < 2:
#     print "Syntax: jabber_recipient message"
#     sys.exit(0)
#
# jabber_recipient=sys.argv[1]
# message=' '.join(sys.argv[2:])
#print jabber_recipient+" "+message #debug
jid=xmpp.protocol.JID(jidparams['username'] + "@" + jidparams['domain'])
cl=xmpp.Client(jid.getDomain(),debug=[])

con=cl.connect(server=(jidparams['domain'], 5223),secure=1,use_srv=False)
if not con:
    #print 'could not connect to Jabber server!' #debug
    sys.exit()
#print 'connected with server',con #debug
auth=cl.auth(jidparams['username'],jidparams['password'], resource=jidparams['resource'], sasl=0)
if not auth:
    #print 'could not authenticate!' #debug
    sys.exit()
#print 'authenticated using',auth #debug

while 1:
    s.listen(1)
    conn, addr = s.accept()
    while 1:
        data = conn.recv(1024)
        if not data: break
        #print(data)
        splitted=data.split()
        recipient=splitted[0]
        message=' '.join(splitted[1:])
        cl.send(xmpp.Presence(to="%s/%s" % (recipient, jidparams['surname'])))

        msg = xmpp.protocol.Message(body=message)
        msg.setTo(recipient)
        msg.setType('groupchat')

        cl.send(msg)
        #conn.send(data)
    conn.close()
    time.sleep(1)

cl.disconnect()

