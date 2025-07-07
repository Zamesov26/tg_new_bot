def add_questionare(foo, questionare_name: str):
    async def wrap(*args, **kwargs):
        return await foo(*args, questionnaire=questionare_name, **kwargs)

    return wrap
