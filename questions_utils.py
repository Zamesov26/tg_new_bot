import json


def upload_questions(file_path="questions.txt"):
    res = {}
    with open(file_path, "r") as file:
        data = file.read()
        themes = data.split("\n\n")
        for theme in themes:
            theme_title, *questions = theme.strip().lstrip("#").split("\n")
            for i in range(0, len(questions), 2):
                question = questions[i]
                answer = questions[i + 1]
                res.setdefault(theme_title.capitalize(), []).append(
                    {"question": question.strip(), "answer": answer.strip()}
                )
    with open("questions.json", "w", encoding="utf-8") as file:
        json.dump(res, file)


def load_questions(file_path="questions.json", encoding="utf-8"):
    with open(file_path, "r") as file:
        return json.load(file)


if __name__ == "__main__":
    load_questions()
