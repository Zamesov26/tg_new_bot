from app.tg_api.models import Update


class TextFilter:
    def __init__(self, text=""):
        self.text = text

    def __call__(self, update: Update) -> bool:
        return bool(update.message and update.message.text)
