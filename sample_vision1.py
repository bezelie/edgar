#!/usr/bin/python
# -*- coding: utf-8 -*-
# demo Code for Raspberry Pi : Label Recognition of Google Vision API

from time import sleep
import subprocess
import picamera
import requests
import base64
import json
import bezelie

# Variables
GOOGLE_CLOUD_VISION_API_URL = 'https://vision.googleapis.com/v1/images:annotate?key='
API_KEY = ''  # Google Cloud Platform Consoleで登録したAPIキー
jpgFile = '/home/pi/Pictures/capture.jpg'  # キャプチャー画像ファイル

# Functions
def request_cloud_vison_api(image_base64):
    api_url = GOOGLE_CLOUD_VISION_API_URL + API_KEY
    req_body = json.dumps({
        'requests': [{
            'image': {
                'content': image_base64.decode('utf-8') # base64でencodeする。
            },
            'features': [{
                'type': 'LABEL_DETECTION',
#                'type': 'TEXT_DETECTION',
#                'type': 'LOGO_DETECTION',
                'maxResults': 3,
            }]
        }]
    })
    res = requests.post(api_url, data=req_body)
    return res.json()

# Setting
bez = bezelie.Control()               # べゼリー操作インスタンスの生成
bez.moveCenter()                      # サーボをセンタリング

# Main Loop
def main():
  try:
    print "カメラの前に何かをかざしてください"
    with picamera.PiCamera() as camera:
      camera.resolution = (640, 480)   # Change this number for your display
      camera.rotation = 180            # comment out if your screen upside down
      camera.start_preview()
      sleep(1)
      while True:
        print "--------------------"
        camera.stop_preview()
        camera.capture(jpgFile)
        sleep(0.1)
        with open(jpgFile, 'rb') as img:
          img_byte = img.read()
        img_base64 = base64.b64encode(img_byte)
        result = request_cloud_vison_api(img_base64)
        for i in range(3):
          try:
            answer = result['responses'][0]['labelAnnotations'][i]['description'].encode('utf-8')
            print (answer)
            subprocess.call('flite -voice "kal16" -t "'+ answer +'"', shell=True)
            # Other English Voices :kal awb_time kal16 awb rms slt
          except:
            print ("no answer")
        camera.start_preview()
        sleep (3)

  except KeyboardInterrupt:
    # CTRL+Cで終了
    print "  終了しました"

if __name__ == "__main__":
    main()


