import importlib
import pkgutil
from config.language_templates.chat_config import ChatConfigTemplate
from config.language_templates.gui_text import GuiTextTemplate

from . import language_configs
# list of ChatConfigTemplate objects for different languages
DEFAULT_LANGUAGE="de-de"


class LanguageConfig:
    def __init__(
        self,
        language_code: str,
        language_icon: str,  # emoji
        chat_config: ChatConfigTemplate,
        gui_text: GuiTextTemplate
    ):
        self.language_code = language_code
        self.language_icon = language_icon
        self.chat_config = chat_config
        self.gui_text = gui_text

    def get_language_str(self) -> str:
        return f"{self.language_icon} {self.language_code}"


languages: dict[str, LanguageConfig] = {}
# List the submodules and import each one
for _, submodule_name, _ in pkgutil.iter_modules(language_configs.__path__):
    full_module_name = f"{language_configs.__name__}.{submodule_name}"
    submodule = importlib.import_module(full_module_name)

    language_config = LanguageConfig(
        language_code=submodule.language_code,
        language_icon=submodule.language_icon,
        chat_config=submodule.ChatConfigImplementation(), 
        gui_text=submodule.GuiTextImplementation(),
    )
    # add to list
    languages.update({language_config.language_code: language_config})


def get_languages() -> list[str]:
    return [cc.get_language_str() for cc in languages.values()]


def get_language_config(language: str) -> LanguageConfig:
    # remove country flag
    language = language[-5:]
    return languages[language]
