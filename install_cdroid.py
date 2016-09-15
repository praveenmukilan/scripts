#!/usr/local/bin/python

import subprocess
import argparse
import os
import sys

HOME=os.getenv("HOME")
APK_FOLDER=HOME+"/Downloads/Debug/"
BUILD_OUTPUT_FOLDER=HOME+"/HB-Droid-Consumer/HBDroidConsumer/build/outputs/apk/"
env_d={"staging":"Staging","development":"Development","production":"Production"}
package_d={"staging":"com.honestbee.consumer.staging","development":"com.honestbee.consumer.development","production":"com.honestbee.consumer"}
APK=""

class InstallDebug(object):
    version=""
    env=""   
    def __init__(self,version,env,apk):
        self.version=version
        self.tag="REL_"+version
        self.coreTag=self.tag+"_Consumer"
        self.env=env
        self.apk=apk

    def getUdid(self):
        '''
        to return the udid of the connected device
        '''
        output = subprocess.check_output("adb devices", shell=True)
        for row in output.split('\n'):
            if ("\tdevice" in row):
                print row
                value, key = row.split('\t')
        udidl=value.strip()
        return udidl

    def gitCheckout(self,tag):
        command="git checkout development && git fetch --all && git pull && git checkout tags/"+ tag
        print command
        subprocess.check_output(command,shell=True)


    def build(self):
        print "running build"
        subprocess.check_output("GRADLE_OPTS=-Xmx1024m ./gradlew assemble"+env_d[self.env]+"Debug --stacktrace", shell=True)
        #if(self.isApkBuilt(self.version,BUILD_OUTPUT_FOLDER)):
        #subprocess.check_output("cp "+BUILD_OUTPUT_FOLDER+"/HBDroidBee-staging-v"+self.version+".apk "+APK_FOLDER, shell=True)
        subprocess.check_output("cp "+BUILD_OUTPUT_FOLDER+self.apk+" "+APK_FOLDER, shell=True)


    def gitCheckoutConsumer(self,tag):
        print "checking out bee"
        os.chdir(HOME+"/HB-Droid-Consumer")     
  #      print "Tag : "+tag
        self.gitCheckout(tag)

    def gitCheckoutCore(self,coreTag):
        print "checking out Core"
        os.chdir(HOME+"/HB-Droid-Core")
        self.gitCheckout(self.coreTag)

    def buildApk(self,version):
        #removing directories

        print "building debug apk.."
        os.chdir(HOME)
        coreTag=self.tag+"_Consumer"
        self.gitCheckoutCore(self.coreTag) 
        self.gitCheckoutConsumer(self.tag)   
        self.build()


    def uninstallApk(self,udid):
        '''
        uninstall any version of the staging apk installed already
        '''
        command="adb -s "+udid+" uninstall "+package_d[self.env]
        print command
        print "uninstalling if there are any installations already"
        output = subprocess.check_output(command, shell=True)
        print output


    def installApk(self,udid,version):            

        #install apk
        print "installing apk..."
        command = "adb -s "+udid+ " install "+APK_FOLDER+self.apk
        print "***** : "+command
        output = subprocess.check_output(command, shell=True)
        #print output
        list=output.splitlines()
        #print the status of installation
        print list[-1]

    def isApkBuilt(self,version,path):
        try:
            os.chdir(path)
            #print os.getcwd()
            output=subprocess.check_output("ls "+path+self.apk,shell=True)
            print output
            return True
        except:
            return False


    
def main():
#    print "main method"
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', dest='command', help='supported commands `install`, `build`, `uninstall` ')
    parser.add_argument('-udid', dest='udid', help='UDID of the device, if not specified, automatically runs `adb devices` to get the udid')
    parser.add_argument('-v', dest='version', help='the version of the apk to install. eg, 3.1.4.7')
    parser.add_argument('-env', dest='env', help='the environment to build `staging`, `development` , `production')
    args = parser.parse_args()
    print args

    version=args.version
    command=args.command
    #env if given, else defaults to Staging
    env=args.env if bool(args.env) else "staging"
    APK="HBDroidConsumer"
    APK=APK+"-v"+version+"-"+env+".apk"
    
    install=InstallDebug(version,env,APK)
    isBuilt = install.isApkBuilt(version,APK_FOLDER)
#    print "isBuilt? "
#    print isBuilt
    udid=udid.udid if bool(args.udid) else install.getUdid()

    if command == 'build' :
        print "expected apk :"+APK
        install.buildApk(version)
    elif command == 'install' :
        install.uninstallApk(udid)
        install.installApk(udid,version)
    elif command == 'uninstall' :
        install.uninstallApk(udid)
    else :
        if not isBuilt:
            install.buildApk(version) 
        install.uninstallApk(udid)
        install.installApk(udid,version)
    
    
if __name__ == '__main__': 
    main()
