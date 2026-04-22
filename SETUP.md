# Kaamgar Connect – Complete Setup Guide
## Django + HTML/CSS/JS + MySQL

### 1. Install Dependencies
```bash
pip install django==4.2 mysqlclient pillow
```

### 2. MySQL Database Setup
```sql
CREATE DATABASE kaamgar_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Update `kaamgar_connect/settings.py` — uncomment MySQL block and set your password.

### 3. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 4. Run Dev Server
```bash
python manage.py runserver
```
Visit: http://127.0.0.1:8000/

### 5. For SQLite (quick local test)
The settings.py already has SQLite configured. Just run migrations directly.

### MySQL SQL Setup
```sql
CREATE DATABASE kaamgar_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'kaamgar_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON kaamgar_db.* TO 'kaamgar_user'@'localhost';
FLUSH PRIVILEGES;
```
