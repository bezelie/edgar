#!/bin/bash
ps aux | grep python | grep -v grep | awk '{ print "kill -9", $2 }' | bash
ps aux | grep julius | grep -v grep | awk '{ print "kill -9", $2 }' | bash
/opt/bezelie/bin/boot_julius.sh
/opt/bezelie/bin/boot_python.sh
exit 0
