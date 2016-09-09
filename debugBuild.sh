#! /usr/bin/env bash

env=$2

tag=$1
#version=`echo $1 | grep -o REL_(.*)`
version=`echo $1 | sed -E 's/REL_//'`

cd ~
#git clone https://github.com/honestbee/HB-Droid-Bee.git
#git clone https://github.com/honestbee/HB-Droid-Core.git

cd ~/HB-Droid-Core
coreTag=$tag"_bee"
echo $coreTag
git checkout development && git fetch --all && git pull && git checkout tags/$coreTag

cd ~/HB-Droid-Bee
git checkout development && git fetch --all && git pull && git checkout tags/$tag

GRADLE_OPTS=-Xmx1024m ./gradlew assembleStagingDebug --stacktrace
cp ~/HB-Droid-Bee/HBDroidBee/build/outputs/apk/*$version* ~/Downloads/Debug
GRADLE_OPTS=-Xmx1024m ./gradlew assembleDevelopmentDebug --stacktrace
cp ~/HB-Droid-Bee/HBDroidBee/build/outputs/apk/*$version* ~/Downloads/Debug
GRADLE_OPTS=-Xmx1024m ./gradlew assembleProductionDebug --stacktrace
cp ~/HB-Droid-Bee/HBDroidBee/build/outputs/apk/*$version* ~/Downloads/Debug




