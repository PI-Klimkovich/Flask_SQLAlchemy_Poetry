from flask import Flask, render_template, url_for, request, redirect
from crud import get_note, create_note, get_notes, delete_note, update_note
import time

app = Flask(__name__)

# Как активировать db??


@app.route('/')
@app.route('/home')
def index():
    notes = get_notes()
    return render_template('index.html', notes=notes)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/notes')
def posts():
    notes = get_notes()
    return render_template('notes.html', notes=notes)


@app.route('/about_note/<uuid>')
def post_about(uuid):
    note = get_note(uuid)
    return render_template('note_about.html', note=note)


@app.route('/notes/<uuid>')
def post_detail(uuid):
    note = get_note(uuid)
    return render_template('note_detail.html', note=note)


@app.route('/notes/<uuid>/delete')
def post_delete(uuid):
    try:
        delete_note(uuid)
        return redirect('/notes')
    except:
        return "При удалении записи произошла ошибка"


@app.route('/notes/<uuid>/update', methods=['POST', 'GET'])
def post_update(uuid):
    note = get_note(uuid)
    if request.method == 'POST':
        note_data = request.form

        try:
            update_note(uuid, note_data)
            return redirect('/notes')
        except:
            return "При редактировании заметки произошла ошибка"
    else:
        return render_template('note_update.html', note=note)


@app.route('/create_note', methods=['POST', 'GET'])
def create_post():
    if request.method == 'POST':
        note_data = request.form

        try:
            note = create_note(title=note_data['title'], content=note_data['content'])
            return redirect(url_for('post_about', uuid=note.uuid))
        except:
            return "При добавлении заметки произошла ошибка"
    else:
        return render_template('create_note.html')


@app.route('/note_access', methods=['POST', 'GET'])
def note_access():
    if request.method == 'POST':
        uuid = request.form['uuid']
        try:
            note = get_note(uuid)
            return redirect(url_for('post_detail', uuid=note.uuid))
        except:
            return redirect('/id')
    else:
        return render_template('note_access.html')


@app.route('/id')
def id_id():
    return render_template('id_id.html')


if __name__ == "__main__":
    # create_tables()  ##########################
    app.run(debug=True)  # 'debug=True' - для отслеживания ошибок при тестировании
