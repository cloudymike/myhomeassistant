#!/bin/bash


USBPORT=$(ls /dev/ | grep -e ACM)
if [ "$USBPORT" = "" ]
then
USBPORT=$(ls /dev/ | grep -e USB)
fi
PORT=/dev/$USBPORT
echo Port used $PORT

PUSHCMD="ampy --port $PORT put "

CURDIR=$(pwd)
TOPDIR=${CURDIR%/*}
UPYDIR=$TOPDIR/micropythonexamples/ESP32C3

echo loading configs
# Enter your path to your WLAN configuration file here, see ../wlan/wlanconfig.py for example
$PUSHCMD ~/secrets/wlanconfig.py

# This is just to get the host IP address, you may have to change it
cp ../../config/config.py mqtthost.py
echo "MQTT_HOST='$(hostname -I | awk '{print $1}')'" >>mqtthost.py
$PUSHCMD mqtthost.py

echo loading mha
$PUSHCMD $TOPDIR/mha

echo loading other libraries
$PUSHCMD $UPYDIR/wlan/wlan.py

echo loading main
$PUSHCMD main.py

echo "Resetting board"
timeout 2  ampy --port $PORT run $UPYDIR/reset/reset.py
