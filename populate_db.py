from database import *

def populate_characters():
    characters = [
        {
            "name": "Дилюк",
            "description": "Мастер меча, защитник Монштадта днем и ночной охотник ночью.",
            "talent_materials": "Волчья острота, опыт героя, философские размышления о законах природы.",
            "recommended_artifacts": "Набор гонца рассвета, комплект избранника ветра.",
            "recommended_weapon": "Меч демонслея."
        },
        {
            "name": "Джинн",
            "description": "Великолепный капитан стражи Монштадта, специалист в искусстве лечения и исцеления.",
            "talent_materials": "Цвет окиси серебра, алхимическая философия, звездный блеск.",
            "recommended_artifacts": "Архонтова тиара, железный костяк.",
            "recommended_weapon": "Белая рапира."
        },
        # Добавляйте другие персонажи аналогичным образом
    ]

    for character in characters:
        insert_character(**character)

if __name__ == "__main__":
    populate_characters()
