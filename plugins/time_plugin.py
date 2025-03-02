import datetime
from plugins.plugin_register import register

@register(plugin="time")
def current_time():
    return str(datetime.datetime.now())
