from abc import ABC, abstractproperty


class ChatConfig(ABC):

    @abstractproperty
    def language_code(self) -> str:
        pass

    @abstractproperty
    def language_icon(self) -> str:
        pass

    def get_language_str(self) -> str:
        return f"{self.language_icon} {self.language_code}"

    @abstractproperty
    def AI_NAME(self) -> str:
        pass

    @abstractproperty
    def USER_NAME(self) -> str:
        pass

    @abstractproperty
    def DB_QUERY_GEN_PROMPT(self) -> str:
        pass

    @abstractproperty
    def HISTORY_MESSAGE_FORMATTING(self) -> str:
        pass

    @abstractproperty
    def INITIAL_CHAT_HISTORY(self) -> list[dict[str, str]]:
        pass

    @abstractproperty
    def PROMPT_SOURCES_WRAPPER(self) -> str:
        pass

    @abstractproperty
    def PROMPT_WRAPPER(self) -> str:
        pass

    @abstractproperty
    def SOURCES_FORMATTING(self) -> str:
        pass

    @abstractproperty
    def SOURCE_DOC_FORMATTING(self) -> str:
        pass
