import inspect
from fastapi import Form

"""
Decorator that adds an 'as_form' class method to a Pydantic model,
allowing it to be instantiated from form data submitted via an HTTP request.
"""

def as_form(cls):
    new_params = []

    for field_name, model_field in cls.model_fields.items():
        new_params.append(
            inspect.Parameter(
                field_name,
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                default=Form(...)
                if model_field.is_required 
                else Form(model_field.default),
                annotation=model_field.annotation,
            )
        )

    async def _as_form(**data):
        return cls(**data)
    
    sig = inspect.signature(_as_form)
    sig = sig.replace(parameters=new_params)

    _as_form.__signature__ = sig

    cls.as_form = _as_form

    return cls