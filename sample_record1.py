#!/usr/bin/python
# -*- coding: utf-8 -*-
# Bezelie demo Code for Raspberry Pi : 音声録音サンプル
# ラズパイにマイクとスピーカーを接続してから実行してください。

# ライブラリの読み込み
from time import sleep
import subprocess
import pyaudio
import wave

# 音声合成シェルスクリプトのファイル名の指定
openJTalkFile = "exec_openJTalk.sh"

# Pyaudio
RATE = 44100              #サンプル周波数 取り込み１回分の時間
CHUNK = 2**9              #取り込み１回分のデータサイズ 512
FORMAT = pyaudio.paInt16  #データフォーマットは int16型
CHANNELS = 1              #モノラル
RECORD_SECONDS = 2        #録音する時間の長さ
DEVICE_INDEX = 0
WAVE_OUTPUT_FILENAME = "test.wav"
audio = pyaudio.PyAudio() #pyaudioのインスタンスaudioを生成

# Main Loop
def main():
  try:
    while (True):
      subprocess.call("sh "+openJTalkFile+" "+"何か言って", shell=True)
      print ("recording...")
      sleep(1)
      # Record
      stream = audio.open(format=FORMAT,
        channels=CHANNELS,
        rate=RATE, input=True,  #入力モード
        input_device_index = DEVICE_INDEX,
        frames_per_buffer = CHUNK)
      frames = []
      for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read (CHUNK )
        frames.append (data )
      stream.stop_stream()           # streamを停止
      stream.close()                 # streamを開放
      waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb') # wavファイルをwbモードで開く
      waveFile.setnchannels(CHANNELS)
      waveFile.setsampwidth(audio.get_sample_size(FORMAT))
      waveFile.setframerate(RATE)
      waveFile.writeframes(b''.join(frames))
      waveFile.close()
      # Play
      subprocess.call("sh "+openJTalkFile+" "+"再生します", shell=True)
      print ("finished recording")
      subprocess.call('aplay -D plughw:1 "'+ WAVE_OUTPUT_FILENAME +'"', shell=True)
      sleep (2)

  except KeyboardInterrupt:
    print " Interrupted by Keyboard"
    audio.terminate()              # インスタンスaudioを終了

if __name__ == "__main__":
    main()
