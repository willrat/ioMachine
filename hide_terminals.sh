#!/bin/bash

WIDS=`xdotool search --classname "gnome-terminal"`
for id in $WIDS; do
  #xdotool windowsize $id 500 500
  xdotool windowminimize $id
done
