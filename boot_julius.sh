#!/bin/bash
# Juliusをモジュールモードで起動
ALSADEV="plughw:0,0" /usr/local/bin/julius -w /home/pi/bezelie/edgar/chatEntity.dic -C /home/pi/bezelie/edgar/julius.jconf -module &
echo "Julius's Process ID = "$!
# $! = シェルが最後に実行したバックグラウンドプロセスのID
exit 0
