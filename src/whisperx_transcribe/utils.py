import gc
import logging
import os

import torch
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("whisperx_transcribe")


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


def cleanup(obj):
    """Cleanup function to free up resources."""
    if isinstance(obj, torch.Tensor):
        torch.cuda.empty_cache()
        del obj
    elif isinstance(obj, torch.nn.Module):
        for param in obj.parameters():
            if param.grad is not None:
                param.grad.detach_()
                param.grad.zero_()
        del obj

    gc.collect()
    logger.info("Cleanup complete.")
