#!/usr/bin/python
# -*- coding: utf-8 -*-
# Bezelie Sample Code for Raspberry Pi : ランダムでサーボを動かす
# ラズパイにサーボドライバーとサーボを接続してから実行してください。

# ライブラリの読み込み
from time import sleep                # ウェイト処理
import bezelie                        # べゼリー専用モジュール

# Setting
bez = bezelie.Control()               # べゼリー操作インスタンスの生成
bez.moveCenter()                      # サーボをセンタリング
sleep(0.5)

# Main Loop
def main():
  try:
    print "開始します"
    while True:
      bez.moveRnd() 
      bez.stop()
      sleep (0.5)
  except KeyboardInterrupt:
    print "  終了しました"

if __name__ == "__main__":
    main()
