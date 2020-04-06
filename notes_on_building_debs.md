The maintainer of Zamia doesn't have time to build the raspian packages 
needed any more, so I've started to try and figure it out - all the 
scripts are on his [github](https://github.com/gooofy/zamia-dist) but there are no instructions I can find.

I think you need to build:

 * kaldi-chain-zamia-speech-en_20190609-1_armhf.deb
 * libkaldi-asr (not finished)
 * python-kaldiasr (not got that far yet)
 * python-nltools (not got that far yet)

python-nltools has a load of dependencies: python-espeakng, python-marytts, python-num2words, python-picotts, python-webrtcvad.
  
This is extrapolating from [here](https://github.com/libbymiller/zamia_listening_pi/blob/master/README.md) which I got from his [now-outdated docs](https://github.com/gooofy/zamia-speech#get-started-with-our-pre-trained-models) on the zamia github.)

# 1. kaldi-chain-zamia-speech-en_20190609-1_armhf.deb

This is pretty easy to build, took 24 mins on a pi4 (the only linux machine I have 
handy).

Instructions - 

    git clone https://github.com/gooofy/zamia-dist
    cd zamia-dist/raspbian-ai

download the en models from https://goofy.zamia.org/zamia-speech/asr-models/ into that directory

```
[   ]   kaldi-generic-en-tdnn_250-r20190609.tar.xz      2019-06-09 20:16        108M
[   ]   kaldi-generic-en-tdnn_f-r20190609.tar.xz        2019-06-09 23:13        159M
[   ]   kaldi-generic-en-tri2b_chain-r20190609.tar.xz   2019-06-09 21:05        151M
```

untar them all using `tar -xvf`

    ./doit.sh


For installation:

`sudo dpkg -i kaldi-chain-zamia-speech-en_20190609-1_armhf.deb`

 this complains that a couple of things are missing - 

`libatlas-base` which is easy (`sudo apt-get install libatlas-base-dev`)

and `libkaldi-asr` which requires another build.


# 2. libkaldi-asr

[not finished this one and guessing a bit]

    cd zamia-dist/raspbian-ai/libkaldi-asr
    git clone https://github.com/kaldi-asr/kaldi

    sudo apt-get update
    sudo apt-get install devscripts # for debuild ... seems like overkill!

    ./doit.sh 

fails, mising kaldi libs

    cd zamia-dist/raspbian-ai/libkaldi-asr/kaldi/tools
    sudo apt-get install sox gfortran subversion
    extras/install_openblas.sh

    make 

update - seems to need 32GB to work...

....
