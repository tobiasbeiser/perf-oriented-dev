killall io_loadgen &> /dev/null
../build/io_loadgen 100 10000 1 1 &> /dev/null &
../build/io_loadgen 100 10000 1 1 &> /dev/null &
../build/io_loadgen 100 10000 1 1 &> /dev/null &
../build/io_loadgen 100 10000 1 1 &> /dev/null &
../build/io_loadgen 100 10000 1 1 &> /dev/null &
#time -p nice -n 100 $1
nice -n 1000 $1
killall io_loadgen &> /dev/null
