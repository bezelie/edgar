#!/usr/bin/python
# -*- coding: utf-8 -*-
# Bezelie Sample Code for Raspberry Pi : 出力のサンプル
# GPIO 16,20,21ピンとGNDにLEDを接続してから実行してください。

# ライブラリの読み込み
from time import sleep                 # sleep(ウェイト処理)ライブラリの読み込み
import RPi.GPIO as GPIO                # GPIO(汎用入出力端子)ライブラリの読み込み

# 変数
ledRed = 16       # as Red
ledBlue = 20      # as Blue
ledGreen = 21     # as Green
interval = 0.5    # 色変え間隔

# 初期設定
GPIO.setmode(GPIO.BCM)
GPIO.setup(ledRed, GPIO.OUT)
GPIO.setup(ledBlue, GPIO.OUT)
GPIO.setup(ledGreen, GPIO.OUT)

# 関数
def ledOff():
  GPIO.output (ledRed, False)
  GPIO.output (ledBlue, False)
  GPIO.output (ledGreen, False)
  sleep(0.04)

# メインループ
def main():
  try:
    while True:
      print "赤"
      GPIO.output (ledRed, True)
      sleep(interval)
      ledOff()
      print "青"
      GPIO.output (ledBlue, True)
      sleep(interval)
      ledOff()
      print "緑"
      GPIO.output (ledGreen, True)
      sleep(interval)
      ledOff()
      print "マゼンタ"
      GPIO.output (ledRed, True)
      GPIO.output (ledBlue, True)
      sleep(interval)
      ledOff()
      print "シアン"
      GPIO.output (ledBlue, True)
      GPIO.output (ledGreen, True)
      sleep(interval)
      ledOff()
      print "黃"
      GPIO.output (ledGreen, True)
      GPIO.output (ledRed, True)
      sleep(interval)
      ledOff()
      print "白"
      GPIO.output (ledRed, True)
      GPIO.output (ledBlue, True)
      GPIO.output (ledGreen, True)
      sleep(interval)
      ledOff()
      sleep (1)

  except KeyboardInterrupt:
    print " 終了しました"
    GPIO.cleanup()

if __name__ == "__main__":
    main()
