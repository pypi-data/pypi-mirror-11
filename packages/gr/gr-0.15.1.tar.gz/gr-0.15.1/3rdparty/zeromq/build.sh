#!/bin/sh

src="zeromq-4.0.4"
if [ "$1" = "" ]; then
  dest=`pwd`/../build
else
  dest=$1
fi

curl -O http://download.zeromq.org/zeromq-4.0.4.tar.gz

tar xf ${src}.tar.gz

cd ${src}

export CFLAGS=-fPIC
export CXXFLAGS=-fPIC
./configure --prefix=${dest} --disable-shared
make -j4
make install
make distclean

cd ..

rm -rf ${src} *.tar.gz

