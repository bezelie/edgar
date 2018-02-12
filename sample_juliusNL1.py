#!/usr/bin/python
# -*- coding: utf-8 -*-
# Julius音声認識（自然言語版）サンプル
# for Bezelie Edgar
# for Raspberry Pi
# by Jun Toyoda (Team Bezelie)
# from Aug15th2017

from time import sleep             # ウェイト処理
import subprocess                  # 外部プロセスを実行するモジュール
import bezelie                     # べゼリー専用モジュール
import socket                      # ソケット通信モジュール
import select                      # 待機モジュール
import json                        # jsonファイルを扱うモジュール
import csv                         # CSVファイルを扱うモジュール
import sys                         # python終了sys.exit()のために必要
import re                          # 正規表現モジュール
import xml.etree.ElementTree as ET # XMLエレメンタルツリー変換モジュール

jsonFile = "/home/pi/bezelie/data_chat.json"          # 設定ファイル
ttsFile  = "/home/pi/bezelie/edgar/exec_openJTalk.sh" # 音声合成

# 設定ファイルの読み込み
f = open (jsonFile,'r')
jDict = json.load(f)
mic = jDict['data0'][0]['mic']         # マイク感度。62が最大値。
vol = jDict['data0'][0]['vol']         # スピーカー音量。

# 変数の初期化
muteTime = 1        # 音声入力を無視する時間
bufferSize = 256    # 受信するデータの最大バイト。２の倍数が望ましい。

# 関数
def socket_buffer_clear():
  while True:
    rlist, _, _ = select.select([client], [], [], 1)
    if len(rlist) > 0: 
      dummy_buffer = client.recv(bufferSize)
    else:
      break

# TCPクライアントを作成しJuliusサーバーに接続する
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
enabled_julius = False
for count in range(3):
  try:
    client.connect(('localhost', 10500))
    # client.connect(('10.0.0.1', 10500))  # Juliusサーバーに接続
    enabled_julius = True
    break
  except socket.error, e:
    # print 'failed socket connect. retry'
    pass
if enabled_julius == False:
  print 'Juliusが起動していないようです'
  sys.exit(1)

# メインループ
def main():
  try:
    subprocess.call('amixer cset numid=1 '+vol+'% -q', shell=True)      # スピーカー音量
    subprocess.call('sudo amixer -q sset Mic 0 -c 0', shell=True)       # 自分の声を認識してしまわないようにマイクを切る
    subprocess.call("sh "+ttsFile+" 音声認識開始", shell=True)
    sleep (muteTime)
    subprocess.call('sudo amixer sset Mic '+mic+' -c 0 -q', shell=True) # マイク感受性
    socket_buffer_clear()
    print 'ー何か喋ってくださいー'
    data = ""
    while True:
      if "</RECOGOUT>\n." in data:  # RECOGOUTツリーの最終行を見つけたら以下の処理を行う
        try:
          # dataから必要部分だけ抽出し、かつエラーの原因になる文字列を削除する。
          data = data[data.find("<RECOGOUT>"):].replace("\n.", "").replace("</s>","").replace("<s>","")
          # fromstringはXML文字列からコンテナオブジェクトであるElement型に直接変換する。
          root = ET.fromstring('<?xml version="1.0" encoding="utf-8" ?>\n' + data)
          keyword = ""
          for whypo in root.findall("./SHYPO/WHYPO"):
            keyword = keyword + whypo.get("WORD")
          subprocess.call('sudo amixer -q sset Mic 0 -c 0', shell=True)        # 自分の声を認識してしまわないようにマイクを切る
          print keyword
          subprocess.call("sh "+ttsFile+" "+keyword, shell=True)
          sleep (muteTime)
          socket_buffer_clear()
          subprocess.call('sudo amixer -q sset Mic '+mic+' -c 0', shell=True)  # マイク感受性を元に戻す
          print "ー何か喋ってくださいー"
        except:
          print "----- except -----"
        data = ""  # 認識終了したのでデータをリセットする
      else:
        data = data + client.recv(bufferSize)  # Juliusサーバーから受信
        # /RECOGOUTに達するまで受信データを追加していく
  except KeyboardInterrupt: # CTRL+Cで終了
    client.close()
    sys.exit(0)

if __name__ == "__main__":
  main()
  sys.exit(0)
