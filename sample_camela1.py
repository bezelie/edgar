#!/usr/bin/python
# -*- coding: utf-8 -*- 
# Bezelie Sample Code for Raspberry Pi : Camera Moving Test

from  time import sleep
import picamera
import bezelie

# Centering All Servos
bez = bezelie.Control()               # べゼリー操作インスタンスの生成
bez.moveCenter()                      # サーボをセンタリング

# Main Loop
def main():
  try:
    with picamera.PiCamera() as camera:
      camera.resolution = (800, 480)   # change this number depending on your display
      camera.rotation = 180            # comment out if your screen is upside down
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
