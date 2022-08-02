from PyQt5 import Qt
from PyQt5.QtWidgets import *

app = QApplication([])

notes_win = QWidget()
notes_win.setWindowTitle("Smart note")
notes_win.resize(900, 600)

field_text = QTextEdit()
listname = QLabel("List of notes")
listnote = QListWidget()
button_note_create = QPushButton("Add note")
button_note_del = QPushButton("Delete note")
button_note_save = QPushButton('Save note')

field_tag = QLineEdit('')
field_tag.setPlaceholderText('Enter tag...')
field_text = QTextEdit()
button_tag_add = QPushButton('Add to note')
button_tag_del = QPushButton('Unpin from note')
button_tag_search = QPushButton('Search notes by tag')
list_tags = QListWidget()
list_tags_label = QLabel('List of tags')

layoutbox = QHBoxLayout()

col_1 = QVBoxLayout()
col_2 = QVBoxLayout()

col_1.addWidget(field_text)

col_2.addWidget(listname)
col_2.addWidget(listnote)

row_1 = QHBoxLayout()
row_2 = QHBoxLayout()

row_1.addWidget(button_note_create)
row_1.addWidget(button_note_del)
row_2.addWidget(button_note_save)

col_2.addLayout(row_1)
col_2.addLayout(row_2)

col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)
row_3 = QHBoxLayout()
row_3.addWidget(button_tag_add)
row_3.addWidget(button_tag_del)
row_4 = QHBoxLayout()
row_4.addWidget(button_tag_search)

col_2.addLayout(row_3)
col_2.addLayout(row_4)

layoutbox.addLayout(col_1)
layoutbox.addLayout(col_2)

notes_win.setLayout(layoutbox)

def show_note():
    name = listnote.selectedItems()[0].text()
    notes_data = notes[name]

    field_text.setText(notes_data['text'])
    list_tags.clear()
    list_tags.addItems(notes_data['tag'].split(" "))


listnote.itemClicked.connect(show_note)

def add_note():
    name, ok = QInputDialog.getText(notes_win, "Add Note", "Notes name:")
    if ok and name != '':
        notes[name] = {
            'text': field_text.toPlainText(),
            'tag': field_tag.text()
        }
        listnote.addItem(name)
        list_tags.clear()
        list_tags.addItems(notes[name]['tag'].split(" "))


button_note_create.clicked.connect(add_note)


def del_note():
    if listnote.selectedItems():
        name = listnote.selectedItems()[0].text()
        del notes[name]

        field_text.clear()
        field_tag.clear()
        list_tags.clear()
        listnote.clear()
        listnote.addItems(notes)

        save_note()


button_note_del.clicked.connect(del_note)


def save_note():
    with open('notes_data.json', 'w') as data:
        json.dump(notes, data)

button_note_save.clicked.connect(save_note)

import json

with open('notes_data.json', 'r') as data:
    notes = json.load(data)
listnote.addItems(notes)


def add_tag():
    if listnote.selectedItems():
        name = listnote.selectedItems()[0].text()
        tag = field_tag.text()

        if not tag in notes[name]['tag']:
            notes[name]['tag'] += " " + tag
            list_tags.addItem(tag)
            field_tag.clear()

button_tag_add.clicked.connect(add_tag)

def del_tag():
    if listnote.selectedItems():
        name = listnote.selectedItems()[0].text()
        tag = field_tag.text()
        if tag in notes[name]['tag']:
            notes[name]['tag'] = notes[name]['tag'].replace(' ' + tag, '')
            field_tag.clear()
            list_tags.clear()
            list_tags.addItems(notes[name]['tag'].split(" "))
            
            

button_tag_del.clicked.connect(del_tag)


notes_win.show()
app.exec_()