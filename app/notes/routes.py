from flask import Blueprint, redirect, render_template, request, url_for
from flask_sqlalchemy import query

from app.notes.service import NoteService

notes_bp = Blueprint("notes", __name__)

note_service = NoteService()


@notes_bp.route("/")
def main_list():
    search = request.args.get("search")
    favorites = request.args.get("favorites") == "true"
    page = request.args.get('page', 1, type=int)
    notes = (
        note_service.search_by_title(query=search, page=page)
        if search
        else note_service.get_paginated_notes(page=page)
    )
    notes_list = (
        note_service.get_favorites() if favorites else note_service.get_recent_notes()
    )
    print('search: ', search)
    print('resutls: ', notes.items)
    print('query', repr(query))
    return render_template("main_list.html", notes=notes, notes_list=notes_list)


@notes_bp.route("/note/<string:slug>")
def view_note(slug: str):
    favorites = request.args.get("favorites") == "true"
    notes_list = (
            note_service.get_favorites() if favorites else note_service.get_recent_notes()
        )
    return render_template(
        "view_note.html",
        note=note_service.get_note_by_slug(slug),
        notes_list=notes_list,
        filters=request.args
    )


@notes_bp.route("/note/new", methods=["GET", "POST"])
def add_note():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        note_service.add_note(title=title, content=content)
        return redirect(url_for("notes.main_list"))
    favorites = request.args.get("favorites") == "true"
    notes_list = (
            note_service.get_favorites() if favorites else note_service.get_recent_notes()
        )
    return render_template("add_note.html", notes_list=notes_list, filters=request.args)


@notes_bp.route("/note/<string:slug>/edit", methods=["GET", "POST"])
def edit_note(slug: str):
    note = note_service.get_note_by_slug(slug)
    favorites = request.args.get("favorites") == "true"
    notes_list = (
            note_service.get_favorites() if favorites else note_service.get_recent_notes()
        )
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        note_service.edit_note(note=note, title=title, content=content)
        return redirect(url_for("notes.main_list"))
    return render_template(
        "edit_note.html", note=note, notes_list=notes_list, filters=request.args
    )


@notes_bp.route("/note/<string:slug>/delete", methods=["POST"])
def delete_note(slug: str):
    note = note_service.get_note_by_slug(slug)
    note_service.delete_note(note)
    return redirect(url_for("notes.main_list"))


@notes_bp.route("/note/<string:slug>/favorite", methods=["POST"])
def mark_as_favorite(slug: str):
    note = note_service.get_note_by_slug(slug)
    note_service.mark_note_as_favorite(note)
    return redirect(url_for("notes.main_list"))
