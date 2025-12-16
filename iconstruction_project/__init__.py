import os

# Solo usar PyMySQL cuando NO haya DATABASE_URL (o sea, en local con MySQL/XAMPP)
if not os.getenv("DATABASE_URL"):
    import pymysql
    pymysql.install_as_MySQLdb()
