import importlib
import pkgutil
from config.chat_config import ChatConfig

from . import language_configs
# list of ChatConfig objects for different languages
chat_configs: dict[str, ChatConfig] = {}

# List the submodules and import each one
for _, submodule_name, _ in pkgutil.iter_modules(language_configs.__path__):
    full_module_name = f"{language_configs.__name__}.{submodule_name}"
    submodule = importlib.import_module(full_module_name)
    chat_config: ChatConfig = submodule.chat_config

    # add to list
    chat_configs.update({chat_config.language_code: chat_config})


def get_languages() -> list[str]:
    return [cc.get_language_str() for cc in chat_configs.values()]


def get_chat_config(language: str) -> ChatConfig:
    # remove country flag
    language = language[-5:]
    return chat_configs[language]
