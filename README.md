# backup_scripts_stanley
backup psql 12 any dbs, files users

---

#### Начало работы

Для успешного выполнения backup_psql_files.py не обходим файл config.py,
в котором указаны параметры для отправки почты и другие конфиденциальные данные.
Файл config.py не отправляется в гит (.gitignore)

example config.py:

    smtp_server = "smtp.yandex.ru"
    smtp_port = 587
    smtp_login = 'LOGIN'
    smtp_passwd = 'PASSWD'
    smtp_fromaddr = 'you-from_mail@ya.ru'
    smtp_toaddr = ['one-mail@mail.ru', 'test@ya.ru']
    smtp_msg = "\r\n".join([
         f"From: {smtp_fromaddr}",
         f"To: {', '.join(map(str,smtp_toaddr))}",
         "Subject: Backup complete",
         "",
         str('Every day backup completed is successfuly')
    ])
    
- smtp_server  - адрес smtp сервера
- smtp_port - порт smtp сервера
- smtp_login - логин для почты
- smtp_passwd - пароль для почты
- smtp_fromaddr - имя ящика, с которого отправляется почта
- smtp_toaddr - список адресов, на которые должно отправиться письмо
- smtp_msg - тест сообщения, для редактирования Subject и str(), остальные параметры автоматически применяеются

#### Как работает

Скрипт принимает на вход имя пользователя системы, данные которого нобходимо архивировать.
Для успешной работы скрипта, без дописания "костылей", именя польозвателя, 
логина входа в базу и имя базы должны быть составлены следующим образом:

    Имя пользователя системы: raskraski
    Имя пользователя базы данные: raskrasius - добавился постфикс "us"
    Имя базы данных этого пользователя: raskrasiusdb - добавился постфикс "db"

Скрипт работает от "основного" пользователя, например stanley.
Для безпроблемного бекапа базы, требуется создать файл .pgpass с правами 600,
в домашней директории "основного пользователя" (/home/stanley/.pgpass) 
https://postgrespro.ru/docs/postgrespro/12/libpq-pgpass

Все бекапы храняться на ЯДиске.

Установка ядиска:

https://yandex.ru/support/disk-desktop-linux/
    
    echo "deb http://repo.yandex.ru/yandex-disk/deb/ stable main" | sudo tee -a /etc/apt/sources.list.d/yandex-disk.list > /dev/null && wget http://repo.yandex.ru/yandex-disk/YANDEX-DISK-KEY.GPG -O- | sudo apt-key add - && sudo apt update && sudo apt install -y yandex-disk
    yandex-disk setup # - запустит настройку
    
    # Отвечая на вопросы, указать директорию монтирования $HOME/yandex,
    # и разрешить автомонтирование
    

Для запуска по расписанию использовать cron.

    crontab -e # от имени "основого пользователя"
    
    0 3	* * * $HOME/_scripts/backup_psql_files srisovki >> $HOME/_log/srisovki_backup_psql.log 2>&1
    0 4	* * * $HOME/_scripts/backup_psql_files raskraski >> $HOME/_log/raskraski_backup_psql.log 2>&1

Требуется директория $HOME/_log - создается скриптом, при первом запуске

Все действия логируются в фвйл USER_BK_backup_psql.log
В файл USER_BK_backup_psql_error.log - пишутся логи pg_dump - особенность pg_dump


#### Возможные проблемы

на версии Python3.7 может не работать exсlude у модуля tarfile
https://github.com/PipelineAI/pipeline/issues/294

На версии < 3.6.9 работает