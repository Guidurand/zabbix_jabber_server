#!/bin/bash

echo $@ | socat 'unix-connect:/etc/zabbix/jabber_server/.socket' stdio

exit 0

