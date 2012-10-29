#!/bin/bash

if [ -e /dev/ttyUSB0 ] 
then
    sudo inputattach -elo /dev/ttyUSB0 --daemon
    sleep 1
    xinput set-int-prop "Elo Serial TouchScreen" "Evdev Axis Calibration" 32 370 3523 3585 512
fi

