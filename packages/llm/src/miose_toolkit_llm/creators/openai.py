from typing import Any, Dict, List, Literal, Optional, Tuple

from ..exceptions import ArgumentTypeError, RenderPromptError
from .base import BasePromptCreator


class _Message:
    role: Literal["system", "user", "assistant"]

    def __init__(self, *args, sep: str = "\n"):
        self.message_segments: Tuple[Any] = args
        self.sep: str = sep

    @property
    def message_text(self) -> str:
        return self.sep.join([str(m) for m in self.message_segments])

    def to_dict(self) -> Dict[str, str]:
        return {"role": self.role, "message": self.message_text}


class SystemMessage(_Message):
    role = "system"


class UserMessage(_Message):
    role = "user"


class AiMessage(_Message):
    role = "assistant"


class OpenAIPromptCreator(BasePromptCreator):

    messages: List[_Message]
    temperature: Optional[float]
    top_p: Optional[float]
    presence_penalty: Optional[float]
    frequency_penalty: Optional[float]
    max_tokens: Optional[int]
    stop_words: Optional[List[str]]

    def __init__(
        self,
        *args,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        presence_penalty: Optional[float] = None,
        frequency_penalty: Optional[float] = None,
        max_tokens: Optional[int] = None,
        stop_words: Optional[List[str]] = None,
    ) -> None:
        self.messages = []
        for arg in args:
            if isinstance(arg, _Message):
                self.messages.append(arg)
            else:
                raise ArgumentTypeError("Invalid message type")
        self.temperature = temperature
        self.top_p = top_p
        self.presence_penalty = presence_penalty
        self.frequency_penalty = frequency_penalty
        self.max_tokens = max_tokens
        self.stop_words = stop_words

    # Override
    def render(self) -> List[Dict[str, str]]:
        try:
            return [m.to_dict() for m in self.messages]
        except Exception as e:
            raise RenderPromptError(f"Error rendering prompt: {e}") from e
