from abc import ABC, abstractproperty


class GuiTextTemplate(ABC):
    @abstractproperty
    def DOCUMENT(self) -> str:
        pass

    @abstractproperty
    def DOCUMENT_COLLECTION(self) -> str:
        pass

    @abstractproperty
    def LLM_MODEL(self) -> str:
        pass
    @abstractproperty
    def SELECT_DOC_COLXN(self) -> str:
        pass
        
    @abstractproperty
    def SELECT_LLM_MODEL(self) -> str:
        pass
    @abstractproperty
    def SELECT_DOCUMENT(self) -> str:
        pass

    @abstractproperty
    def PROMPT_BOX(self) -> str:
        pass

    @abstractproperty
    def DOWNLOAD_DOCUMENT(self) -> str:
        pass

    @abstractproperty
    def PAGE(self) -> str:
        pass
    @abstractproperty
    def PAGES(self) -> str:
        pass
    @abstractproperty
    def LAST_PAGE(self) ->str:
        pass

    @abstractproperty
    def NEXT_PAGE(self) -> str:
        pass
