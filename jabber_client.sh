#!/bin/bash

echo $@ | socat 'unix-connect:/tmp/.socket' stdio

exit 0

