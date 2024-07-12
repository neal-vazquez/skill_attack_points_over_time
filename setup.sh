#!/bin/bash

# Install Node.js and npm
curl -sL https://deb.nodesource.com/setup_14.x | bash -
apt-get install -y nodejs

# Install Playwright browsers with dependencies
npx playwright install --with-deps
