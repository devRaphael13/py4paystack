import sys
import typing
from functools import wraps
from inspect import _empty, signature
from types import GenericAlias
from .settings import TYPE_CHECK

def func_type_checker(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        if TYPE_CHECK:
            sig = signature(func)
            bound = sig.bind(*args, **kwargs)

            for key, value in bound.arguments.items():
                ann = sig.parameters[key].annotation

                if ann == _empty or isinstance(ann, GenericAlias):
                    continue
            
                if not isinstance(value, get_types(ann)):
                    class_name = bound.arguments.get('self')
                    func_name = func.__name__
                    if class_name:
                        func_name = f"{class_name.__class__.__name__}.{func_name}"

                    raise TypeError(
                        f"Expected type {ann} for {key} in function {func_name}, got {type(value)} instead")
        return func(*args, **kwargs)
    return wrapper


def class_type_checker(_cls):

    class C(_cls):

        def __new__(cls, *args, **kwargs):
            for key, value in _cls.__dict__.items():
                if callable(value):
                    setattr(_cls, key, func_type_checker(value))
            return super().__new__(cls)
    C.__name__ = _cls.__name__
    C.__doc__ = _cls.__doc__
    return C
    

def get_types(ann):
    if isinstance(ann, typing._UnionGenericAlias) and not ".".join(map(str, sys.version_info[:3])).startswith("3.10"):
        return typing.get_args(ann)
    return ann
    

