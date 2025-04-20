class States:
    PREPARING = 1
    CHOICE_THEME = 2
    CHOICE_QUESTION = 3
    WAITING_PLAYER = 4
    WAITING_ANSWER = 5
    GAME_OVER = 6
    GAME_STOPPED = 7
    BLOCKED = 8


class Timers:
    WAITING_PLAYER = 1
    WAITING_PLAYER_BEFORE_BAD_ANSWER = 1
    WAITING_ANSWER = 10


class GameSetting:
    NUMBER_THEMES = 6
    NUMBER_QUESTIONS = 4
    MIN_NUMBER_PLAYERS = 1


class GameImages:
    START = "https://i.postimg.cc/43dQYpFX/start.jpg"
    PREPARING = "https://i.postimg.cc/MpT1cM7m/image.jpg"
    CHOICE_THEME = "https://i.postimg.cc/Cxctpq7y/choice-theme.jpg"
    CHOICE_QUESTION = "https://i.postimg.cc/pXKNnrB4/choice-question.jpg"
    QUESTION = "https://i.postimg.cc/tC7gWhcJ/image.jpg"
    TRUE_ANSWER = "https://i.postimg.cc/g0bcC12L/image.jpg"
    FALSE_ANSWER = "https://i.postimg.cc/rm8VmWW8/image.jpg"


WAITING_PLAYERS = (
    "Для начала игры пользователи должны подтверидть участие.\n"
    "ждем пока все присоединяться....\n"
    "\n"
    "Участники:\n%s"
)
CURRENT_TURN = "Ход игрока: %s\nвыберите тему..."
CURRENT_THEME = "Тема %s\nВыберите стоиомoсть..."
CURRENT_QUESTION = "Вопрос:\n\n%s\n\nОтвечает первый нажавыший на кнопку"
TRUE_ANSWER = "Ураа ответ верный\nначисляем балы\n%s"
FALSE_ANSWER = "Ответ не верный\nснимаем балы\n%s"
