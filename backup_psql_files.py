#!/usr/bin/python3

import sys
import datetime
import os

if len(sys.argv) > 1:
    user_bk = sys.argv[1]
    if user_bk == 'srisovki':
        db_name = f'vse{user_bk}db'
    else:
        db_name = f'{user_bk}db'
    db_user = f'{user_bk}us'
else:
    sys.exit("Error: less argv, you mast write argv username")


def timestamp():
    return datetime.datetime.now()


print(f'{timestamp()} Begin backup process for {user_bk} , db_name: {db_name}, db_user: {db_user}, {datetime.datetime.now()} ')

home_path = '/home/stanley'
db_host = 'localhost'
db_port = 5432
current_date = datetime.date.today().strftime('%Y-%m-%d')
backup_path = f'{home_path}/yandex/backup/{user_bk}'
BACKUP_FILE_DBNAME=f'{db_name}-{current_date}.backup'


home_user = f'/home/{user_bk}'
USER_WWW=f'{home_user}/www'
exclude_dir = "site/media/CACHE"


keep_backup_day = 10
keep_backup_yesterday = 1
FS_ZIP = f'{backup_path}/files-{current_date}.tar.gz'

log = ''
logerr = ''

print(f'{timestamp()} Backup Database: {db_name}, userdb: {db_user}')
print(f'{timestamp()} Create {backup_path}')

if not os.path.exists(backup_path):
    os.makedirs(backup_path)
    print(f'{timestamp()} Create folder {backup_path} - complete')

