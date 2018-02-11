#!/usr/bin/python
# -*- coding: utf-8 -*-
# Bezelie Sample Code for Raspberry Pi : サーボを個別に動かす
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
      print "Head 上回転"
      bez.moveHead(10)                # 頭の上下
      sleep (0.5)
      print "Head 下回転"
      bez.moveHead(-10)               # 頭の上下
      sleep (0.5)
      print "Head 中央"
      bez.moveHead(0)                 # 頭の上下
      sleep (1)
      print "Back 右回転"
      bez.moveBack(20)                # 頭の左右
      sleep (0.5)
      print "Back 左回転"
      bez.moveBack(-20)               # 頭の左右
      sleep (0.5)
      print "Back 中央"
      bez.moveBack(0)                 # 頭の左右
      sleep (1)
      print "Stage 右回転"
      bez.moveStage(30)               # 体の左右
      sleep (0.5)
      print "Stage 左回転"
      bez.moveStage(-30)              # 体の左右
      sleep (0.5)
      print "Stage 中央"
      bez.moveStage(0)                # 体の左右
      sleep (1)
  except KeyboardInterrupt:
    print "  終了しました"

if __name__ == "__main__":
    main()
