#!/bin/bash
xgettext -d machine -o locale/machine.pot \
			gui1.py \
			storable.py \
			keyboard.py \
			motionProgram.py \
			gui1.glade
