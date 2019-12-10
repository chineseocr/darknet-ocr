git clone https://github.com/pjreddie/darknet.git ../darknet
cp network.c ../darknet/src/network.c
cp Makefile ../darknet
cd ../darknet && make