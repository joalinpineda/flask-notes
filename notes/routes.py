from flask import Blueprint, render_template

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
    

@notes_bp.route('/add')
def add_note():
    return render_template('add_note.html')

@notes_bp.route('/edit/<int:id>')
def edit_note(id):
    note = db.get_or_404(Note, id)
    return render_template('edit_note.html', note = note, notes=Note.query.all())