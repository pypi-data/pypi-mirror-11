
P1=$1
P2=$2

echo $P1 $P2

runme(){
    port=$1
    fifo="/tmp/fifo.$port"
    rm -rf $fifo
    mkfifo $fifo
    echo "run on port $port"
    nc -l -p $port <$fifo | /bin/sh /tmp/spawner.sh /tmp/e1/ >$fifo
}

(runme $P1) &
(runme $P2) 

