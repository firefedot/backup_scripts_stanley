#!/bin/bash

if [[ ! -z $1 ]]
then 
    USER_BK=$1
    DB_NAME=$USER_BK"db"
    DB_USER=$USER_BK"us"
else
    echo "Please read username"
    exit 1
fi

DB_HOST="localhost"
DB_PORT="5432"
CURRENT_DATE=`date +%Y-%m-%d`
BACKUP_PATH=$HOME/yandex/backup/$USER_BK/$CURRENT_DATE
BACKUP_FILE_NAME=$DB_NAME-$CURRENT_DATE.backup

log="$HOME/_log/$USER_BK"_"`echo $0 | rev | cut -d/ -f1 | cut -c 4- | rev`.log"
logerr="$HOME/_log/$USER_BK"_"`echo $0 | rev | cut -d/ -f1 | cut -c 4- | rev`_error.log"

echo "Backup DB $DB_NAME for user $DB_USER"
echo "Create backup dir $BACKUP_PATH"
mkdir -p $BACKUP_PATH
set -e
pg_dump --verbose -h $DB_HOST -F c -U $DB_USER -f $BACKUP_PATH/$BACKUP_FILE_NAME $DB_NAME > $logerr 2>&1
set +e

echo "Backup folders user:$USER_BK"

