import tiktoken
from docling_core.transforms.chunker.base import BaseTokenizer


class OpenAITokenizer(BaseTokenizer):
    def __init__(self, model: str = "text-embedding-3-small"):
        self.encoding = tiktoken.encoding_for_model(model)

    def count_tokens(self, text: str) -> int:
        return len(self.encoding.encode(text))
