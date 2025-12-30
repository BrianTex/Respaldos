Creacion de la base de datos en MariaDB

CREATE DATABASE remotebackup_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE USER 'remotebackup_user'@'localhost' IDENTIFIED BY 'R3m0t3B4ckUp';

GRANT ALL PRIVILEGES ON remotebackup_db.* TO 'remotebackup_user'@'localhost';

FLUSH PRIVILEGES;

EXIT;
