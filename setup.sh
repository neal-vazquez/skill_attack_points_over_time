#!/bin/bash

# Log the installation process to a log file
exec > >(tee -i /tmp/setup.log)
exec 2>&1

# Install Node.js 18.x and npm locally if not installed
if ! command -v node &> /dev/null
then
    curl -sL https://deb.nodesource.com/setup_18.x | bash -
    mkdir -p $HOME/local/bin
    tar -xJf node-v18.*-linux-x64.tar.xz -C $HOME/local --strip-components=1
    export PATH=$HOME/local/bin:$PATH
fi

# Install Playwright browsers with dependencies locally
npx playwright install --with-deps