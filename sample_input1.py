#!/usr/bin/python
# -*- coding: utf-8 -*-
# Bezelie Sample Code for Raspberry Pi : スイッチ（＋プルダウン抵抗）入力のサンプル
# マニュアルを見てラズパイにスイッチを接続しておいてください。

# ライブラリの読み込み
from time import sleep                 # sleep(ウェイト処理)ライブラリの読み込み
import RPi.GPIO as GPIO                # GPIO(汎用入出力端子)ライブラリの読み込み

# 初期設定
GPIO.setmode(GPIO.BCM)                 # GPIOをGPIO番号で指定できるように設定
GPIO.setup(24, GPIO.IN)                # GPIOの24ピンを入力モードに設定

# 関数
def main():
  try:
    print "開始します"
    while True:                        # 繰り返し処理
      if GPIO.input(24)==GPIO.HIGH:    # GPIO24に3.3Vの電圧がかかっていたら・・・
        print "スイッチが押されています"
      else:                            # それ以外の場合は・・・
        print "スイッチは押されてません"
      sleep (0.5)                      # 0.5秒待つ
  except KeyboardInterrupt:            # コントロール＋Cが押された場合の処理
    print "終了しました"
    GPIO.cleanup()                     # ポートをクリア

# 直接実行された場合の処理
if __name__ == "__main__":
    main()
