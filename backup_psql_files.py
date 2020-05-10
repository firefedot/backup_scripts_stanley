#!/usr/bin/python3

import sys

if len(sys.argv) > 1:
    user_bk = sys.argv[1]
    if user_bk == 'srisovki':
        db_name = f'vse{user_bk}db'
    else:
        db_name = f'{user_bk}db'
    db_user = f'{user_bk}us'
else:
    sys.exit("Error: less argv, you mast write argv username")

print(f'Begin backup process for {user_bk} , db_name: {db_name}, db_user: {db_user}')

