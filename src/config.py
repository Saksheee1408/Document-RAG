"""
Configuration module for Doc-RAG.
Handles environment variable loading, default values, and path resolution.
"""

import os
import logging
from dataclasses import dataclass, field
from pathlib import Path
from dotenv import load_dotenv

# Configure standard logger
logger = logging.getLogger("doc_rag.config")


@dataclass
class AppConfig:
    """Application Configuration Settings."""

    # Paths
    base_dir: Path = field(default_factory=lambda: Path(__file__).resolve().parent.parent)
    data_dir: Path = field(default=Path("files"))
    index_dir: Path = field(default=Path("vector_store_data"))

    # LLM Settings
    groq_api_key: str = ""
    groq_model: str = "groq/compound-mini"

    # Embedding Settings
    embedding_model: str = "all-MiniLM-L6-v2"

    # Retrieval Settings
    target_chunk_size: int = 200
    overlap: int = 40
    top_k: int = 4
    similarity_threshold: float = 0.20

    def __post_init__(self):
        # Resolve absolute paths if relative
        if not self.data_dir.is_absolute():
            self.data_dir = (self.base_dir / self.data_dir).resolve()
        if not self.index_dir.is_absolute():
            self.index_dir = (self.base_dir / self.index_dir).resolve()

        # Ensure index directory exists
        self.index_dir.mkdir(parents=True, exist_ok=True)

    @classmethod
    def load_from_env(cls, env_path: str = None) -> "AppConfig":
        """Load configuration from environment variables or .env file."""
        if env_path:
            load_dotenv(dotenv_path=env_path, override=True)
        else:
            load_dotenv(override=False)

        groq_key = os.getenv("GROQ_API_KEY", "").strip()

        # Sanitize placeholder keys
        if groq_key.startswith("your_"):
            groq_key = ""

        try:
            top_k = int(os.getenv("TOP_K", "4"))
        except ValueError:
            logger.warning("Invalid TOP_K in env, defaulting to 4")
            top_k = 4

        try:
            similarity_threshold = float(os.getenv("SIMILARITY_THRESHOLD", "0.35"))
        except ValueError:
            logger.warning("Invalid SIMILARITY_THRESHOLD in env, defaulting to 0.35")
            similarity_threshold = 0.35

        return cls(
            base_dir=Path(__file__).resolve().parent.parent,
            data_dir=Path(os.getenv("DATA_DIR", "files")),
            index_dir=Path(os.getenv("INDEX_DIR", "vector_store_data")),
            groq_api_key=groq_key,
            groq_model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile").strip(),
            embedding_model=os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2").strip(),
            top_k=top_k,
            similarity_threshold=similarity_threshold,
        )

    def validate_groq_key(self) -> bool:
        """Check if a valid Groq API key is configured."""
        if not self.groq_api_key or self.groq_api_key.startswith("your_"):
            return False
        return True
