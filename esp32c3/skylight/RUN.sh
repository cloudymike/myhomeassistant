#!/bin/bash


usage ()
{
  echo "USAGE: $0 options"
  echo "-c     Only update config"
  echo "-m     Only update main"
  echo "-h     Help"
  echo "-i     IP of mosquitto server"
  echo "-P     Port to use for USB connection, default: $PORT"
  exit 0
}

IP=""
USBPORT=""
MAINONLY=false
CONFIGONLY=false
while getopts "cim:h" arg; do
  case $arg in
    c)
      CONFIGONLY=true
      ;;
    h)
      usage
      ;;
    i)
      IP=$OPTARG
      ;;
    m)
      MAINONLY=true
      ;;
    P)
      USBPORT=$OPTARG
      ;;
    *) usage
    ;;
  esac
done



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

if (! $MAINONLY)
then

  echo loading configs
  # Enter your path to your WLAN configuration file here, see ../wlan/wlanconfig.py for example
  $PUSHCMD ~/secrets/wlanconfig.py

  # This is to get the mosquitto host IP address
  cp ../../config/config.py mqtthost.py
  if [ "$IP" = "" ]
  then
  	echo "MQTT_HOST='$(hostname -I | awk '{print $1}')'" >>mqtthost.py
  else
  	echo "MQTT_HOST='$IP'" >>mqtthost.py
  fi
  cat mqtthost.py
  $PUSHCMD mqtthost.py
fi

if (! $CONFIGONLY)
then
  if (! $MAINONLY)
  then
    echo loading mha
    $PUSHCMD $TOPDIR/mha
    echo loading other libraries
    $PUSHCMD $UPYDIR/wlan/wlan.py
    $PUSHCMD $UPYDIR/LED/LED.py
  fi

  echo loading main
  $PUSHCMD main.py
fi

echo "Resetting board"
timeout 2  ampy --port $PORT run $UPYDIR/reset/reset.py
