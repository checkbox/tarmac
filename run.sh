#!/bin/sh

while true; do
    echo "-- STARTING NEW MERGE RUN --"
    PYTHONPATH=. ./bin/tarmac merge -v -d
    #echo "-- ABOUT TO SUSPEND FOR 60 MINUTES --"
    #for i in $(seq 1 60); do
    #    echo $i
    #    sleep 1
    #done
    #sudo rtcwake --mode mem --seconds 3600    
    echo "-- SLEEPING FOR 60 MINUTES --"
    sleep 3600
done
