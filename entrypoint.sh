#!/bin/bash

# Start Scrapyd in the background
scrapyd &

# Deploy the Scrapy project to Scrapyd
scrapyd-deploy default

# Keep the container running
tail -f /dev/null