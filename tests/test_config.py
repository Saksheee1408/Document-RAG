"""
Unit tests for configuration loading and validation.
"""

import os
from src.config import AppConfig


def test_config_defaults():
    config = AppConfig()
    assert config.top_k == 4
    assert config.similarity_threshold == 0.20
    assert config.groq_model == "groq/compound-mini"
    assert config.embedding_model == "all-MiniLM-L6-v2"


def test_config_from_env(tmp_path, monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "test_key_123")
    monkeypatch.setenv("TOP_K", "6")
    monkeypatch.setenv("SIMILARITY_THRESHOLD", "0.42")

    config = AppConfig.load_from_env()
    assert config.groq_api_key == "test_key_123"
    assert config.top_k == 6
    assert config.similarity_threshold == 0.42
    assert config.validate_groq_key() is True


def test_invalid_groq_key():
    config = AppConfig(groq_api_key="your_groq_api_key_here")
    assert config.validate_groq_key() is False
