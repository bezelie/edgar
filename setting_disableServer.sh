#!/bin/bash
# ラズパイのアクセスポイント化を解除し、wifiに接続する設定にする
# サービス終了
sudo service isc-dhcp-server stop
# DHCPサーバ無効化
sudo cp config/isc-dhcp-server_original /etc/default/isc-dhcp-server
sudo cp config/dhcpd_original.conf /etc/dhcp/dhcpd.conf
# hostapd設定の初期化
sudo cp config/hostapd_original /etc/default/hostapd
sudo cp config/hostapd_original.conf /etc/hostapd/hostapd.conf
# IPアドレス固定化の無効化
sudo cp config/dhcpcd_original.conf /etc/dhcpcd.conf
# wlan0をアクセスポイントにすることの無効化
sudo cp config/interfaces_original /etc/network/interfaces
# systmd自動起動の無効化
sudo systemctl disable autoStart_julius.service
sudo systemctl disable autoStart_python.service
sudo systemctl disable autoStart_node.service
sudo systemctl disable autoStart_dhcp.service
sudo reboot
