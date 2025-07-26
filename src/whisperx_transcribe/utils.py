import os

from dotenv import load_dotenv

load_dotenv()


def parse_token():
    """
    Parse the authentication token from the environment variable.
    """
    token = os.getenv("MY_TOKEN")
    if not token:
        raise ValueError(
            "Authentication token `MY_TOKEN` is not set in the `.env` file."
        )
    if not token.startswith("hf_"):
        raise ValueError(
            "Authentication token should start with 'hf_'. Please check your `.env` file."
        )
    return token
