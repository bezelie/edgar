#!/bin/bash
# entityデータの変換
# csvをtsvに変換
sudo sed -E "s/,/    /g" chatEntity.csv > chatEntity.tsv
# tsvファイルをjuliusのdic形式に変換
sudo iconv -f utf8 -t eucjp chatEntity.tsv | /home/pi/dictation-kit-v4.4/src/julius-4.4.2/gramtools/yomi2voca/yomi2voca.pl > chatEntity.dic
exit 0
