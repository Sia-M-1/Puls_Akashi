import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QTextEdit, QListWidget, QStackedWidget, QFormLayout, QGroupBox, QRadioButton, QDialog, QCheckBox, QMessageBox, QInputDialog
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from database import *  # импортируем наши функции работы с базой данных

class ViewNoteDialog(QDialog):
    def __init__(self, note_data):
        super().__init__()
        self.initUI(note_data)
    
    def initUI(self, note_data):
        layout = QVBoxLayout()
        title_label = QLabel(f"<h2>{note_data['title']}</h2>")
        content_label = QLabel(note_data['content'])
        close_button = QPushButton("Закрыть")
        close_button.clicked.connect(self.accept)
        
        layout.addWidget(title_label)
        layout.addWidget(content_label)
        layout.addWidget(close_button)
        self.setLayout(layout)
        self.setWindowTitle("Просмотр заметки")

class ListItemWidget(QWidget):
    def __init__(self, item_id, text, checked=False):
        super().__init__()
        self.item_id = item_id
        self.checkbox = QCheckBox(text)
        self.checkbox.setChecked(checked)
        self.checkbox.stateChanged.connect(self.on_check_state_changed)
        
        layout = QHBoxLayout()
        layout.addWidget(self.checkbox)
        self.setLayout(layout)
    
    def on_check_state_changed(self, state):
        """ Обновляет статус отметки в базе данных """
        mark_completed(self.item_id, bool(state))

class EditListDialog(QDialog):
    def __init__(self, note_id, parent=None):
        super().__init__(parent)
        self.note_id = note_id
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        # Получаем пункты списка
        items = get_list_items(self.note_id)
        for item in items:
            # Замена словарного доступа на индексы кортежа
            list_item_widget = ListItemWidget(item[0], item[1], item[2])
            layout.addWidget(list_item_widget)
        
        add_new_item_button = QPushButton("Добавить новый пункт")
        add_new_item_button.clicked.connect(self.add_new_item)
        layout.addWidget(add_new_item_button)
        
        close_button = QPushButton("Закрыть")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)
        
        self.setLayout(layout)
        self.setWindowTitle("Редактирование списка")
    
    def add_new_item(self):
        new_item_text, ok_pressed = QInputDialog.getText(self, "Новый пункт", "Введите текст пункта:")
        if ok_pressed and new_item_text.strip():
            try:
                insert_list_item(self.note_id, new_item_text)
                self.parent().update_lists()
            except Exception as ex:
                QMessageBox.critical(self, "Ошибка", str(ex))

class NotesPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        # Переключатель между заметками и списками
        self.note_type_radio_group = QGroupBox("Тип заметки")
        radio_buttons_layout = QHBoxLayout()
        self.radio_note = QRadioButton("Заметки")
        self.radio_list = QRadioButton("Списки")
        radio_buttons_layout.addWidget(self.radio_note)
        radio_buttons_layout.addWidget(self.radio_list)
        self.note_type_radio_group.setLayout(radio_buttons_layout)
        layout.addWidget(self.note_type_radio_group)
        
        # Виджеты для отображения заметок и списков
        self.notes_list = QListWidget()
        self.lists_list = QListWidget()
        
        # Поля для ввода заметки
        form_layout = QFormLayout()
        self.title_edit = QLineEdit()
        self.content_edit = QTextEdit()
        submit_button = QPushButton("Добавить")
        submit_button.clicked.connect(self.save_item)
        
        form_layout.addRow("Название:", self.title_edit)
        form_layout.addRow("Описание:", self.content_edit)
        form_layout.addRow(submit_button)
        
        # Генерация общей компоновки
        stacked_layout = QStackedWidget()
        stacked_layout.addWidget(self.notes_list)
        stacked_layout.addWidget(self.lists_list)
        
        # Навигация по переключателю
        self.radio_note.clicked.connect(lambda: stacked_layout.setCurrentIndex(0))
        self.radio_list.clicked.connect(lambda: stacked_layout.setCurrentIndex(1))
        
        # Сигнал клика по заметке или списку
        self.notes_list.itemDoubleClicked.connect(self.open_note_dialog)
        self.lists_list.itemDoubleClicked.connect(self.edit_list_dialog)
        
        # Добавляем кнопку удаления
        delete_button = QPushButton("Удалить выбранную запись")
        delete_button.clicked.connect(self.delete_selected_item)
        layout.addWidget(delete_button)
        
        # Собираем всё вместе
        layout.addLayout(form_layout)
        layout.addWidget(stacked_layout)
        self.setLayout(layout)
    
    def save_item(self):
        """ Сохраняет новую запись в базу данных """
        title = self.title_edit.text()
        content = self.content_edit.toPlainText()
        note_type = "list" if self.radio_list.isChecked() else "note"
        
        if title and content:
            save_note(title, content, note_type=note_type)
            self.update_lists()
            self.title_edit.clear()
            self.content_edit.clear()
    
    def update_lists(self):
        """ Обновляет списки заметок и списков раздельно """
        conn = sqlite3.connect('genshin.db')
        cursor = conn.cursor()
        
        # Получаем заметки
        cursor.execute("SELECT id, title FROM notes WHERE type='note' ORDER BY date_created DESC")
        rows = cursor.fetchall()
        self.notes_list.clear()
        for row in rows:
            item_text = f"{row[1]} ({row[0]})"
            self.notes_list.addItem(item_text)
        
        # Получаем списки
        cursor.execute("SELECT id, title FROM notes WHERE type='list' ORDER BY date_created DESC")
        rows = cursor.fetchall()
        self.lists_list.clear()
        for row in rows:
            item_text = f"{row[1]} ({row[0]})"
            self.lists_list.addItem(item_text)
        
        conn.close()
    
    def edit_list_dialog(self, item):
        """ Открывает диалоговое окно для редактирования списка """
        selected_id = int(item.text().split("(")[-1][:-1])
        dialog = EditListDialog(selected_id, parent=self)
        dialog.exec_()
    
    def open_note_dialog(self, item):
        """ Открывает диалоговое окно с содержимым выбранной заметки """
        selected_id = int(item.text().split("(")[-1][:-1])
        note_data = self.get_note_by_id(selected_id)
        dialog = ViewNoteDialog(note_data)
        dialog.exec_()
    
    def get_note_by_id(self, note_id):
        """ Получает полную информацию о заметке по её ID """
        conn = sqlite3.connect('genshin.db')
        cursor = conn.cursor()
        cursor.execute("SELECT title, content FROM notes WHERE id=?", (note_id,))
        result = cursor.fetchone()
        conn.close()
        return {"title": result[0], "content": result[1]}
    
    def delete_selected_item(self):
        """ Удаляет выбранную заметку или список """
        selected_item = None
        if len(self.notes_list.selectedItems()) > 0:
            selected_item = self.notes_list.selectedItems()[0]
        elif len(self.lists_list.selectedItems()) > 0:
            selected_item = self.lists_list.selectedItems()[0]
        
        if selected_item is None:
            return  # Нет выбранных элементов
        
        selected_id = int(selected_item.text().split("(")[-1][:-1])
        confirm_delete = QMessageBox.question(
            self,
            "Подтверждение",
            f"Удалить выбранную запись '{selected_item.text()}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirm_delete == QMessageBox.Yes:
            delete_note(selected_id)
            self.update_lists()

class CharactersPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        # Виджет для отображения персонажей
        self.character_list = QListWidget()
        self.character_list.itemDoubleClicked.connect(self.view_character_details)
        
        # Загрузка персонажей из базы данных
        characters = get_all_characters()
        for char in characters:
            # Используем имя персонажа для отображения
            self.character_list.addItem(char[1])  # Индексация начинается с 0, поэтому второй элемент - имя персонажа
        
        layout.addWidget(self.character_list)
        self.setLayout(layout)
    
    def view_character_details(self, item):
        """Открывает окно с деталями выбранного персонажа"""
        selected_name = item.text()
        details = next((char for char in get_all_characters() if char[1] == selected_name), None)
        if details:
            dialog = CharacterDetailsDialog(details)
            dialog.exec_()

class CharacterDetailsDialog(QDialog):
    def __init__(self, character_data):
        super().__init__()
        self.initUI(character_data)
    
    def initUI(self, character_data):
        layout = QVBoxLayout()
        title_label = QLabel(f"<h2>{character_data[1]}</h2>")  # Имя персонажа
        description_label = QLabel(f"Описание: {character_data[2]}")  # Описание
        rarity_label = QLabel(f"Редкость: {character_data[3]}")  # Редкость
        element_label = QLabel(f"Элемент: {character_data[4]}")  # Элемент
        birthday_label = QLabel(f"День рождения.: {character_data[5]}")  # День рождения
        constellation_label = QLabel(f"Созвездие: {character_data[6]}")  # Созвездие
        region_label = QLabel(f"Регион: {character_data[7]}")  # Регион
        type_weapon_label = QLabel(f"Тип оружия: {character_data[8]}")  # Тип оружия
        artifacts_label = QLabel(f"Рекомендуемые артефакты: {character_data[9]}")  # Рекомендуемые артефакты
        weapon_label = QLabel(f"Рекомендуемое оружие: {character_data[10]}")  # Рекомендованное оружие
        close_button = QPushButton("Закрыть")
        close_button.clicked.connect(self.accept)
        
        layout.addWidget(title_label)
        layout.addWidget(description_label)
        layout.addWidget(rarity_label)
        layout.addWidget(element_label)
        layout.addWidget(birthday_label)
        layout.addWidget(constellation_label)
        layout.addWidget(region_label)
        layout.addWidget(type_weapon_label)
        layout.addWidget(artifacts_label)
        layout.addWidget(weapon_label)
        layout.addWidget(close_button)
        self.setLayout(layout)
        self.setWindowTitle("Детали персонажа")

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        nav_bar = QHBoxLayout()
        btn_notes = QPushButton("Заметки")
        btn_characters = QPushButton("Персонажи")
        nav_bar.addWidget(btn_notes)
        nav_bar.addWidget(btn_characters)
        layout.addLayout(nav_bar)
        
        # Основной контент
        self.main_area = QStackedWidget()
        self.notes_page = NotesPage()
        self.characters_page = CharactersPage()
        self.main_area.addWidget(self.notes_page)
        self.main_area.addWidget(self.characters_page)
        layout.addWidget(self.main_area)
        
        # Навигационные сигналы
        btn_notes.clicked.connect(lambda: self.main_area.setCurrentIndex(0))  # Переход на страницу заметок
        btn_characters.clicked.connect(lambda: self.main_area.setCurrentIndex(1))  # Переход на страницу персонажей
        
        self.setLayout(layout)
        self.setGeometry(300, 300, 700, 500)
        self.setWindowTitle('Пульс Акаши')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
