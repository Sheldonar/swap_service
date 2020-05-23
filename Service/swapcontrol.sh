#!/bin/bash

trap recieveSignal SIGUSR1

function recieveSignal {
	echo 'SIGUSR1 signal was recieved!'
	createFile $NEW_SWAPFILE $DOUBLE_MEM 
}

function createFile {
        echo 'Creating swap file...'
        dd if=/dev/zero of=/$1 bs=1M count=$2
        chmod 600 /$1
        mkswap /$1
        swapon /$1
        echo /$1 'none swap defaults 0 0' >> /etc/fstab
        echo 'Swap file was created: ' `swapon | tail -n1`
}

function expandSpace {
        #parse swap file size and amount of USED mem
        SIZE=`swapon -s | tail -n1 | awk '{print +$3}'`
        USED=`swapon -s | tail -n1 | awk '{print +$4}'`

	#create new file name
        COUNT=$((`swapon | wc -l` - 1))
        NEW_SWAPFILE=swapfile$COUNT

        HALF_MEM=$((SIZE / 2))
        #convert to MB
        DOUBLE_MEM=$(((SIZE + 4) / 512))
        echo $DOUBLE_MEM

        #if file is more than half full
	if [ $USED -gt $HALF_MEM ]
        then
            	echo 'Swap file is more than half full. Creating another file...'
                creatFile $NEW_SWAPFILE $DOUBLE_MEM
        fi
}


while true
do
  	#check if swapfile exist
	grep -q "swapfile" /etc/fstab

        #if not then create
        if [ $? -ne 0 ]
        then
            	echo 'Swap file not found'
                createFile swapfile 512
        else
            	expandSpace
        fi
        sleep 30
done




