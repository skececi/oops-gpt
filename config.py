import abc
import os

import openai
from dotenv import load_dotenv



class Singleton(abc.ABCMeta, type):
    """
    Singleton metaclass for ensuring only one instance of a class.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """Call method for the singleton metaclass."""
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(
                *args, **kwargs)
        return cls._instances[cls]


class Config(metaclass=Singleton):
    """
    Configuration class to store the state from the .env file
    """

    def __init__(self):
        """Initialize the Config class"""
        # if the .env file doesn't exist, create it
        if not os.path.exists(".env"):
            with open(".env", "w") as file:
                file.write("OPENAI_API_KEY=\n")
                file.write("OPENAI_MODEL=gpt-3.5-turbo\n")
        
        load_dotenv()

        self.model = os.getenv("OPENAI_MODEL")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")

        if self.openai_api_key is None or self.openai_api_key == "":
            self.openai_api_key = self.get_user_input_openai_api_key()
        
        openai.api_key = self.openai_api_key
   

    def get_user_input_openai_api_key(self):
        """Set the OpenAI API key from user input"""
        openai_api_key = input("No OpenAI API key found in .env - Enter your OpenAI API key: ")
        os.environ["OPENAI_API_KEY"] = openai_api_key
        # read .env file
        with open(".env", "r") as file:
            lines = file.readlines()
        # replace line that starts with OPENAI_API_KEY=
        with open(".env", "w") as file:
            for line in lines:
                if line.startswith("OPENAI_API_KEY="):
                    line = f"OPENAI_API_KEY={openai_api_key}\n"
                file.write(line)
            # if there was no such line, append it
            if not any(line.startswith("OPENAI_API_KEY=") for line in lines):
                file.write(f"OPENAI_API_KEY={openai_api_key}\n")

        print("OpenAI API key set successfully!")
        return openai_api_key
    
