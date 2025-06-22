import sys
from PyQt5.QtWidgets import QApplication
from gui import MainWindow
from database import create_database, get_all_characters # Импортируем необходимые функции
from populate_db import populate_characters_if_empty

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Создаем базу данных (если она еще не существует)
    create_database()

    # Проверяем, есть ли данные в таблице characters
    characters = get_all_characters()
    if not characters:
        # Если таблица пуста, заполняем ее
        populate_characters_if_empty()  # Вызываем функцию заполнения

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
