#!/usr/bin/bash

echo ''
echo 'Remove SQLite Database'
read -r -p "Are you sure? [y/N] " response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]
then
    rm app/backend/data/requested_data.sqlite
    echo 'Done! Succesfully clear database.'
    echo ''
else
    echo 'Task canceled'
    echo ''
fi