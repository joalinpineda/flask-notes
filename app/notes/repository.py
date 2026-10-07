from flask_sqlalchemy.pagination import Pagination

from app.models.note import Note, db


class NoteRepository:
    def __init__(self):
        self.db = db

    def paginated_note_list(self, per_page: int = 6) -> Pagination:
        return Note.query.order_by(Note.created_at.desc()).paginate(per_page=per_page)

    def last_ten_notes(self) -> list[Note]:
        return Note.query.order_by(Note.created_at.desc()).limit(10).all()

    def get_by_slug(self, slug: str) -> Note:
        note = self.db.one_or_404(
            db.select(Note).filter_by(slug=slug),
            description="We couldn't find the note you're looking for. It might have been deleted, or the link may be broken.",
        )
        return note

    def add(self, title: str, content: str, slug: str) -> Note:
        note = Note(title=title, content=content, slug=slug)
        db.session.add(note)
        return note

    def edit(self, note: Note, title: str, content: str, slug: str) -> Note:
        note.title = title
        note.content = content
        note.slug = slug
        return note

    def delete(self, note: Note) -> None:
        self.db.session.delete(note)
