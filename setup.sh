#!/bin/bash

# Log the installation process to a log file
exec > >(tee -i /tmp/setup.log)
exec 2>&1

# Set Node.js version
NODE_VERSION=18.4.0
NODE_DISTRO=linux-x64

# Create a local installation directory
mkdir -p $HOME/local/nodejs

# Download and extract Node.js
curl -o node-v$NODE_VERSION-$NODE_DISTRO.tar.xz https://nodejs.org/dist/v$NODE_VERSION/node-v$NODE_VERSION-$NODE_DISTRO.tar.xz
tar -xJf node-v$NODE_VERSION-$NODE_DISTRO.tar.xz -C $HOME/local/nodejs --strip-components=1

# Add Node.js to PATH
export PATH=$HOME/local/nodejs/bin:$PATH

# Verify installation
node -v
npm -v

# Install Playwright browsers with dependencies locally
npx playwright install --with-deps