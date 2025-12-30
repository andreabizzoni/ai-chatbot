import tiktoken
from docling_core.transforms.chunker.tokenizer.base import BaseTokenizer


class OpenAITokenizer(BaseTokenizer):
    model: str = "text-embedding-3-small"
    max_tokens: int = 8191

    def __init__(
        self, model: str = "text-embedding-3-small", max_tokens: int = 8191, **kwargs
    ):
        super().__init__(max_tokens=max_tokens, **kwargs)
        self.model = model
        self._encoding = tiktoken.encoding_for_model(model)

    def count_tokens(self, text: str) -> int:
        return len(self._encoding.encode(text))

    def get_max_tokens(self) -> int:
        return self.max_tokens

    def get_tokenizer(self):
        return self._encoding
