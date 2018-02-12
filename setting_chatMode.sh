#!/bin/bash
# 音声認識モードで再起動
SCRIPT_DIR=`dirname $0`
cd $SCRIPT_DIR
# wlan0をアクセスポイントにする
sudo cp config/interfaces_changed /etc/network/interfaces
# IPアドレス固定 wlan0に固定IPアドレスを割り振る
sudo cp config/dhcpcd_changed.conf /etc/dhcpcd.conf
# サービスを再起動
sudo service dhcpcd restart
# Hostapdでアクセスポイント化
sudo cp config/hostapd_changed.conf /etc/hostapd/hostapd.conf
# DEAMON_CONF の指定。
sudo cp config/hostapd_changed /etc/default/hostapd
# DHCPサーバ化
sudo cp config/dhcpd_changed.conf /etc/dhcp/dhcpd.conf
sudo cp config/isc-dhcp-server_changed /etc/default/isc-dhcp-server
# systemd自動起動を設定する
sudo cp boot_chatMode.sh /opt/bezelie/bin/boot_python.sh
sudo cp boot_julius.sh /opt/bezelie/bin/
sudo cp boot_node.sh /opt/bezelie/bin/
sudo cp boot_dhcp.sh /opt/bezelie/bin/
sudo cp autoStart_python.service /etc/systemd/system/
sudo cp autoStart_julius.service /etc/systemd/system/
sudo cp autoStart_node.service /etc/systemd/system/
sudo cp autoStart_dhcp.service /etc/systemd/system/
sudo systemctl enable autoStart_python.service
sudo systemctl enable autoStart_julius.service
sudo systemctl enable autoStart_node.service
sudo systemctl enable autoStart_dhcp.service
sudo systemctl daemon-reload
sudo reboot
