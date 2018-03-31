#!/usr/bin/python
# -*- coding: utf-8 -*-
# Bezelie Sample Code for Raspberry Pi : 発話するサンプル
# スピーカーなどを接続してから試してください。

# ライブラリの読み込み
from time import sleep                # ウェイト処理
import subprocess                     # 外部プロセスを実行するモジュール

# 変数
ttsFile = "/home/pi/bezelie/edgar/exec_openJTalk.sh" # 発話シェルスクリプトのファイル名

# メインループ
def main():
  try:
    while (True):
      subprocess.call("sh "+ttsFile+" "+"こんにちわ", shell=True)
#      subprocess.call('flite -voice "slt" -t "alexa"', shell=True) # English
       # Other English Voices :kal awb_time kal16 awb rms slt
      sleep(0.5)
  except KeyboardInterrupt:
    print ' 終了しました'

if __name__ == "__main__":
    main()
