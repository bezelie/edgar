#!/usr/bin/python
# -*- coding: utf-8 -*-
from random import randint         # 乱数の発生
import RPi.GPIO as GPIO
from time import sleep
import bezelie
import subprocess                     # 外部プロセスを実行するモジュール

# 準備
bez = bezelie.Control()               # べゼリー操作インスタンスの生成
bez.moveCenter()                      # サーボをセンタリング
sleep(0.5)

# 初期設定
GPIO.setmode(GPIO.BCM)                 # GPIOをGPIO番号で指定できるように設定
GPIO.setup(24, GPIO.IN)                # GPIOの24ピンを入力モードに設定
GPIO.setup(25, GPIO.IN)                # GPIOの25ピンを入力モードに設定

# 変数設定
headNow = 0
headOld = headNow
backNow = 0
backOld = backNow
stageNow = 0
stageOld = stageNow

# MCP3208からSPI通信で12ビットのデジタル値を取得。0から7の8チャンネル使用可
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
    if adcnum > 7 or adcnum < 0:
        return -1
    GPIO.output(cspin, GPIO.HIGH)
    GPIO.output(clockpin, GPIO.LOW)
    GPIO.output(cspin, GPIO.LOW)

    commandout = adcnum
    commandout |= 0x18  # スタートビット＋シングルエンドビット
    commandout <<= 3    # LSBから8ビット目を送信するようにする
    for i in range(5):
        # LSBから数えて8ビット目から4ビット目までを送信
        if commandout & 0x80:
            GPIO.output(mosipin, GPIO.HIGH)
        else:
            GPIO.output(mosipin, GPIO.LOW)
        commandout <<= 1
        GPIO.output(clockpin, GPIO.HIGH)
        GPIO.output(clockpin, GPIO.LOW)
    adcout = 0
    # 13ビット読む（ヌルビット＋12ビットデータ）
    for i in range(13):
        GPIO.output(clockpin, GPIO.HIGH)
        GPIO.output(clockpin, GPIO.LOW)
        adcout <<= 1
        if i>0 and GPIO.input(misopin)==GPIO.HIGH:
            adcout |= 0x1
    GPIO.output(cspin, GPIO.HIGH)
    return adcout

GPIO.setmode(GPIO.BCM)
# ピンの名前を変数として定義
SPICLK = 11
SPIMOSI = 10
SPIMISO = 9
SPICS = 8
# SPI通信用の入出力を定義
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICS, GPIO.OUT)

try:
  while True:
    if GPIO.input(25)==GPIO.HIGH:    # GPIO24に3.3Vの電圧がかかっていたら・・$
      print "スイッチ24が押されています"
      r = randint(1,3)
      if r > 2:
        subprocess.call('flite -voice "slt" -t "Nice to meet you"', shell=True) # $
      elif r > 1:
        subprocess.call('flite -voice "slt" -t "I am grad to meet you"', shell=True) # $
      else:
        subprocess.call('flite -voice "slt" -t "Hi, ! am Bezelie"', shell=True) # $
       # Other English Voices :kal awb_time kal16 awb rms slt
      continue
    if GPIO.input(24)==GPIO.HIGH:    # GPIO24に3.3Vの電圧がかかっていたら・・$
      print "スイッチ25が押されています"
      r = randint(1,3)
      if r > 2:
        subprocess.call('flite -voice "slt" -t "It is awesome!"', shell=True) # $
      elif r > 1:
        subprocess.call('flite -voice "slt" -t "That is great!"', shell=True) # $
      else:
        subprocess.call('flite -voice "slt" -t "How wonderful it is!"', shell=True) # $
      continue

    inputVal0 = readadc(0, SPICLK, SPIMOSI, SPIMISO, SPICS)
    inputVal0 = inputVal0*180/4096-90
    if inputVal0 > 40:inputVal0=40
    if inputVal0 < -40:inputVal0=-40
    print("stage:"+str(inputVal0))
    if abs(inputVal0 - stageOld) > 4:
      stageOld = inputVal0
      bez.moveStage(inputVal0)

    inputVal1 = readadc(1, SPICLK, SPIMOSI, SPIMISO, SPICS)
    inputVal1 = inputVal1*60/4096-30
    if inputVal1 > 30:inputVal1=30
    if inputVal1 < -30:inputVal1=-30
    print("back:"+str(inputVal1))
    if abs(inputVal1 - backOld) > 4:
      backOld = inputVal1
      bez.moveBack(inputVal1)

    inputVal2 = readadc(2, SPICLK, SPIMOSI, SPIMISO, SPICS)
    inputVal2 = inputVal2*40/4096-30
    if inputVal2 > 20:inputVal2=20
    if inputVal2 < -30:inputVal2=-30
    inputVal2 = inputVal2*(-1)
    print("head:"+str(inputVal2))
    if abs(inputVal2 - headOld) > 4:
      headOld = inputVal2
      bez.moveHead(inputVal2)
    sleep(0.1)

except KeyboardInterrupt:
    pass

GPIO.cleanup()
