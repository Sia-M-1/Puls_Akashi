from database import *

def populate_characters():
    characters = [
        {
            "name": "Аль-Хайтам",
            "description": "Нынешний секретарь Академии Сумеру, наделённый выдающимся умом и способностями.",
            "rarity": "5 звёзд",
            "element": "Дендро",
            "birthday": "11 февраля",
            "constellation": "Сокол",
            "region": "Сумеру",
            "type_weapon": "Одноручный меч",
            "recommended_artifacts": '"Позолоченные сны", "Воспоминания дремучего леса"',
            "recommended_weapon": '"Свет лиственного разреза", "Драгоценный омут"'
        },
        {
            "name": "Албедо",
            "description": "Искусственный человек, главный алхимик Ордо Фавониус.",
            "rarity": "5 звёзд",
            "element": "Гео",
            "birthday": "13 сентября",
            "constellation": "Меловой принц",
            "region": "Мондштадт",
            "type_weapon": "Одноручный меч",
            "recommended_artifacts": '"Архаичный камень", "Встречная комета", "Церемония древней знати", "Кокон сладких грёз х4"',
            "recommended_weapon": '"Небесный меч", "Меч Сокола", "Кромсатель пиков", "Осквернённое желание", "Прототип: Злоба", "Предвестник зари"'
        },
        # Другие персонажи здесь по аналогии
    ]

    for character in characters:
        insert_character(**character)

if __name__ == "__main__":
    populate_characters()
