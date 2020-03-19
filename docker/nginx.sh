#!/bin/bash

apt-get update && apt-get install -y curl vim
rm -f /etc/nginx/conf.d/default.conf