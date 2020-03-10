#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2018 Guenter Bartsch
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

#
# example program for kaldi live nnet3 chain online decoding
#
# configured for embedded systems (e.g. an rpi3) with models
# installed in /opt/kaldi/model/
#
# adapted by @libbymiller to add movement

import traceback
import logging
import datetime

from time                  import time
from nltools               import misc
from nltools.pulserecorder import PulseRecorder
from nltools.vad           import VAD, BUFFER_DURATION
from nltools.asr           import ASR, ASR_ENGINE_NNET3
from optparse              import OptionParser

# gpio stuff

import RPi.GPIO as GPIO

from time import sleep

GPIO.setmode(GPIO.BOARD)

pin0 = 11
pin1 = 13

GPIO.setup(pin0, GPIO.OUT)
GPIO.setup(pin1, GPIO.OUT)

pwm=GPIO.PWM(pin0, 50)
pwm1=GPIO.PWM(pin1, 50)

pwm.start(0)
pwm1.start(0)

def SetAngle(angle):
	duty = angle / 18 + 2
	GPIO.output(pin0, True)
	pwm.ChangeDutyCycle(duty)
	sleep(1)
	GPIO.output(pin0, False)
	pwm.ChangeDutyCycle(0)


def SetAngle1(angle):
	duty = angle / 18 + 2
	GPIO.output(pin1, True)
	pwm1.ChangeDutyCycle(duty)
	sleep(1)
	GPIO.output(pin1, False)
	pwm1.ChangeDutyCycle(0)



# adding words stuff
import os

import random
import re
import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')

words = {}
quotes_index = {} # word => quote number
quotes_array = []
count = 0
new_words = {}

# now take a random keyword

def get_random_quote_by_keyword(keyword):
   if(keyword in quotes_index):
      arr = quotes_index[keyword]
      x = random.choice(arr)
      print(arr)
      print(x)
      print(quotes_array[x])
      return x
   return None

with open("inspiration_short.txt", "r") as ins:
    for line in ins:
       line = line.strip()
       if(line!=""):
         quotes_array.append(line)
         sentences = word_tokenize(str(line))
         sentences = [word.lower() for word in sentences if re.match('^[a-zA-Z]+', word)]  
         for s in sentences:
           if (s in words):
             w = words[s]
             w = w + 1
             words[s] = w             
           else:
             words[s] = 1
           if(s in quotes_index):
             quotes_index[s].append(count)
           else:
             quotes_index[s] = []
             quotes_index[s].append(count)

       count = count + 1



for w in words:
  num = words[w]
  if(num < 40):
    new_words[w] = num


### end words stuff

PROC_TITLE                       = 'kaldi_live_demo'

DEFAULT_VOLUME                   = 150
DEFAULT_AGGRESSIVENESS           = 2

# DEFAULT_MODEL_DIR                = '/opt/kaldi/model/kaldi-generic-de-tdnn_250'
DEFAULT_MODEL_DIR                = '/opt/kaldi/model/kaldi-generic-en-tdnn_250'
DEFAULT_ACOUSTIC_SCALE           = 1.0
DEFAULT_BEAM                     = 7.0
DEFAULT_FRAME_SUBSAMPLING_FACTOR = 3

STREAM_ID                        = 'mic'

#
# init
#

misc.init_app(PROC_TITLE)

print "Kaldi live demo V0.2"

#
# cmdline, logging
#

parser = OptionParser("usage: %prog [options]")

parser.add_option ("-a", "--aggressiveness", dest="aggressiveness", type = "int", default=DEFAULT_AGGRESSIVENESS,
                   help="VAD aggressiveness, default: %d" % DEFAULT_AGGRESSIVENESS)

parser.add_option ("-m", "--model-dir", dest="model_dir", type = "string", default=DEFAULT_MODEL_DIR,
                   help="kaldi model directory, default: %s" % DEFAULT_MODEL_DIR)

parser.add_option ("-v", "--verbose", action="store_true", dest="verbose",
                   help="verbose output")

parser.add_option ("-s", "--source", dest="source", type = "string", default=None,
                   help="pulseaudio source, default: auto-detect mic")

parser.add_option ("-V", "--volume", dest="volume", type = "int", default=DEFAULT_VOLUME,
                   help="broker port, default: %d" % DEFAULT_VOLUME)

(options, args) = parser.parse_args()

if options.verbose:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

source         = options.source
volume         = options.volume
aggressiveness = options.aggressiveness
model_dir      = options.model_dir

#
# pulseaudio recorder
#

rec = PulseRecorder (source_name=source, volume=volume)

#
# VAD
#

vad = VAD(aggressiveness=aggressiveness)

#
# ASR
#

print "Loading model from %s ..." % model_dir

asr = ASR(engine = ASR_ENGINE_NNET3, model_dir = model_dir,
          kaldi_beam = DEFAULT_BEAM, kaldi_acoustic_scale = DEFAULT_ACOUSTIC_SCALE,
          kaldi_frame_subsampling_factor = DEFAULT_FRAME_SUBSAMPLING_FACTOR)


#
# main
#


rec.start_recording()

print "Please speak."

while True:
  try:

    samples = rec.get_samples()
    audio, finalize = vad.process_audio(samples)

    if not audio:
        continue

    logging.debug ('decoding audio len=%d finalize=%s audio=%s' % (len(audio), repr(finalize), audio[0].__class__))

    user_utt, confidence = asr.decode(audio, finalize, stream_id=STREAM_ID)
    #print "\r%s                     " % user_utt,

    if finalize:
        print(user_utt)
        arr = user_utt.split(" ")
        print(arr)
        if("yes" in arr):
           SetAngle(90) 
           SetAngle(180)
           SetAngle(0)  
        else:
           if("no" in arr):
              SetAngle1(90) 
              SetAngle1(180)
              SetAngle1(0)  
        user_utt = ""
  except KeyboardInterrupt:
    print 'Interrupted'
    pwm.stop()
    pwm1.stop()
    GPIO.cleanup()
    sys.exit(0)



