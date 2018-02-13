#!/bin/bash
# Julius（自然言語認識版）をモジュールモードで起動
ALSADEV="plughw:0,0" /usr/local/bin/julius -C /home/pi/bezelie/edgar/juliusNL.jconf -module > /dev/null &
echo "Julius's Process ID = "$!
# /dev/nullはlinuxの特殊ファイルで、何も出力したくない時に指定する。
# $! = シェルが最後に実行したバックグラウンドプロセスのID
exit 0
