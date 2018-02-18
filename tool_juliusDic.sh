#!/bin/bash
# chatEntityデータの変換
# csvをtsvに変換
sudo sed -E "s/,/    /g" /home/pi/bezelie/chatEntity.csv > /home/pi/bezelie/chatEntity.tsv
# tsvファイルをjuliusのdic形式に変換
sudo iconv -f utf8 -t eucjp /home/pi/bezelie/chatEntity.tsv | /home/pi/dictation-kit-v4.4/src/julius-4.4.2/gramtools/yomi2voca/yomi2voca.pl > /home/pi/bezelie/chatEntity.dic
exit 0
