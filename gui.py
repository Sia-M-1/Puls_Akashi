import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QTextEdit, QListWidget, QStackedWidget, QFormLayout, QGroupBox, QRadioButton
from PyQt5.QtGui import QFont
from database import *  # импортируем наши функции работы с базой данных

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
        
        # Поля для ввода заметки
        form_layout = QFormLayout()
        self.title_edit = QLineEdit()
        self.content_edit = QTextEdit()
        submit_button = QPushButton("Добавить заметку")
        submit_button.clicked.connect(self.save_note)
        
        form_layout.addRow("Название:", self.title_edit)
        form_layout.addRow("Описание:", self.content_edit)
        form_layout.addRow(submit_button)
        
        # Список заметок
        self.notes_list = QListWidget()
        self.update_notes_list()
        
        # Макет всей страницы
        layout.addLayout(form_layout)
        layout.addWidget(self.notes_list)
        self.setLayout(layout)
    
    def update_notes_list(self):
        """ Обновляет список заметок """
        conn = sqlite3.connect('genshin.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, title FROM notes ORDER BY date_created DESC")
        rows = cursor.fetchall()
        self.notes_list.clear()
        for row in rows:
            item_text = f"{row[1]} ({row[0]})"
            self.notes_list.addItem(item_text)
        conn.close()
    
    def save_note(self):
        """ Сохраняет новую заметку в базу данных """
        title = self.title_edit.text()
        content = self.content_edit.toPlainText()
        if title and content:
            save_note(title, content)
            self.update_notes_list()
            self.title_edit.clear()
            self.content_edit.clear()

class CharactersPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        font = QFont("Constantia", 12)
        label = QLabel("Список персонажей скоро появится...")
        label.setFont(font)
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        # Панель навигации
        nav_bar = QHBoxLayout()
        btn_notes = QPushButton("Заметки")
        btn_characters = QPushButton("Персонажи")
        nav_bar.addWidget(btn_notes)
        nav_bar.addWidget(btn_characters)
        layout.addLayout(nav_bar)
        
        # Основное пространство
        self.main_area = QStackedWidget()
        self.notes_page = NotesPage()
        self.characters_page = CharactersPage()
        self.main_area.addWidget(self.notes_page)
        self.main_area.addWidget(self.characters_page)
        layout.addWidget(self.main_area)
        
        # Навигация
        btn_notes.clicked.connect(lambda: self.main_area.setCurrentIndex(0))  # переход на страницу заметок
        btn_characters.clicked.connect(lambda: self.main_area.setCurrentIndex(1))  # переход на страницу персонажей
        
        self.setLayout(layout)
        self.setGeometry(300, 300, 700, 500)
        self.setWindowTitle('Геншин-хелпер')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())