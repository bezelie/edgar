#!/usr/bin/python
# -*- coding: utf-8 -*-
# Bezelie Sample Code for Raspberry Pi : べゼリーの基本アクション
# ラズパイにサーボドライバーとサーボを接続してから実行してください。

# ライブラリの読み込み
from time import sleep                # ウェイト処理
import bezelie                        # べゼリー専用モジュール

# 準備
bez = bezelie.Control()               # べゼリー操作インスタンスの生成
bez.moveCenter()                      # サーボをセンタリング
sleep(0.5)

# メインループ
def main():
  try:
    print "開始します"
    while True:
      print "happy"
      bez.moveAct('happy')            # しあわせ
      bez.stop()
      sleep (0.5)
      print "nod"
      bez.moveAct('nod')              # うなづき
      bez.stop()
      sleep (0.5)
      print "why"
      bez.moveAct('why')              # 首かしげ
      bez.stop()
      sleep (0.5)
      print "around"
      bez.moveAct('around')           # 見回し
      bez.stop()
      sleep (0.5)
      print "up"
      bez.moveAct('up')               # 見上げ
      bez.stop()
      sleep (0.5)
      print "wave"
      bez.moveAct('wave')             # くねくね
      bez.stop()
      sleep (0.5)
      print "etc"
      bez.moveAct('etc')              # ETC
      bez.stop()
      sleep (0.5)
  except KeyboardInterrupt:
    print "  終了しました"

if __name__ == "__main__":
    main()
