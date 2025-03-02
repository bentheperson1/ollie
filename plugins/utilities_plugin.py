import subprocess
from plugins.plugin_register import register

@register(plugin="utilities")
def launch_notepad():
    subprocess.run("notepad")
    return "Opened Notepad on Desktop"

@register(plugin="utilities")
def launch_calculator():
    subprocess.run("calc")
    return "Opened Calculator on Desktop"

@register(plugin="system")
def terminate_app():
    exit(0)