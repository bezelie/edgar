#!/usr/bin/python
# -*- coding: utf-8 -*-
# Bezelie Sample Code for Raspberry Pi : １秒おきに文字を画面に表示するだけのサンプルです

# ライブラリの読み込み
from time import sleep                 # ウェイト処理

# メインループ
def main():
  try:
    print "開始します"
    while True:
      print "実行してます"
      sleep (1)                        # １秒待つ
  except KeyboardInterrupt:            # コントロール＋Cが押された場合の処理
    print "終了しました"

if __name__ == "__main__":
    main()
