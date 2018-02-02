#!/usr/bin/python
# -*- coding: utf-8 -*-
# Bezelie Sample Code for Raspberry Pi : 発話するサンプル
# ミニジャックにスピーカーなどを接続してから試してください。

# ライブラリの読み込み
import subprocess                     # shellの実行をするためのライブラリ
from time import sleep                # ウェイト処理
import bezelie                        # べゼリー専用モジュール

# Variables
openJTalkFile = "exec_openJTalk.sh"   # 発話シェルスクリプトのファイル名

# Main Loop
def main():
  try:
    while (True):
      subprocess.call("sh "+openJTalkFile+" "+"こんにちわ", shell=True)
      sleep(0.5)
  except KeyboardInterrupt:
    print ' Interrupted by Keyboard'

if __name__ == "__main__":
    main()
