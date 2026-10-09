from flask_sqlalchemy.pagination import Pagination

from app.models.note import Note, db
from app.notes.repository import NoteRepository
from app.notes.slug_service import generate_slug


class NoteService:
    def __init__(self):
        self.db = db
        self.repo = NoteRepository()

    def get_paginated_notes(self, per_page: int = 6) -> Pagination:
        return self.repo.paginated_note_list(per_page=per_page)

    def get_recent_notes(self) -> list[Note]:
        return self.repo.last_ten_notes()

    def get_note_by_slug(self, slug: str) -> Note:
        return self.repo.get_by_slug(slug)

    def search_by_title(self, query: str) -> list[Note] | None:
        return self.repo.search(query)

    def add_note(self, title: str, content: str) -> None:
        slug = generate_slug(title)
        try:
            self.repo.add(title, content, slug)
            self.db.session.commit()
        except Exception:
            self.db.session.rollback()
            raise

    def edit_note(self, note: Note, title: str, content: str) -> None:
        slug = note.slug
        if title != note.title:
            slug = generate_slug(title)
        try:
            self.repo.edit(note, title, content, slug)
            self.db.session.commit()
        except Exception:
            self.db.session.rollback()
            raise

    def delete_note(self, note: Note) -> None:
        try:
            self.repo.delete(note)
            self.db.session.commit()
        except Exception:
            self.db.session.rollback()
            raise
