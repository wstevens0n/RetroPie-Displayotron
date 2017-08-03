# RetroPie-Displayotron
Python script for Pimoroni's Display-o-tron LCD to display system and game information.

Steps:

Git clone this folder to your /home/pi path and add the following line in the rc.local file before 'exit 0'

sudo nano /etc/rc.local
sudo python /home/pi/displayotron/retropie.py &

Move or replace the following files under /opt/retropie/configs/all
runcommand-onend.sh
runcommand-onstart.sh
