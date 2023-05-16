from dotenv import load_dotenv
import os

import openai

load_dotenv()

class Config():
    """
    Configuration class to store the state from the .env file
    """

    def __init__(self):
        """Initialize the Config class"""

        self.model = os.getenv("OPENAI_MODEL")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")

        # Initialize the OpenAI API client
        openai.api_key = self.openai_api_key



    def set_continuous_mode(self, value: bool):
        """Set the continuous mode value."""
        self.continuous_mode = value