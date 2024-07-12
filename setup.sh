#!/bin/bash

# Log the installation process to a log file
exec > >(tee -i /tmp/setup.log)
exec 2>&1

# Install Node.js and npm if not installed
if ! command -v node &> /dev/null
then
    curl -sL https://deb.nodesource.com/setup_14.x | bash -
    apt-get install -y nodejs
fi

# Install Playwright browsers with dependencies
npx playwright install --with-deps