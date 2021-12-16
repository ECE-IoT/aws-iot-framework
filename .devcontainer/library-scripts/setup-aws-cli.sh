#!/usr/bin/env bash
#-------------------------------------------------------------------------------------------------------------
# description: Basic setup script for enabling full potential for devloping iot an framework with aws
# autho: Tim Schmid
#-------------------------------------------------------------------------------------------------------------

HOME="/home/iot"
SETUP_PATH="$HOME/framework/.devcontainer/library-scripts"
AWS_PATH="/usr/local/bin/aws"


# Get AWS CLI
if [[ ! -f "${HOME}/awscli2.zip" ]];then
    if [[ ! -d "${AWS_PATH}" ]];then
        echo "Install AWS CLI"
        curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "${HOME}/awscli2.zip"
        unzip "${HOME}/awscli2.zip" -d "${HOME}"
        sudo "${HOME}/aws/install"
        echo "DONE!"
        echo "REMOVING INSTALLATION FILES"
        sudo rm -rf "${HOME}/awscli2.zip"
        sudo rm -rf "{HOME}/aws"
    fi
fi
