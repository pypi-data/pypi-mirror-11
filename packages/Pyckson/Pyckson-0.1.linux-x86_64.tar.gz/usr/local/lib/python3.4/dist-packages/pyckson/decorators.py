from inspect import signature

from pyckson.builders import build_pyckson_model
from pyckson.const import PYCKSON_TYPEINFO, PYCKSON_ATTR, PYCKSON_MODEL
from pyckson.helpers import find_class_constructor


def listtype(param_name, param_sub_type):
    def class_decorator(cls):
        type_info = getattr(cls, PYCKSON_TYPEINFO, dict())
        type_info[param_name] = param_sub_type
        setattr(cls, PYCKSON_TYPEINFO, type_info)
        return cls

    return class_decorator


def pyckson(cls):
    setattr(cls, PYCKSON_ATTR, True)
    constructor = find_class_constructor(cls)
    type_info = getattr(cls, PYCKSON_TYPEINFO, dict())
    model = build_pyckson_model(signature(constructor), type_info)
    setattr(cls, PYCKSON_MODEL, model)
    return cls
