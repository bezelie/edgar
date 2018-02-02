#!/bin/bash
# node server
/usr/local/nodejs/bin/node /home/pi/bezelie/dev_edgar/server_chat.js &
# echo "starting startup applications"
# DHCPサービスの起動
# sudo service isc-dhcp-server start
exit 0
