import os
from dotenv import load_dotenv

class AppConfig:
    """
    A Configuration Manager class to securely handle API keys and settings.
    Follows encapsulation principles by keeping validation internal.
    """
    def __init__(self):
        load_dotenv()
        self.llm_api_key = self._get_env_var("GROQ_API_KEY")
        self.langsmith_api_key = self._get_env_var("LANGSMITH_API_KEY")
    def _get_env_var(self, var_name: str) -> str:
        """Private method to fetch and validate environment variables."""
        value = os.getenv(var_name)
        if not value:
            raise ValueError(f"Configuration Error: Missing {var_name} in environment variables.")
        return value

config = AppConfig()