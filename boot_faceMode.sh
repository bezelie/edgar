#!/bin/bash
# pythonスクリプト起動スクリプト
sleep 1 # 自動起動に失敗する場合、この待ち時間を長くしてみてください
cd /home/pi/bezelie/edgar
/usr/bin/python /home/pi/bezelie/edgar/demo_face1.py
exit 0
