def introspection_info(obj):
    obj_type = type(obj).__name__
    obj_module = getattr(obj, '__module__', 'Built-in')  # Встроенные типы могут не иметь модуля
    attributes = [attr for attr in dir(obj) if not callable(getattr(obj, attr)) and not attr.startswith("__")]
    methods = [method for method in dir(obj) if callable(getattr(obj, method)) and not method.startswith("__")]
    special_methods = [method for method in dir(obj) if method.startswith("__") and callable(getattr(obj, method))]
    info = {
        'type': obj_type,
        'attributes': attributes,
        'methods': methods,
        'module': obj_module,
        'special_methods': special_methods,
    }
    return info


class MyClass:
    def __init__(self, value):
        self.value = value

    def get_info(self):
        return introspection_info(self.value)


obj = MyClass(42)
info = obj.get_info()

print(info)
