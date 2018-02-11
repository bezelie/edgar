#!/bin/bash
# Julius（音声コマンド版）をモジュールモードで起動
ALSADEV="plughw:0,0" /usr/local/bin/julius -w /home/pi/bezelie/edgar/chatEntity.dic -C /home/pi/bezelie/edgar/julius.jconf -module > /dev/null &
echo "Julius's Process ID = "$!
# /dev/nullはlinuxの特殊ファイルで、何も出力したくない時に指定する。
# $! = シェルが最後に実行したバックグラウンドプロセスのID
# juliusが立ち上がる前にアクセスしようとするとエラーになるので数秒待つ
# sleep 3
exit 0
