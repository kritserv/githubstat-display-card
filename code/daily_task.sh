#!/usr/bin/bash

echo ''
python --version
echo '...'
echo ''
python app/backend/function/daily_database_updater.py
echo ''
echo 'Done!'