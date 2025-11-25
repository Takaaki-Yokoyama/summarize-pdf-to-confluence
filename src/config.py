"""Configuration module for loading environment variables."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass
class Config:
    """Configuration class for storing API keys and settings."""

    gemini_api_key: str
    confluence_url: str
    confluence_username: str
    confluence_api_token: str
    confluence_space_key: str

    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment variables.

        Returns:
            Config: Configuration object with all required settings.

        Raises:
            ValueError: If any required environment variable is missing.
        """
        load_dotenv()

        gemini_api_key = os.getenv("GEMINI_API_KEY")
        confluence_url = os.getenv("CONFLUENCE_URL")
        confluence_username = os.getenv("CONFLUENCE_USERNAME")
        confluence_api_token = os.getenv("CONFLUENCE_API_TOKEN")
        confluence_space_key = os.getenv("CONFLUENCE_SPACE_KEY")

        missing_vars = []
        if not gemini_api_key:
            missing_vars.append("GEMINI_API_KEY")
        if not confluence_url:
            missing_vars.append("CONFLUENCE_URL")
        if not confluence_username:
            missing_vars.append("CONFLUENCE_USERNAME")
        if not confluence_api_token:
            missing_vars.append("CONFLUENCE_API_TOKEN")
        if not confluence_space_key:
            missing_vars.append("CONFLUENCE_SPACE_KEY")

        if missing_vars:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_vars)}"
            )

        return cls(
            gemini_api_key=gemini_api_key,
            confluence_url=confluence_url,
            confluence_username=confluence_username,
            confluence_api_token=confluence_api_token,
            confluence_space_key=confluence_space_key,
        )
