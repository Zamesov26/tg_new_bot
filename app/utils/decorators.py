def inject_kwargs(foo, **injected_kwargs):
    async def wrap(*args, **kwargs):
        return await foo(*args, **injected_kwargs, **kwargs)
    
    return wrap
