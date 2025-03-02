from plugins.plugin_register import register

@register(plugin="math")
def add_two_numbers(a: float, b: float) -> float:
    return float(a) + float(b)

@register(plugin="math")
def subtract_two_numbers(a: float, b: float) -> float:
    return float(a) - float(b)

@register(plugin="math")
def multiply_two_numbers(a: float, b: float) -> float:
    return float(a) * float(b)

@register(plugin="math")
def divide_two_numbers(a: float, b: float) -> float:
    return float(a) / float(b)
