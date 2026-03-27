#!/usr/bin/env sh

echo "Pulling latest images..."
docker compose pull

echo "Starting up docker containers..."
docker compose up -d

echo "Deleting old sites and config..."
rm -v /etc/nginx/sites-available/* /etc/nginx/nginx.conf /etc/nginx/sites-enabled/*

echo "Copying latest sites..."
cp -v nginx/sites/* /etc/nginx/sites-available/.

echo "Enabling sites..."
ln -sv /etc/nginx/sites-available/* /etc/nginx/sites-enabled/.

echo "Copying the latest nginx.conf..."
cp -v nginx/nginx.conf /etc/nginx/.

echo "Checking syntax and restarting nginx if all're ok..."
nginx -t && systemctl restart nginx

