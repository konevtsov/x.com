#!/bin/sh

set -e 

for dir in infrastructure x-auth-service x-user-service x-post-service
do 
  (cd "$dir" && docker compose up -d)
done

echo "Done!"