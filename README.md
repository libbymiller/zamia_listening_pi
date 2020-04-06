# Zamia on a Pi 3

[Zamia](http://goofy.zamia.org/) is a version of Kaldi - speech to text. This is a how-to for making it work on a Raspberry Pi 3.

I used python 2.7 - not tried with python 3 yet.

To make it work it really needs a good microphone. I used a [respeaker 4 mic](https://www.seeedstudio.com/ReSpeaker-4-Mic-Array-for-Raspberry-Pi.html). 

I used Raspian Buster lite.

# Clone this directory onto the pi

    git checkout https://github.com/libbymiller/zamia_listening_pi

# Install Zamia

Dependencies

    sudo apt-get install zip git libatlas-base-dev cython python-future python-requests python-setproctitle espeak-ng

More dependencies - [from here](https://github.com/alexylem/jarvis/issues/129#issuecomment-248072872)

    curl -O http://ftp.fr.debian.org/debian/pool/non-free/s/svox/libttspico-data_1.0+git20130326-3_all.deb
    curl -O http://ftp.fr.debian.org/debian/pool/non-free/s/svox/libttspico0_1.0+git20130326-3_armhf.deb
    curl -O http://ftp.fr.debian.org/debian/pool/non-free/s/svox/libttspico-utils_1.0+git20130326-3_armhf.deb

    sudo dpkg -i libttspico-data_1.0+git20130326-3_all.deb
    sudo dpkg -i libttspico0_1.0+git20130326-3_armhf.deb
    sudo dpkg -i libttspico-utils_1.0+git20130326-3_armhf.deb

<a href="https://twitter.com/Gooofy">Günter Bartsch</a> - who runs [zamia.org](zamia.org), which is where all this work came from - used to build the debian packages but can't right now - I've included the ones you 
need in this repo, apart from kaldi-chain-zamia-speech [which you need to download from dropbox](https://www.dropbox.com/transfer/AAAAADYHFQTdVbYixPNTKhTA-b0yc44nIh3pUPQP9QLjZ9p6YhddQ2w) because it's 431MB, and [started but not finished some build instructions](https://github.com/libbymiller/zamia_listening_pi/blob/master/notes_on_building_debs.md).

    sudo dpkg -i libkaldi-asr_5.4.248-3_armhf.deb
    sudo dpkg -i kaldi-chain-zamia-speech-en_20190609-1_armhf.deb
    sudo dpkg -i python-kaldiasr_0.5.2-1_armhf.deb
    sudo dpkg -i python-espeakng_0.1.5-1_all.deb 
    sudo dpkg -i python-marytts_0.1.4-1_all.deb
    sudo dpkg -i python-num2words_0.5.7-1_all.deb 
    sudo dpkg -i python-picotts_0.1.2-1_all.deb 
    sudo dpkg -i python-webrtcvad_2.0.11-4_armhf.deb 
    sudo dpkg -i python-nltools_0.5.0-1_all.deb 

# Install pulse

 This is copied from [Radiodan](https://github.com/andrewn/neue-radio/blob/master/deployment/provision)

    sudo apt-get install pulseaudio -y
    sudo adduser pi pulse
    sudo sed -i '/load-module module-native-protocol-unix/c load-module\ module-native-protocol-unix auth-anonymous=1\ socket=/tmp/pulseaudio-system.sock\nload-module module-native-protocol-tcp auth-anonymous=1 auth-ip-acl=127.0.0.1;192.168.178.0/24' /etc/pulse/system.pa
    sudo mkdir -p /home/pi/.config/pulse/
    sudo echo "default-server = unix:/tmp/pulseaudio-system.sock" >> /home/pi/.config/pulse/client.conf
    sudo chown -R pi:pi /home/pi/.config/pulse/
    sudo cp pulseaudio.service /etc/systemd/system/
    sudo systemctl enable pulseaudio

    sudo systemctl start pulseaudio
    sudo systemctl status pulseaudio

# Install respeaker stuff if using it

    sudo nano /boot/config.txt

after

    dtparam=audio=on

add

    dtoverlay=seeed-4mic-voicecard

then 

    git clone https://github.com/respeaker/seeed-voicecard.git
    cd seeed-voicecard
    sudo ./install.sh 4mic
    sudo reboot

check this there:

    arecord -l


# Test

    wget 'http://goofy.zamia.org/zamia-speech/misc/kaldi_decode_live.py'

    python kaldi_decode_live.py
    
If it crashes with `terminate called after throwing an instance of 'std::bad_alloc'` or similar, try increasing the swap size.

    /etc/dphys-swapfile

to e.g.

    CONF_SWAPSIZE=1000

# 'Fix'? the VAD (it's a tiny change, but my code doesn't work without it)

    sudo cp vad.py /usr/lib/python2.7/dist-packages/nltools/vad.py

# Install deps for kaldi_and_move.py

    pip install nltk

# start it up automatically

You'll need to edit for your own code

    sudo cp speaky.service /lib/systemd/system/
    sudo systemctl enable speaky.service 
    sudo systemctl start speaky.service
