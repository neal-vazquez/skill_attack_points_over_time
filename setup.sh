#!/bin/bash

# Log the installation process
exec > >(tee -i /var/log/setup.log)
exec 2>&1

# Install Playwright browsers with dependencies
npx playwright install --with-deps
