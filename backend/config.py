"""
Strategic AI Core Backend
Configuration loader
"""

import os
from pathlib import Path

import yaml

CONFIG_PATH = Path(__file__).resolve().parent.parent / "project_config.yaml"


def load_config(path: Path = CONFIG_PATH) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)


def get_env(name: str, default: str = None) -> str:
    return os.environ.get(name, default)


config = load_config()
llm_config = config.get("llm", {})

ANTHROPIC_API_KEY = get_env("ANTHROPIC_API_KEY")
