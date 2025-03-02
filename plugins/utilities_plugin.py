import subprocess
from plugins.plugin_register import register

@register(plugin="utilities")
def open_notepad_on_desktop():
    subprocess.run("notepad", check=True)
    return "Opened Notepad on Desktop"

@register(plugin="utilities")
def open_calculator_on_desktop():
    subprocess.run("calc", check=True)
    return "Opened Calculator on Desktop"

@register(plugin="system")
def terminate_close_shutdown_end_app():
    exit(0)