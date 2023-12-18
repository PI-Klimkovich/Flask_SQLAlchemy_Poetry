from sqlalchemy import select, desc, update, delete
from models import Note, session


def get_note(uuid: str) -> Note:
    with session() as conn:
        query = select(Note).where(Note.uuid == uuid)
        return conn.execute(query).scalar_one()


def delete_note(uuid: str) -> None:
    with session() as conn:
        stmt = (
            delete(Note).
            where(Note.uuid == uuid)
        )
        conn.execute(stmt)
        conn.commit()
        # return note


def update_note(uuid, note_data) -> None:
    with session() as conn:
        stmt = (
            update(Note).
            where(Note.uuid == uuid).
            values(title=note_data['title'], content=note_data['content'])
        )
        conn.execute(stmt)
        conn.commit()


def create_note(title: str, content: str) -> Note:
    with session() as conn:
        note = Note(title=title, content=content)
        conn.add(note)  # Добавляем.
        conn.commit()  # Подтверждаем создание.
        conn.refresh(note)  # Обновляем. Для чего? Получаем созданный ID из базы.
    return note


def get_notes() -> list[Note]:
    with session() as conn:
        return conn.execute(select(Note).order_by(desc(Note.created_at))).scalars().all()
