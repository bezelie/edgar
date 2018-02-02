#!/usr/bin/python
# -*- coding: utf-8 -*-
# Bezelie Sample Code for Raspberry Pi : 出力のサンプル
# GPIO 27ピンとGNDにLEDなどを接続してから実行してください。

# ライブラリの読み込み
from time import sleep                 # sleep(ウェイト処理)ライブラリの読み込み
import RPi.GPIO as GPIO                # GPIO(汎用入出力端子)ライブラリの読み込み

# 初期設定
GPIO.setmode(GPIO.BCM)                 # GPIOをGPIO番号で指定できるように設定
GPIO.setup(27, GPIO.OUT)               # GPIOの27ピンを出力モードに設定

# 関数
def main():
  try:
    print "GPIO 27ピンの出力を交互にオンオフします"
    while True:                        # 繰り返し処理
      print "オン"
      GPIO.output(27, True)
      sleep (1)
      print "オフ"
      GPIO.output(27, False)
      sleep (1)
  except KeyboardInterrupt:            # コントロール＋Cが押された場合の処理
    print "終了しました"
    GPIO.cleanup()                     # ポートをクリア

# 直接実行された場合の処理
if __name__ == "__main__":
    main()
