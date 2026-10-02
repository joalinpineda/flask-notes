from flask import Blueprint, redirect, render_template, request, abort, url_for

from models import Note, db
from services.slug_service import generate_slug

notes_bp = Blueprint('notes', __name__)

@notes_bp.route('/')
def main_list():
    notes = Note.query.order_by(Note.created_at.desc()).paginate(per_page=6)
    return render_template('main_list.html', notes=notes)


@notes_bp.route('/view/<int:id>')
def view_note(id):
    note = db.get_or_404(Note, id)
    return render_template('view_note.html', note = note, notes=Note.query.all())
    

@notes_bp.route('/add', methods=['GET', 'POST'])
def add_note():
    #Todo: handle sqlalchemy error
    if request.method == "POST":
        title = request.form.get('title')
        content = request.form.get('content')
        slug = generate_slug(title)
        note = Note(title=title, content=content, slug=slug)
        db.session.add(note)
        db.session.commit()
        return redirect(url_for('notes.main_list'))
    return render_template('add_note.html', notes=Note.query.all())


@notes_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_note(id):
    note = db.get_or_404(Note, id)
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        note.title = title
        note.content = content
        db.session.add(note)
        db.session.commit()
        return redirect(url_for('notes.main_list'))
    return render_template('edit_note.html', note = note, notes=Note.query.all())

@notes_bp.route('/delete/<int:id>', methods=['POST'])
def delete_note(id):
    note = db.get_or_404(Note, id)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for('notes.main_list'))