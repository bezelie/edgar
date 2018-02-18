#!/usr/bin/python
# -*- coding: utf-8 -*-
# 音声対話デモ
# for Bezelie Edgar
# for Raspberry Pi
# by Jun Toyoda (Team Bezelie)
# from Aug15th2017

from datetime import datetime      # 現在時刻取得
from random import randint         # 乱数の発生
from time import sleep             # ウェイト処理
import subprocess                  # 外部プロセスを実行するモジュール
import threading                   # マルチスレッド処理
import socket                      # ソケット通信モジュール
import select                      # I/O処理完了待機モジュール
import json                        # jsonファイルを扱うモジュール
import csv                         # CSVファイルを扱うモジュール
import sys                         # python終了sys.exit()のために必要
import re                          # 正規表現モジュール
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
vol = jDict['data0'][0]['vol']         # スピーカー音量。
subprocess.call('amixer cset numid=1 '+vol+'% -q', shell=True)      # スピーカー音量
# mic = jDict['data0'][0]['mic']         # マイク感度。
mic = "60"                               # マイク感度。
subprocess.call('sudo amixer sset Mic '+mic+' -c 0 -q', shell=True) # マイク感度設定

# 変数の初期化
muteTime = 1        # 音声入力を無視する時間
bufferSize = 256    # 受信するデータの最大バイト。２の倍数が望ましい。

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

def alarm():
  f = open (jsonFile,'r')
  jDict = json.load(f)
  alarmOn = jDict['data1'][0]['alarmOn']
  alarmTime = jDict['data1'][0]['alarmTime']
  alarmKind = jDict['data1'][0]['alarmKind']
  now = datetime.now()
  if int(now.hour) == int(alarmTime[0:2]) and int(now.minute) == int(alarmTime[3:5]):
    if alarmOn == "true":
      # subprocess.call('sudo amixer -q sset Mic 0 -c 0', shell=True) 
      if alarmKind == 'mild':
        bez.moveAct('happy')
        subprocess.call("sh "+ttsFile+" "+"朝ですよ", shell=True)
        bez.stop()
      else:
        bez.moveAct('happy')
        subprocess.call("sh "+ttsFile+" "+"朝だよ起きて起きて起きてー", shell=True)
        bez.stop()
      sleep (muteTime)
      # subprocess.call('sudo amixer -q sset Mic '+mic+' -c 0', shell=True)
  t=threading.Timer(20,alarm) # ｎ秒後にまたスレッドを起動する
  t.setDaemon(True)           # メインスレッドが終了したら終了させる
  t.start()

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

  # 発話
  # subprocess.call('sudo amixer -q sset Mic 0 -c 0', shell=True)  # 自分の声を認識してしまわないようにマイクを切る
  # 設定ファイルの読み込み
  f = open (jsonFile,'r')
  jDict = json.load(f)
  vol = jDict['data0'][0]['vol']         # スピーカーボリューム
  # mic = jDict['data0'][0]['mic']         # マイク感度

  if timeCheck(): # 活動時間だったら会話する
    bez.moveRnd()
    subprocess.call('amixer cset numid=1 '+vol+'% -q', shell=True) # スピーカー音量
    subprocess.call("sh "+ttsFile+" "+data[ansNum][1], shell=True)
    bez.stop()
  else:           # 活動時間外は会話しない
    subprocess.call('amixer cset numid=1 60% -q', shell=True)      # スピーカー音量
    subprocess.call("sh "+ttsFile+" "+"活動時間外です", shell=True)
    sleep (5)
    subprocess.call('amixer cset numid=1 '+vol+'% -q', shell=True) # スピーカー音量
  # subprocess.call('sudo amixer -q sset Mic '+mic+' -c 0', shell=True)  # マイク感度を元に戻す

def socket_buffer_clear():
  while True:
    rlist, _, _ = select.select([client], [], [], 1)
    if len(rlist) > 0: 
      dummy_buffer = client.recv(bufferSize)
    else:
      break

def debug_message(message):
  t = datetime.now()
  message = str(t.minute)+":"+str(t.second)+":"+message
  print message
#  writeFile(message)
#  sys.stdout.write(message)
#　pass

def writeFile(text):                # デバッグファイル出力機能
  f = open (debugFile,'r')
  textBefore = ""
  for row in f:
    textBefore = textBefore + row
  f.close()
  f = open (debugFile,'w')
  f.write(textBefore + text + "\n")
  f.close()

# サーボの初期化
bez = bezelie.Control() # べゼリー操作インスタンスの生成
bez.moveCenter()        # サーボの回転位置をトリム値に合わせる
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# メインループ
def main():
  t=threading.Timer(10,alarm)
  t.setDaemon(True)
  t.start()
  bez.moveAct('happy')
  subprocess.call("sh "+ttsFile+" "+u"こんにちは"+user, shell=True)
  subprocess.call("sh "+ttsFile+" "+u"ぼく"+name, shell=True)
  bez.stop()
  # subprocess.call('sh exec_camera.sh', shell=True)            # カメラの映像をディスプレイに表示
  sleep (1)
  # TCPクライアントを作成しJuliusサーバーに接続する
  enabled_julius = False
  for count in range(5):
    try:
      client.connect(('localhost', 10500))
      enabled_julius = True
      break
    except socket.error, e:
      print 'failed socket connect. retry'
      sleep (1)
  if enabled_julius == False:
    print 'Juliusが見つかりませんでした'
    sys.exit(1)
  data = ""
  socket_buffer_clear()
  try:
    while True:
      if "</RECOGOUT>\n." in data:  # RECOGOUTツリーの最終行を見つけたら以下の処理を行う
        data = re.search(r'WORD\S+', data)                          # dataからWORD\sで始まる行を抽出
        keyWord = data.group().replace("WORD=","").replace("\"","") # dataからキーワード以外を削除
        replyMessage(keyWord)
        socket_buffer_clear()
        data = ""  # 認識終了したのでデータをリセットする
      else:
        data = data + client.recv(bufferSize)  # Juliusサーバーから受信
  except KeyboardInterrupt: # CTRL+Cで終了
    debug_message(' 終了しました')
    client.close()
    bez.moveCenter()
    bez.stop()
    sys.exit(0)

if __name__ == "__main__":
  main()
  sys.exit(0)
