from flask import Blueprint, render_template
from test_data import notes

notes_bp = Blueprint('notes', __name__)

@notes_bp.route('/')
def main_list():
    return render_template('main_list.html', notes=notes)

@notes_bp.route('/view/<int:id>')
def view_note(id):
    for note in notes:
        if note['id'] == id:
            note_founded = note
            return render_template('view_note.html', note = note_founded, notes=notes)
        note_not_founded =  {
            'id':0, 
            "title": "Note was not found",
            "content": "The note was not found or does not exist, this is a dummy note for testing purposes",
            "created_at": "2026-09-10T08:15:00Z",
            "updated_at": "2026-09-10T08:15:00Z"
          }
    return render_template('view_note.html', note = note_not_founded, notes=notes)
    

@notes_bp.route('/add')
def add_note():
    return render_template('add_note.html')

@notes_bp.route('/edit/<int:id>')
def edit_note(id):
    for note in notes:
        if note['id'] == id:
            note_founded = note
            return render_template('edit_note.html', note = note_founded, notes=notes)
        note_not_founded =  {
            'id':0, 
            "title": "Note was not found",
            "content": "The note was not found or does not exist, this is a dummy note for testing purposes",
            "created_at": "2026-09-10T08:15:00Z",
            "updated_at": "2026-09-10T08:15:00Z"
            }
    return render_template('edit_note.html', note = note_not_founded, notes=notes)