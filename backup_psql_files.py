#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import datetime
import os
import subprocess
import tarfile
import smtplib
# this import config file
from config import *


# function timestamp
def timestamp():
    return datetime.datetime.now()


# checking less args
if len(sys.argv) > 1:
    user_bk = sys.argv[1]
    if user_bk == 'srisovki':
        db_name = f'vse{user_bk}db'
    else:
        db_name = f'{user_bk}db'
    db_user = f'{user_bk}us'
else:
    sys.exit(f"{timestamp()} Error: less argv, you mast write argv username")


# function send email
def send_email(email_text):
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.ehlo()
    server.starttls()
    server.login(smtp_login, smtp_passwd)
    server.sendmail(smtp_fromaddr, smtp_toaddr, email_text)
    server.quit()
    print(f'{timestamp()} Send mail compete')


# define vars
script_name = os.path.basename(__file__).split('.')[0]
home_path = '/home/stanley'
db_host = 'localhost'
db_port = 5432
current_date = datetime.date.today().strftime('%Y-%m-%d')
backup_path = f'{home_path}/yandex/backup'
backup_path_user = f'{home_path}/yandex/backup/{user_bk}'
backup_file_dbname = f'{db_name}-{current_date}.backup'


if not os.path.exists(backup_path):
    print(f'{timestamp()} Send email - failed backup')
    send_email(smtp_msg_error)
    sys.exit(f"{timestamp()} Error: {backup_path} is absent")


home_user = f'/home/{user_bk}'
user_www = f'{home_user}/www'
exclude_dir = ["./site/media/CACHE", f"./venv_{user_bk}", "./.git", "./.gitignore"]

keep_backup_day = 3
keep_backup_yesterday = 1
fs_zip = f'{backup_path_user}/files-{current_date}.tar.gz'

log_dir = f'{home_path}/_log'
log = f'{log_dir}/{script_name}.log'
logerr = f'{log_dir}/{script_name}_error.log'

# create logging dir
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
    print(f'{timestamp()} Create logging dir {log_dir} - complete')


# Backup databases
print(f'{timestamp()} Begin backup process for {user_bk} , db_name: {db_name}, db_user: {db_user}, {datetime.datetime.now()} ')
print(f'{timestamp()} Backup Database: {db_name}, userdb: {db_user}')
print(f'{timestamp()} Create {backup_path}')

if not os.path.exists(backup_path_user):
    os.makedirs(backup_path_user)
    print(f'{timestamp()} Create folder {backup_path_user} - complete')

pg_dump = f'pg_dump --verbose -h {db_host} -F c -U {db_user} -f {backup_path_user}/{backup_file_dbname} {db_name}'
pg_dump_run = subprocess.run(pg_dump, shell=True, stderr=subprocess.PIPE, encoding='utf-8')
# write output pg_dump into file
with open(logerr, 'w') as logerr_file:
    logerr_file.write(pg_dump_run.stderr)
print(f'{timestamp()} Backup db {db_name} complete!')
print(f'{timestamp()} Backup filestorage {fs_zip} complete!')


# archive filestorage to tar.gz
# exclude dir
def excludes_fn(name):
    if name in exclude_dir:
        print(f'Exclude: {name}')
        return True
    else:
        return False


os.chdir(user_www)
with tarfile.open(fs_zip, 'w:gz') as tar:
    tar.add('.', exclude=excludes_fn)

# remove old files
for dirpath, dirnames, filenames in os.walk(backup_path_user):
    for file in filenames:
        curpath = os.path.join(dirpath, file)
        file_modified = datetime.datetime.fromtimestamp(os.path.getmtime(curpath))
        if datetime.datetime.now() - file_modified > datetime.timedelta(days=keep_backup_day):
            os.remove(curpath)
            print(f'{timestamp()} file {curpath} removed')

# send email if script success complete
print(f'{timestamp()} Send email')

send_email(smtp_msg)
