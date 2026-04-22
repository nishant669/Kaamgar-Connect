-- Kaamgar Connect MySQL Setup
CREATE DATABASE IF NOT EXISTS kaamgar_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'kaamgar_user'@'localhost' IDENTIFIED BY 'KaamgarPass@2025';
GRANT ALL PRIVILEGES ON kaamgar_db.* TO 'kaamgar_user'@'localhost';
FLUSH PRIVILEGES;
USE kaamgar_db;
-- Run: python manage.py migrate  (after configuring settings.py)
