#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import datetime
import os
import subprocess
import tarfile

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

script_name = os.path.basename(__file__).split('.')[0]
home_path = '/home/stanley'
db_host = 'localhost'
db_port = 5432
current_date = datetime.date.today().strftime('%Y-%m-%d')
backup_path = f'{home_path}/yandex/backup/{user_bk}'
backup_file_dbname = f'{db_name}-{current_date}.backup'


home_user = f'/home/{user_bk}'
user_www = f'{home_user}/www'
exclude_dir = "site/media/CACHE"


keep_backup_day = 3
keep_backup_yesterday = 1
fs_zip = f'{backup_path}/files-{current_date}.tar.gz'

log_dir = f'{home_path}/_log'
log = f'{log_dir}/{script_name}.log'
logerr = f'{log_dir}/{script_name}_error.log'

print(f'{timestamp()} Backup Database: {db_name}, userdb: {db_user}')
print(f'{timestamp()} Create {backup_path}')

if not os.path.exists(backup_path):
    os.makedirs(backup_path)
    print(f'{timestamp()} Create folder {backup_path} - complete')

pg_dump = f'pg_dump --verbose -h {db_host} -F c -U {db_user} -f {backup_path}/{backup_file_dbname} {db_name}'
pg_dump_run = subprocess.run(pg_dump, shell=True, stderr=subprocess.PIPE, encoding='utf-8')
# write output pg_dump into file
with open(logerr, 'w') as logerr_file:
    logerr_file.write(pg_dump_run.stderr)
print(f'{timestamp()} Backup db {db_name} complete!')
print(f'{timestamp()} Backup filestorage {fs_zip} complete!')


def excludes_fn(name):
    return exclude_dir in name


os.chdir(user_www)
with tarfile.open(fs_zip, 'w:gz') as tar:
    tar.add('.', exclude=excludes_fn)

# remove old files
for dirpath, dirnames, filenames in os.walk(user_www):
    for file in filenames:
        curpath = os.path.join(dirpath, file)
        file_modified = datetime.datetime.fromtimestamp(os.path.getmtime(curpath))
        if datetime.datetime.now() - file_modified > datetime.timedelta(days=keep_backup_day):
            # os.remove(curpath)
            print(f'remove {curpath}')
        else:
            print('all files fresh')
