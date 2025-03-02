import os
import json
import importlib
from pathlib import Path

bot_functions = {}

def load_plugin_config(config_path: Path = None) -> dict:
    if config_path is None:
        config_path = Path(__file__).parent.parent / "config" / "plugin_config.json"
    try:
        with config_path.open("r") as f:
            config = json.load(f)
        return config.get("plugins", {})
    except FileNotFoundError:
        return {}

enabled_plugins = load_plugin_config()

def register(func=None, *, plugin: str = None):
    if func is None:
        return lambda f: register(f, plugin=plugin)
    
    if plugin is not None and not enabled_plugins.get(plugin, True):
        return func
    
    bot_functions[func.__name__] = func
    return func

def load_active_plugins(config_path: Path = None):
    plugins_config = load_plugin_config(config_path)
    
    for plugin_name, is_active in plugins_config.items():
        if is_active:
            module_name = f"plugins.{plugin_name}_plugin"
            try:
                importlib.import_module(module_name)
                print(f"Successfully imported the {plugin_name} plugin")
            except ImportError as e:
                print(f"Error importing {module_name}: {e}")
