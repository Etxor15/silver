from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QInputDialog, QHBoxLayout, QVBoxLayout, QFormLayout


import json


app = QApplication([])


#Interfaz de la app
#parámetros de la ventana de la app
notes_win = QWidget()
notes_win.setWindowTitle('Notas inteligentes')
notes_win.resize(900, 600)


#widgets de la ventana de la app
list_notes = QListWidget()
list_notes_label = QLabel('Lista de notas')


button_note_create = QPushButton('Crear nota') #aparece una ventana con el campo “Ingresar nombre de nota”
button_note_del = QPushButton('Eliminar nota')
button_note_save = QPushButton('Guardar nota')


field_tag = QLineEdit('')
field_tag.setPlaceholderText('Ingresar etiqueta...')
field_text = QTextEdit()
button_tag_add = QPushButton('Añadir a nota')
button_tag_del = QPushButton('Remover etiqueta de nota')
button_tag_search = QPushButton('Buscar notas por etiqueta')
list_tags = QListWidget()
list_tags_label = QLabel('Lista de etiquetas')


#organizando los widgets por diseño
layout_notes = QHBoxLayout()
col_1 = QVBoxLayout()
col_1.addWidget(field_text)


col_2 = QVBoxLayout()
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)
row_1 = QHBoxLayout()
row_1.addWidget(button_note_create)
row_1.addWidget(button_note_del)
row_2 = QHBoxLayout()
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


layout_notes.addLayout(col_1, stretch = 2)
layout_notes.addLayout(col_2, stretch = 1)
notes_win.setLayout(layout_notes)


#Funcionalidad de la app


#Trabajando con el texto de la nota
def add_note():
    note_name, ok = QInputDialog.getText(notes_win, "Añadir nota", "Nombre de nota: ")
    if ok and note_name != "":
        notes[note_name] = {"texto" : "", "etiquetas" : []}
        list_notes.addItem(note_name)
        list_tags.addItems(notes[note_name]["etiquetas"])
        print(notes) 


def show_note():
    #recibiendo texto de la nota con título resaltado y mostrándolo en el campo editar
    key = list_notes.selectedItems()[0].text()
    print(key)
    field_text.setText(notes[key]["texto"])
    list_tags.clear()
    list_tags.addItems(notes[key]["etiquetas"])


def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]["texto"] = field_text.toPlainText()
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("¡La nota para guardar no está seleccionada!")


def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(notes)
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("¡La nota para eliminar no está seleccionada!")


#Trabajando con etiquetas de nota
def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if not tag in notes[key]["etiquetas"]:
            notes[key]["etiquetas"].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("¡La nota para añadir una etiqueta no está seleccionada!")


def del_tag():
    if list_tags.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[key]["etiquetas"].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]["etiquetas"])
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
    else:
        print("¡La etiqueta a ser eliminada no está seleccionada!")


def search_tag():
    print(button_tag_search.text())
    tag = field_tag.text()
    if button_tag_search.text() == "Buscar notas por etiqueta" and tag:
        print(tag)
        notes_filtered = {} #las notas con la etiqueta resaltada estarán aquí
        for note in notes:
            if tag in notes[note]["etiquetas"]: 
                notes_filtered[note]=notes[note]
        button_tag_search.setText("Restablecer búsqueda")
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filtered)
        print(button_tag_search.text())
    elif button_tag_search.text() == "Restablecer búsqueda":
        field_tag.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes)
        button_tag_search.setText("Buscar notas por etiqueta")
        print(button_tag_search.text())
    else:
        pass
    
#Ejecución de la app
#Adjuntando el manejo de eventos
button_note_create.clicked.connect(add_note)
list_notes.itemClicked.connect(show_note)
button_note_save.clicked.connect(save_note)
button_note_del.clicked.connect(del_note)
button_tag_add.clicked.connect(add_tag)
button_tag_del.clicked.connect(del_tag)
button_tag_search.clicked.connect(search_tag)


#app startup 
notes_win.show()




app.exec_()
