#!/bin/sh

set -e

for dir in infrastructure x-auth-service x-user-service x-post-service
do
  (
    cd "$dir"
    if docker compose ps -q | grep -q .; then
      docker compose restart
    else
      docker compose up -d
    fi
    sleep 2
  )
done

echo "Done!"

