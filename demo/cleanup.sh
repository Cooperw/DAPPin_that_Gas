#! /bin/bash

for x in $(ps -aux | grep "meterpreter" | tr -s ' ' | cut -d ' ' -f 2); do kill -9 $x; done
rm ./linux_x*
