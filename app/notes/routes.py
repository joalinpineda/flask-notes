from flask import Blueprint, redirect, render_template, request, abort, url_for
from slugify import slugify
from sqlalchemy import select

from app.models.note import Note, db
from app.notes.slug_service import generate_slug

notes_bp = Blueprint("notes", __name__)


@notes_bp.route("/")
def main_list():
    notes = Note.query.order_by(Note.created_at.desc()).paginate(per_page=6)
    return render_template("main_list.html", notes=notes)


@notes_bp.route("/note/<string:slug>")
def view_note(slug):
    note = db.one_or_404(
        db.select(Note).filter_by(slug=slug),
        description="We couldn't find the note you're looking for. It might have been deleted, or the link may be broken.",
    )
    return render_template("view_note.html", note=note, notes=Note.query.all())


@notes_bp.route("/note/new", methods=["GET", "POST"])
def add_note():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        slug = generate_slug(title)
        note = Note(title=title, content=content, slug=slug)
        db.session.add(note)
        db.session.commit()
        return redirect(url_for("notes.main_list"))
    return render_template("add_note.html", notes=Note.query.all())


@notes_bp.route("/note/<string:slug>/edit", methods=["GET", "POST"])
def edit_note(slug):
    note = db.one_or_404(
            db.select(Note).filter_by(slug=slug),
            description="We couldn't find the note you're looking for. It might have been deleted, or the link may be broken.",
        )
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        if title != note.title:
            note.slug = generate_slug(title)
        note.title = title
        note.content = content 
        slug = generate_slug(title)
        db.session.commit()
        return redirect(url_for("notes.main_list"))
    return render_template("edit_note.html", note=note, notes=Note.query.all())


@notes_bp.route("/note/<string:slug>/delete", methods=["POST"])
def delete_note(slug):
    note = db.one_or_404(
                db.select(Note).filter_by(slug=slug),
                description="We couldn't find the note you're looking for. It might have been deleted, or the link may be broken.",
            )
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for("notes.main_list"))