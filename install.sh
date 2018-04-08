#!/bin/bash

if [[ $1 == "install" ]] ; then
    ###### INSTALL ALL REQUIRED PROGRAMS
    if [[ $OSTYPE == "linux-gnu" ]] ; then
        # Probably on ubuntu, do the ubuntu specific stuff here

        sudo apt-get install python3
        sudo apt install python3-pip

        sudo pip3 install --upgrade pip

        # echo '\033[94m finished upgrading pip \033[0m'
        #install Mongodb for ubuntu
        sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2930ADAE8CAF5059EE73BB4B58712A2291FA4AD5
        echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.6 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.6.list
        sudo apt-get update
        sudo apt-get install -y mongodb-org

        #Pin the current mongo version to prevent upgrades
        echo "mongodb-org hold" | sudo dpkg --set-selections
        echo "mongodb-org-server hold" | sudo dpkg --set-selections
        echo "mongodb-org-shell hold" | sudo dpkg --set-selections
        echo "mongodb-org-mongos hold" | sudo dpkg --set-selections
        echo "mongodb-org-tools hold" | sudo dpkg --set-selections

        # make sure we can unzip the models
        sudo apt-get install zip
        sudo apt-get install unzip

    elif [[ $OSTYPE == "darwin"* ]] ; then # Probably on osx, do the osx specific stuff here
        brew update
        brew upgrade

        brew install mongodb 
        brew install python3 #also installs pip3

    fi


    # ensure the mongo data directory exists and we have permissions
    sudo mkdir -p /data/db
    sudo chown -R `id -un` /data/db

    #create the various directories used by the program
    mkdir logs
    # mkdir ai/data
    # mkdir ai/output
    # mkdir ai/output_test

    # install all the required python libraries
    sudo pip3 install -r requirements.txt

    sudo pip3 install awscli

    #move the aws credentials file to where boto and the awscli can see it
    sudo mkdir ~/.aws
    sudo cp -a aws/. ~/.aws/


elif [[ $1 == "data" ]] ; then
    echo "loading blacklist"
    # do a thing
    python3 blacklist.py

elif [[ $1 == "run" ]] ; then
    echo "Starting Mongo..."
    mongod --fork --logfile logs/mongo.log

    echo "Starting Flask..."
    export FLASK_APP=server.py  export FLASK_DEBUG=1
    nohup flask run --host=0.0.0.0 &> logs/flask.log &


else
    echo "Invalid Argument"

fi