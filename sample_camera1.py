#!/usr/bin/python
# -*- coding: utf-8 -*- 
# Bezelie Sample Code for Raspberry Pi : Camera Moving Test

from  time import sleep                # ウェイト処理
import picamera                        # カメラモジュール
import bezelie                         # べゼリー専用サーボ制御モジュール

# サーボの準備
bez = bezelie.Control()                # べゼリー操作インスタンスの生成
bez.moveCenter()                       # サーボをセンタリング

# メインループ
def main():
  try:
    with picamera.PiCamera() as camera:
      camera.resolution = (640, 480)   # お使いのディスプレイに合わせて調整してください
      camera.rotation = 180            # 画面が上下逆さまだったらこの行は削除してください。
      camera.start_preview()
      sleep(2)
      head = 0
      while (True):
        bez.moveBack (10)
        bez.moveStage (30, 2)
        sleep (0.5)
        bez.moveBack (-10)
        bez.moveStage (-30, 2)
        sleep (0.5)
        head += 10
        if head > 20:
          head = -10
        bez.moveHead (head)
  except KeyboardInterrupt:
    print " Interrupted by Keyboard"

if __name__ == "__main__":
    main()
