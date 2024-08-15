import databases
import sqlalchemy

DATABASE_URL = "sqlite:///online_stor.db"

# Создание подключения к базе данных
database = databases.Database(DATABASE_URL)

# Создание объекта MetaData для описания структуры базы данных
metadata = sqlalchemy.MetaData()

# Создание движка для работы с базой данных
engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
