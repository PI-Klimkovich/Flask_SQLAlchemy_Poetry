import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Строка подключения (DSN)

# Диалект - `sqlite`
# Обращение - `://`
# Путь - `/tasks_lesson_18.db` (В текущей папке)
dsn = "sqlite:///tasks_lesson_18.db"

# Точка входа в БД.
# `echo=True` - выводятся все действия с базой.
engine = create_engine(dsn, echo=True)

# Класс для сессий, которые использует `engine`
# `autoflush=False` - отключение автоматических подтверждений действий.
session = sessionmaker(bind=engine, autoflush=False)


# Декларативная основа для будущих классов
class Base(DeclarativeBase):
    pass


# Декларативное описание таблицы
class Note(Base):
    __tablename__ = "note"
    uuid = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __str__(self):
        return f"Note: {self.uuid}"

    def __repr__(self):
        return '<Note %r>' % self.uuid


def drop_tables():
    # Удаление таблиц, унаследованных от `Base`
    Base.metadata.drop_all(engine)


def create_tables():
    # Создание таблиц, унаследованных от `Base`
    Base.metadata.create_all(engine)
