from slugify import slugify
from sqlalchemy import select

from app.models.note import Note, db


def exist_slug(slug: str) -> bool:
    """Validate if the slug already exists in the DB."""
    result = db.session.execute(
        select(Note).where(Note.slug == slug)
    ).scalar_one_or_none()
    return result is not None


def generate_slug(title: str) -> str:
    """Create a unique slug for the note."""
    slug = slugify(title)
    #If slug does not exist, then return it
    if not exist_slug(slug):
        return slug
    
    #Else try by adding a number till the slug is unique
    i = 2
    while exist_slug(f"{slug}-{i}"):
        i += 1
    return f"{slug}-{i}"
