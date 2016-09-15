#! /usr/bin/env bash

env=$2

tag=$1
#version=`echo $1 | grep -o REL_(.*)`
version=`echo $1 | sed -E 's/REL_//'`
buildOpFolder="~/HB-Droid-Consumer/HBDroidConsumer/build/outputs/apk/"
cd ~
#git clone https://github.com/honestbee/HB-Droid-Bee.git
#git clone https://github.com/honestbee/HB-Droid-Core.git

cd ~/HB-Droid-Core
coreTag=$tag"_Consumer"
echo $coreTag
git checkout development && git fetch --all && git pull && git checkout tags/$coreTag

cd ~/HB-Droid-Consumer
git checkout development && git fetch --all && git pull && git checkout tags/$tag

GRADLE_OPTS=-Xmx1024m ./gradlew assembleStagingDebug --stacktrace
cp "${buildOpFolder}"*$version* ~/Downloads/Debug
GRADLE_OPTS=-Xmx1024m ./gradlew assembleDevelopmentDebug --stacktrace
cp "${buildOpFolder}"*$version* ~/Downloads/Debug
#cp ~/HB-Droid-Bee/HBDroidBee/build/outputs/apk/*$version* ~/Downloads/Debug
GRADLE_OPTS=-Xmx1024m ./gradlew assembleProductionDebug --stacktrace
cp "${buildOpFolder}"*$version* ~/Downloads/Debug
#cp ~/HB-Droid-Bee/HBDroidBee/build/outputs/apk/*$version* ~/Downloads/Debug

