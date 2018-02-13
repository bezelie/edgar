#!/usr/bin/python
# -*- coding: utf-8 -*-
# 顔認識デモ
# for Bezelie Edgar
# for Raspberry Pi
# by Jun Toyoda (Team Bezelie)
# from Aug15th2017

from datetime import datetime      # 現在時刻取得
from random import randint         # 乱数の発生
from time import sleep             # ウェイト処理
import subprocess                  # 外部プロセスを実行するモジュール
import json                        # jsonファイルを扱うモジュール
import csv                         # CSVファイルを扱うモジュール
import sys                         # python終了sys.exit()のために必要
import picamera                    # カメラ用モジュール
import picamera.array              # カメラ用モジュール
import cv2                         # Open CVモジュール    
import bezelie                     # べゼリー専用サーボ制御モジュール

csvFile   = "/home/pi/bezelie/chatDialog.csv"          # 対話リスト
jsonFile  = "/home/pi/bezelie/edgar/data_chat.json"    # 設定ファイル
ttsFile   = "/home/pi/bezelie/edgar/exec_openJTalk.sh" # 音声合成
debugFile = "/home/pi/bezelie/debug.txt"               # debug用

# 設定ファイルの読み込み
f = open (jsonFile,'r')
jDict = json.load(f)
name = jDict['data0'][0]['name']       # べゼリーの別名。
user = jDict['data0'][0]['user']       # ユーザーのニックネーム。
mic = jDict['data0'][0]['mic']         # マイク感度。62が最大値。
vol = jDict['data0'][0]['vol']         # スピーカー音量。

# 変数の初期化
alarmStop = False   # アラームのスヌーズ機能（非搭載）
is_playing = False  # 再生中か否かのフラグ
waitTime = 5        # autoモードでの会話の間隔

# OpenCV
cascade_path =  "/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml" # 顔認識xml
cascade = cv2.CascadeClassifier(cascade_path)

# 関数
def timeCheck(): # 活動時間内かどうかのチェック
  f = open (jsonFile,'r')
  jDict = json.load(f)
  awake1Start = jDict['data1'][0]['awake1Start']
  awake1End = jDict['data1'][0]['awake1End']
  awake2Start = jDict['data1'][0]['awake2Start']
  awake2End  = jDict['data1'][0]['awake2End']
  t = datetime.now()
  if   int(t.hour) >  int(awake1Start[0:2]) and int(t.hour) <    int(awake1End[0:2]):
    flag = True
  elif int(t.hour) == int(awake1Start[0:2]) and int(t.minute) >= int(awake1Start[3:5]):
    flag = True
  elif int(t.hour) == int(awake1End[0:2])   and int(t.minute) <= int(awake1End[3:5]):
    flag = True
  elif int(t.hour) >  int(awake2Start[0:2]) and int(t.hour) <    int(awake2End[0:2]):
    flag = True
  elif int(t.hour) == int(awake2Start[0:2]) and int(t.minute) >= int(awake2Start[3:5]):
    flag = True
  elif int(t.hour) == int(awake2End[0:2])   and int(t.minute) <= int(awake2End[3:5]):
    flag = True
  else:
    flag = False # It is not Active Time
  return flag

def replyMessage(keyWord):        # 対話
  data = []                       # 対話ファイル（csv）を変数dataに読み込む
  with open(csvFile, 'rb') as f:  # csvFileをオープン
    for i in csv.reader(f):       # ファイルから１行ずつiに読み込む
      data.append(i)              # dataに追加

  data1 = []                      # dataから質問内容がキーワードに一致している行をdata1として抜き出す
  for index,i in enumerate(data): # index=連番
    if unicode(i[0], 'utf-8')==keyWord:  # i[0]はstrなのでutf-8に変換して比較する必要がある
      j = randint(1,100)          # １から１００までの乱数を発生させる
      data1.append(i+[j]+[index]) # data1=質問内容,返答,乱数,連番のリスト

  if data1 == []:                 # data1が空っぽだったらランダムで返す
    for index,i in enumerate(data): 
      j = randint(1,100)         
      data1.append(i+[j]+[index])

  maxNum = 0                      # 複数の候補からランダムで選出。data1から欄数値が最大なものを選ぶ
  for i in data1:                 
    if i[2] > maxNum:              
      maxNum = i[2]                
      ansNum = i[3]               

  # 設定ファイルの読み込み
  f = open (jsonFile,'r')
  jDict = json.load(f)
  mic = jDict['data0'][0]['mic']         # マイク感度の設定。
  vol = jDict['data0'][0]['vol']         # スピーカー音量。

  bez.moveRnd()
  subprocess.call('amixer cset numid=1 '+vol+'% -q', shell=True) # スピーカー音量
  subprocess.call("sh "+ttsFile+" "+data[ansNum][1], shell=True)
  bez.stop()

def debug_message(message):
  print message
#  writeFile(message)
#　pass
#  sys.stdout.write(message)

def writeFile(text): # デバッグファイル出力機能
  f = open (debugFile,'r')
  textBefore = ""
  for row in f:
    textBefore = textBefore + row
  f.close()
  f = open (debugFile,'w')
  f.write(textBefore + text + "\n")
  f.close()

# サーボの初期化
bez = bezelie.Control()                 # べゼリー操作インスタンスの生成
bez.moveCenter()                        # サーボの回転位置をトリム値に合わせる

# メインループ
def main():
  try:
    subprocess.call('amixer cset numid=1 '+vol+'% -q', shell=True)      # スピーカー音量
    subprocess.call("sh "+ttsFile+" "+u"顔認識モード", shell=True)
    stageAngle = 0           # ステージの初期角度
    stageDelta = 5           # ループごとにステージを回転させる角度
    stageSpeed = 8           # ループごとにステージを回転させる速度
    with picamera.PiCamera() as camera:                         # Open Pi-Camera as camera
      with picamera.array.PiRGBArray(camera) as stream:         # Open Video Stream from Pi-Camera as stream
        camera.resolution = (640, 480)                          # Display Resolution
        # camera.resolution = (1280, 720)                       # Display Resolution
        # camera.resolution = (1920, 1080)                      # Display Resolution
        camera.hflip = True                                     # Vertical Flip 
        camera.vflip = True                                     # Horizontal Flip
        while True:
          if timeCheck(): # 活動時間だったら動く
            camera.capture(stream, 'bgr', use_video_port=True)    # Capture the Video Stream
            gray = cv2.cvtColor(stream.array, cv2.COLOR_BGR2GRAY) # Convert BGR to Grayscale
            facerect = cascade.detectMultiScale(gray,             # Find face from gray
              scaleFactor=1.9,                                    # 1.1 - 1.9 :the bigger the quicker & less acurate 
              minNeighbors=3,                                     # 3 - 6 : the smaller the more easy to detect
              minSize=(100,120),                                   # Minimam face size 
              maxSize=(640,480))                                  # Maximam face size
            if len(facerect) > 0:
              for rect in facerect:
                cv2.rectangle(stream.array,                       # Draw a red rectangle at face place 
                  tuple(rect[0:2]),                               # Upper Left
                  tuple(rect[0:2]+rect[2:4]),                     # Lower Right
                  (0,0,255), thickness=2)                         # Color and thickness
              replyMessage(u"顔認識")
            # cv2.imshow('frame', stream.array)                     # 画面に表示したい場合はコメント外してください
            if cv2.waitKey(1) & 0xFF == ord('q'):                 # Quit operation
              break
            stream.seek(0)                                        # Reset the stream
            stream.truncate()
            stageAngle = stageAngle + stageDelta            
            if stageAngle > 30 or stageAngle < -30:
              stageDelta = stageDelta*(-1)
            bez.moveStage(stageAngle,stageSpeed)
          else:           # 活動時間外は動作しない
            subprocess.call('amixer cset numid=1 60% -q', shell=True)      # スピーカー音量を調整
            subprocess.call("sh "+ttsFile+" "+"活動時間外です", shell=True)
            print "活動時間外なので発声・動作しません"
            sleep (600)   # 10分待機
            subprocess.call('amixer cset numid=1 '+vol+'% -q', shell=True) # スピーカー音量を戻す
        cv2.destroyAllWindows()

  except KeyboardInterrupt: # CTRL+Cで終了
    debug_message('keyboard interrupted')
    bez.moveCenter()
    bez.stop()
    sys.exit(0)

if __name__ == "__main__":
  debug_message('---------- started ----------')
  main()
  sys.exit(0)
