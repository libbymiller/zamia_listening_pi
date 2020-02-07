# Zamia on a Pi 3

Zamia a a version of Kaldi - speech to text
This is a how-to for making it work on a pi 3
I used python 2.7 - not tried with python 3 yet.
To make it work it really needs a good microphone.

http://goofy.zamia.org/

# Install Zamia

Dependencies - https://github.com/alexylem/jarvis/issues/129#issuecomment-248072872

    curl -O http://ftp.fr.debian.org/debian/pool/non-free/s/svox/libttspico-data_1.0+git20130326-3_all.deb
    curl -O http://ftp.fr.debian.org/debian/pool/non-free/s/svox/libttspico0_1.0+git20130326-3_armhf.deb
    curl -O http://ftp.fr.debian.org/debian/pool/non-free/s/svox/libttspico-utils_1.0+git20130326-3_armhf.deb

    sudo dpkg -i libttspico-data_1.0+git20130326-3_all.deb
    sudo dpkg -i libttspico0_1.0+git20130326-3_armhf.deb
    sudo dpkg -i libttspico-utils_1.0+git20130326-3_armhf.deb

As root:

    echo "deb http://goofy.zamia.org/repo-ai/raspbian/stretch/armhf/ ./" >/etc/apt/sources.list.d/zamia-ai.list
    wget -qO - http://goofy.zamia.org/repo-ai/raspbian/stretch/armhf/bofh.asc | sudo apt-key add -
    apt-get update
    apt-get install kaldi-chain-zamia-speech-de kaldi-chain-zamia-speech-en python-kaldiasr python-nltools pulseaudio-utils pulseaudio
    apt-get install kaldi-chain-zamia-speech-en python-kaldiasr python-nltools pulseaudio-utils pulseaudio

# Install pulse

    This is copied from Radiodan https://github.com/andrewn/neue-radio/blob/master/deployment/provision

    apt-get install pulseaudio -y
    echo "*** Pulse Audio system mode"
    adduser pi pulse
    sed -i '/load-module module-native-protocol-unix/c load-module\ module-native-protocol-unix auth-anonymous=1\ socket=/tmp/pulseaudio-system.sock\nload-module module-native-protocol-tcp auth-anonymous=1 auth-ip-acl=127.0.0.1;192.168.178.0/24' /etc/pulse/system.pa

    mkdir -p /home/pi/.config/pulse/
    echo "default-server = unix:/tmp/pulseaudio-system.sock" >> /home/pi/.config/pulse/client.conf
    chown -R pi:pi /home/pi/.config/pulse/
    cp pulseaudio.service /etc/systemd/system/
    systemctl enable pulseaudio

    sudo systemctl start pulseaudio
    sudo systemctl status pulseaudio

# Install respeaker stuff

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

# 'Fix'? the VAD (it's a tiny change, but doesn't work without it)

    sudo cp vad.py /usr/lib/python2.7/dist-packages/nltools/vad.py

# Install deps

    pip install nltk


# start it up automatically

You'll need to edit for your own code

    sudo cp speaky.service /lib/systemd/system/
    sudo systemctl enable speaky.service 
    sudo systemctl start speaky.service
