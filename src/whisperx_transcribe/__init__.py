import logging
import sys
from datetime import datetime
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

start_time = datetime.now()


def get_version():
    try:
        return version("whisperx-transcribe")
    except PackageNotFoundError:
        return "0.0.0+local"


def get_logger():
    version = get_version()
    logger = logging.getLogger("whisperx_transcribe")
    logger.setLevel(logging.INFO)
    format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Stream handler
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setFormatter(format)
    logger.addHandler(stream_handler)

    # File handler
    start_time_s = start_time.strftime("%Y-%m-%d_%H-%M-%S")
    Path("logs").mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(
        f"logs/WXTv{version}_{start_time_s}.log", mode="w"
    )
    file_handler.setFormatter(format)
    logger.addHandler(file_handler)

    return logger


__version__ = get_version()
logger = get_logger()
