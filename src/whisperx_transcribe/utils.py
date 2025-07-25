import os

from dotenv import load_dotenv

load_dotenv()


def parse_token():
    """
    Parse the authentication token from the environment variable.
    """
    token = os.getenv("MY_TOKEN")
    if not token:
        raise ValueError("Authentication token is not set.")
    return f"hf_{token}"
