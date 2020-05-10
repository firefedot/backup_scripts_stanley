#!/bin/bash

timestamp(){
  date +%Y-%m-%d" "%X,%3N
}

if [[ ! -z $1 ]]
then 
    USER_BK=$1
    if [[ $USER_BK == 'srisovki' ]]
        then
	    DB_NAME="vse"$USER_BK"db"
	else
	    DB_NAME=$USER_BK"db"
	fi
    DB_USER=$USER_BK"us"
else
    echo "$(timestamp) Please read username"
    exit 1
fi

DB_HOST="localhost"
DB_PORT="5432"
CURRENT_DATE=`date +%Y-%m-%d`
BACKUP_PATH=$HOME/yandex/backup/$USER_BK #/$CURRENT_DATE
BACKUP_FILE_DBNAME=$DB_NAME-$CURRENT_DATE.backup
BACKUP_FILES_DIR='files'

HOME_USER="/home/$USER_BK"
USER_WWW=$HOME_USER/"www"
EXCLUDE_DIR="site/media/CACHE"

KEEP_BACKUP_DAYS=10
KEEP_BACKUP_YESTERDAY=1
BACKUP_YESTERDAY_DATE=`date +%F --date="$BACKUP_YESTERDAY_DATE days ago"`
FS_ZIP=$BACKUP_PATH/files-$CURRENT_DATE.tar.gz

log="$HOME/_log/$USER_BK"_"`echo $0 | rev | cut -d/ -f1 | cut -c 4- | rev`.log"
logerr="$HOME/_log/$USER_BK"_"`echo $0 | rev | cut -d/ -f1 | cut -c 4- | rev`_error.log"

echo "$(timestamp) Backup DB $DB_NAME for user $DB_USER"
echo "$(timestamp) Create backup dir $BACKUP_PATH"
mkdir -p $BACKUP_PATH
set -e
pg_dump --verbose -h $DB_HOST -F c -U $DB_USER -f $BACKUP_PATH/$BACKUP_FILE_DBNAME $DB_NAME > $logerr 2>&1
set +e

echo "$(timestamp) Backup folders user:$USER_BK"

echo "$(timestamp)" "Backup filestorage $FS_ZIP"
cd $USER_WWW
# use parametr -p for save permissions
tar --exclude=$EXCLUDE_DIR -czf $FS_ZIP .

echo "$(timestamp)" "Delete old backups"
find $BACKUP_PATH -mtime +$KEEP_BACKUP_DAYS -exec rm -rfv {} \;


