#!/bin/bash
echo "restart_app.sh start" >> debug.txt
ps aux | grep python | grep -v grep | awk '{ print "kill -9", $2 }' | bash
ps aux | grep julius | grep -v grep | awk '{ print "kill -9", $2 }' | bash
echo "python and julius are killed" >> debug.txt
/opt/bezelie/bin/boot_julius.sh
echo "julius executed on back ground" >> debug.txt
/opt/bezelie/bin/boot_python.sh
echo "demo_chat1.py executed" >> debug.txt
exit 0
