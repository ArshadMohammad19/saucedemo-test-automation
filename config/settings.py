"""
Central configuration loader.

Combines environment variables (.env) for secrets/environment-specific
values with config.yaml for static, non-secret test settings. Importing
`settings` anywhere in the framework gives a single source of truth.
"""
import os
from pathlib import Path

import yaml
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")


def _load_yaml_config() -> dict:
    config_path = ROOT_DIR / "config" / "config.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


_yaml_config = _load_yaml_config()


class Settings:
    """Read-only view over merged environment + yaml configuration."""

    # --- UI ---
    BASE_URL: str = os.getenv("BASE_URL", "https://www.saucedemo.com")
    BROWSER: str = os.getenv("BROWSER", _yaml_config["browser"]["default"])
    HEADLESS: bool = os.getenv("HEADLESS", "true").lower() == "true"
    SLOW_MO: int = int(os.getenv("SLOW_MO", "0"))

    VIEWPORT_WIDTH: int = _yaml_config["browser"]["viewport"]["width"]
    VIEWPORT_HEIGHT: int = _yaml_config["browser"]["viewport"]["height"]

    # --- API ---
    API_BASE_URL: str = os.getenv("API_BASE_URL", "https://jsonplaceholder.typicode.com")

    # --- Credentials (SauceDemo publishes these test accounts publicly) ---
    STANDARD_USER: str = os.getenv("STANDARD_USER", "standard_user")
    LOCKED_USER: str = os.getenv("LOCKED_USER", "locked_out_user")
    PROBLEM_USER: str = os.getenv("PROBLEM_USER", "problem_user")
    PERFORMANCE_USER: str = os.getenv("PERFORMANCE_USER", "performance_glitch_user")
    PASSWORD: str = os.getenv("PASSWORD", "secret_sauce")

    # --- Timeouts ---
    DEFAULT_TIMEOUT: int = int(
        os.getenv("DEFAULT_TIMEOUT", _yaml_config["timeouts"]["default_ms"])
    )
    NAVIGATION_TIMEOUT: int = int(
        os.getenv("NAVIGATION_TIMEOUT", _yaml_config["timeouts"]["navigation_ms"])
    )

    # --- Retries / reporting (yaml-only, no secrets involved) ---
    MAX_RERUNS: int = _yaml_config["retries"]["max_reruns"]
    RERUN_DELAY: int = _yaml_config["retries"]["rerun_delay_seconds"]
    SCREENSHOT_ON_FAILURE: bool = _yaml_config["reporting"]["screenshot_on_failure"]
    VIDEO_ON_FAILURE: bool = _yaml_config["reporting"]["video_on_failure"]
    TRACE_ON_FAILURE: bool = _yaml_config["reporting"]["trace_on_failure"]

    # --- Inventory test data expectations ---
    EXPECTED_ITEM_COUNT: int = _yaml_config["inventory"]["expected_item_count"]
    EXPECTED_ITEMS: list = _yaml_config["inventory"]["expected_items"]


settings = Settings()
