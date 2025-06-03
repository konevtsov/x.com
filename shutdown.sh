#!/bin/sh

set -e

for dir in infrastructure x-auth-service x-user-service x-post-service
do
  (
    cd "$dir"
    docker compose down
  )
done

echo "Done!"
