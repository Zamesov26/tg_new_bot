from collections.abc import Iterable

from app.own_game.models import Category, Question


def category_to_dict(category: Category) -> dict:
    return {
        "id": category.id,
        "name": category.name,
    }


def categories_to_dict(themes: Iterable[Category]) -> list[dict]:
    return [category_to_dict(theme) for theme in themes]


def question_to_dict(question: Question) -> dict:
    return {
        "id": question.id,
        "title": question.title,
        "category_id": question.category_id,
        "answer": question.answer,
    }


def questions_to_dict(questions: Iterable[Question]) -> list[dict]:
    return [question_to_dict(question) for question in questions]
