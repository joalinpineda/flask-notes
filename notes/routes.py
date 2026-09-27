from flask import Blueprint, redirect, render_template, request, abort, url_for

from models import Note, db

notes_bp = Blueprint('notes', __name__)

@notes_bp.route('/')
def main_list():
    notes = Note.query.all()
    return render_template('main_list.html', notes=notes)


@notes_bp.route('/view/<int:id>')
def view_note(id):
    note = db.get_or_404(Note, id)
    return render_template('view_note.html', note = note, notes=Note.query.all())
    

@notes_bp.route('/add', methods=['GET', 'POST'])
def add_note():
    if request.method == "POST":
        title = request.form.get('title')
        content = request.form.get('content')
        note = Note(title=title, content=content)
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