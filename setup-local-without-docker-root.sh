#!/bin/bash
# Run as root!
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list

apt-get update && apt-get install -y wget gnupg2 lsof apt-transport-https ca-certificates x11-utils xdg-utils xvfb software-properties-common python3-pip google-chrome-stable pipx

pipx install virtualenv
