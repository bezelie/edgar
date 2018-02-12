#!/usr/bin/python
# -*- coding: utf-8 -*-
# Bezelie Python Module for Raspberry Pi
# べゼリー専用モジュール
from random import randint      # 
from time import sleep          #
import RPi.GPIO as GPIO         #
import smbus                    # for I2C
import math                     # 
import threading                # 
import json                     #

bus = smbus.SMBus(1)

# 変数
jsonFile = "/home/pi/bezelie/data_chat.json"        # 設定ファイル

class Control(object): # クラスの定義

    # 初期化メソッド。インスタンス生成時に自動実行される。
    def __init__(self, address_pca9685=0x40, dutyMax=490, dutyMin=110, dutyCenter=300, steps=1):
        f = open (jsonFile,'r')
        jDict = json.load(f)
        self.headTrim = int(jDict['data2'][0]['head'])    # トリム値の読み込み
        self.backTrim = int(jDict['data2'][0]['back'])
        self.stageTrim = int(jDict['data2'][0]['stage'])

        # インスタンス変数に値を代入。selfは自分自身のインスタンス名。
        self.address_pca9685 = address_pca9685
        self.dutyMax = dutyMax
        self.dutyMin = dutyMin
        self.dutyCenter = dutyCenter
        self.steps = steps
        self.headNow = dutyCenter
        self.backNow = dutyCenter
        self.stageNow = dutyCenter
        self.initPCA9685()
        # 第１引数はselfにするのが義務。

    def moveHead(self, degree, speed=1):
        max = 320     # 下方向の限界
        min = 230     # 上方向の限界
        self.headNow = self.moveServo(2, degree, self.headTrim, max, min, speed, self.headNow)

    def moveBack(self, degree, speed=1):
        max = 380     # 反時計回りの限界
        min = 220     # 時計回りの限界
        self.backNow = self.moveServo(1, degree, self.backTrim, max, min, speed, self.backNow)

    def moveStage(self, degree, speed=1):
        max = 390     # 反時計回りの限界
        min = 210     # 時計回りの限界
        self.stageNow = self.moveServo(0, degree, self.stageTrim, max, min, speed, self.stageNow)

    def moveCenter(self): # 3つのサーボの回転位置をトリム値に合わせる
        self.moveHead(self.headTrim)
        self.moveBack(self.backTrim)
        self.moveStage(self.stageTrim)

    def initPCA9685(self):
      try:
        bus.write_byte_data(self.address_pca9685, 0x00, 0x00)
        freq = 0.9 * 50
        prescaleval = 25000000.0    # 25MHz
        prescaleval /= 4096.0       # 12-bit
        prescaleval /= float(freq)
        prescaleval -= 1.0
        prescale = int(math.floor(prescaleval + 0.5))
        oldmode = bus.read_byte_data(self.address_pca9685, 0x00)
        newmode = (oldmode & 0x7F) | 0x10
        bus.write_byte_data(self.address_pca9685, 0x00, newmode)
        bus.write_byte_data(self.address_pca9685, 0xFE, prescale)
        bus.write_byte_data(self.address_pca9685, 0x00, oldmode)
        sleep(0.005)
        bus.write_byte_data(self.address_pca9685, 0x00, oldmode | 0xa1)
      except:
        pass
        # print "Please connect PCA9685 to RaspberryPi"

    def resetPCA9685(self):
        bus.write_byte_data(self.address_pca9685, 0x00, 0x00)

    def setPCA9685Duty(self, channel, on, off):
        channelpos = 0x6 + 4*channel
        try:
            bus.write_i2c_block_data(self.address_pca9685, channelpos, [on&0xFF, on>>8, off&0xFF, off>>8])
        except IOError:
            pass

    def moveServo(self, id, degree, trim, max, min, speed, now):
        dst = (self.dutyMin - self.dutyMax) * (degree + trim + 90) / 180 + self.dutyMax
        if speed == 0:
            self.setPCA9685Duty_(id, 0, dst)
            sleep(0.001 * math.fabs(dst - now))
            now = dst
        if dst > max:
            dst = max
        if dst < min:
            dst = min
        while (now != dst):
            if now < dst:
                now += self.steps
                if now > dst:
                    now = dst
            else:
                now -= self.steps
                if now < dst:
                    now = dst
            self.setPCA9685Duty(id, 0, now)
            sleep(0.004 * self.steps *(speed))
        return (now)

    def moveRnd(self):
        self.stop_event = threading.Event()
        r = randint(1,7)
        if r == 1:
            self.thread = threading.Thread(target = self.actHappy)
        elif r == 2:
            self.thread = threading.Thread(target = self.actNod)
        elif r == 3:
            self.thread = threading.Thread(target = self.actWhy)
        elif r == 4:
            self.thread = threading.Thread(target = self.actAround)
        elif r == 5:
            self.thread = threading.Thread(target = self.actUp)
        elif r == 6:
            self.thread = threading.Thread(target = self.actWave)
        else:
            self.thread = threading.Thread(target = self.actEtc)
        self.thread.start()

    def moveAct(self, act):
        self.stop_event = threading.Event()
        if act == 'happy':
            self.thread = threading.Thread(target = self.actHappy)
        elif act == 'nod':
            self.thread = threading.Thread(target = self.actNod)
        elif act == 'why':
            self.thread = threading.Thread(target = self.actWhy)
        elif act == 'around':
            self.thread = threading.Thread(target = self.actAround)
        elif act == 'up':
            self.thread = threading.Thread(target = self.actUp)
        elif act == 'wave':
            self.thread = threading.Thread(target = self.actWave)
        else:
            self.thread = threading.Thread(target = self.actEtc)
        self.thread.start()

    def actHappy(self, time=0.2): # しあわせ
        while not self.stop_event.is_set():
            self.moveHead(10)
            self.moveBack(5)
            self.moveBack(-5)
            # self.moveBack(10)
            # self.moveBack(-10)
            self.moveBack(0)
            sleep (time)
            self.moveHead(0)  
  
    def actNod(self, time=0.2): # うなづき
        while not self.stop_event.is_set():
            self.moveHead(-10)
            # self.moveHead(10)  
            # self.moveHead(-10)
            sleep (time)
            self.moveHead(0)  

    def actWhy(self, time=0.2): # 首かしげ
        while not self.stop_event.is_set():
            self.moveHead(10)
            self.moveBack(20)
            sleep (time)
            self.moveBack(0)
            self.moveHead(0)

    def actAround(self, time=0.2): # 見回し
        while not self.stop_event.is_set():
            # self.moveHead(20)
            self.moveStage(20)
            self.moveStage(-20)
            self.moveStage(0)
            sleep (time)
            self.moveHead(0)

    def actUp(self, time=0.2): # 見上げ
        while not self.stop_event.is_set():
            self.moveHead(30)
            # self.moveHead(-10)
            # self.moveHead(30)
            sleep (time)
            self.moveHead(0)

    def actWave(self, time=0.2): # くねくね
        while not self.stop_event.is_set():
            self.moveBack(20)
            self.moveStage(10)
            # self.moveBack(-20)
            self.moveStage(-10)
            # self.moveBack(10)
            self.moveStage(0)
            self.moveBack(0)

    def actEtc(self, time=0.5): # ETC
        while not self.stop_event.is_set():
            self.moveHead(-10)
            sleep (time)
            self.moveHead(0)  

    def stop(self):
        self.stop_event.set()
        self.thread.join()

# Centering Servo Motors
if __name__ == "__main__":  # Do only when this is done as a script
  bez = Control()               # べゼリー操作インスタンスの生成
  jsonFile = "data_chat.json"        # 設定ファイル
  f = open (jsonFile,'r')
  jDict = json.load(f)
  bez.headTrim = int(jDict['data2'][0]['head'])
  bez.backTrim = int(jDict['data2'][0]['back'])
  bez.stageTrim = int(jDict['data2'][0]['stage'])
  bez.moveCenter()
