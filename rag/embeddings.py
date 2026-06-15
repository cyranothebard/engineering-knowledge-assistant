from __future__ import annotations

import hashlib
import math
import re

from langchain_core.embeddings import Embeddings
from langchain_openai import OpenAIEmbeddings

from app.settings import Settings


class LocalHashEmbeddings(Embeddings):
    def __init__(self, dimensions: int = 256) -> None:
        self.dimensions = dimensions

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self._embed(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._embed(text)

    def _embed(self, text: str) -> list[float]:
        vector = [0.0] * self.dimensions
        tokens = re.findall(r"[a-zA-Z0-9äöüß]+", text.lower())
        for token in tokens:
            digest = hashlib.blake2b(token.encode("utf-8"), digest_size=8).digest()
            slot = int.from_bytes(digest[:4], "big") % self.dimensions
            sign = 1.0 if digest[4] % 2 == 0 else -1.0
            vector[slot] += sign

        magnitude = math.sqrt(sum(value * value for value in vector)) or 1.0
        return [value / magnitude for value in vector]


def get_embedding_backend(settings: Settings) -> Embeddings:
    if settings.openai_api_key:
        return OpenAIEmbeddings(model=settings.openai_embedding_model)
    return LocalHashEmbeddings()
