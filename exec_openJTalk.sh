#!/bin/bash
HTSVOICE=/usr/share/hts-voice/mei/mei_happy.htsvoice
DICDIRE=/var/lib/mecab/dic/open-jtalk/naist-jdic/
VOICEDATA=/tmp/voice.wav
sudo echo "$1" | open_jtalk \
-x $DICDIRE \
-m $HTSVOICE \
-ow $VOICEDATA \
-s 20000 \
-p 120 \
-a 0.02 \
-b 0.0 \
-r 1.2 \
-fm -5.0 \
-u 0.0 \
-jm 1.0 \
-jf 1.5 \
-z 0.0 \

aplay -q -D plughw:1,0 $VOICEDATA
sudo rm -f $VOICEDATA
