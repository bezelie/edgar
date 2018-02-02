#!/bin/bash
# Juliusをモジュールモードで起動
ALSADEV="plughw:0,0" /usr/local/bin/julius -w /home/pi/bezelie/dev_edgar/chatEntity.dic -C /home/pi/bezelie/dev_edgar/julius.jconf -module &
echo "Julius's Process ID = "$!
# cd /home/pi/bezelie/dev_edgar
# /usr/bin/python /home/pi/bezelie/dev_edgar/demo_chat1.py
# /dev/nullはlinuxの特殊ファイルで、何も出力したくない時に指定する。
# $! = シェルが最後に実行したバックグラウンドプロセスのID
# juliusが立ち上がる前にアクセスしようとするとエラーになるので数秒待つ
exit 0
