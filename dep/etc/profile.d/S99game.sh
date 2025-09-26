#!/bin/sh

export LANG=en_US.UTF-8
stty iutf8 -F /dev/console
export PATH=$PATH:/oem/pkpy/

clear > /dev/console
echo "Starting..." > /dev/console
sleep 1.5
/bin/sh -c "/root/term_start_all.sh" > /dev/console
