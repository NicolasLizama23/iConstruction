import os

# Solo habilitar PyMySQL cuando estés usando MySQL (local/XAMPP)
if not os.getenv("DATABASE_URL"):
    import pymysql
    pymysql.install_as_MySQLdb()
