from flask import Blueprint, redirect, render_template, request, url_for

from app.notes.repository import NoteRepository
from app.notes.service import NoteService

notes_bp = Blueprint("notes", __name__)

note_service = NoteService()


@notes_bp.route("/")
def main_list():
    return render_template(
        "main_list.html",
        notes_list=note_service.get_paginated_notes(),
        notes=note_service.get_recent_notes(),
    )


@notes_bp.route("/note/<string:slug>")
def view_note(slug: str):
    return render_template(
        "view_note.html",
        note=note_service.get_note_by_slug(slug),
        notes=note_service.get_recent_notes(),
    )


@notes_bp.route("/note/new", methods=["GET", "POST"])
def add_note():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        note_service.add_note(title=title, content=content)
        return redirect(url_for("notes.main_list"))
    return render_template("add_note.html", notes=note_service.get_recent_notes())


@notes_bp.route("/note/<string:slug>/edit", methods=["GET", "POST"])
def edit_note(slug: str):
    note = note_service.get_note_by_slug(slug)
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        note_service.edit_note(note=note, title=title, content=content)
        return redirect(url_for("notes.main_list"))
    return render_template(
        "edit_note.html", note=note, notes=note_service.get_recent_notes()
    )


@notes_bp.route("/note/<string:slug>/delete", methods=["POST"])
def delete_note(slug: str):
    note = note_service.get_note_by_slug(slug)
    note_service.delete_note(note)
    return redirect(url_for("notes.main_list"))
