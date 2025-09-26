#!/bin/sh

# 1.Auto update
/usr/local/bin/copy_file.sh > /dev/console

# 2.Start Color test
sleep 1
clear > /dev/console
/usr/bin/color_test_c > /dev/console

# 3.Game
echo "Start game file..." > /dev/console
 
