import gc
import json
import logging
import os
from typing import Dict, Generator, List

import torch
from dotenv import load_dotenv
from llama_index.core import Document

load_dotenv()

logger = logging.getLogger("whisperx_transcribe")


def parse_token():
    """
    Parse the authentication token from the environment variable.
    """
    token = os.environ.get("MY_TOKEN")
    if not token:
        raise ValueError(
            "Authentication token `MY_TOKEN` is not set in the `.env` file."
        )
    if not token.startswith("hf_"):
        raise ValueError(
            "Authentication token should start with 'hf_'. Please check your `.env` file."
        )
    return token


def load_segments(segments_file):
    """
    Load segments from a JSON file.
    """
    try:
        with open(segments_file, "r") as file:
            segments = json.load(file)["segments"]
    except Exception as e:
        logging.info(f"Error loading segments from {segments_file}: {e}")
    return segments


def labeled_segment(segment, speaker_names: dict = {}) -> Dict[str, str]:
    """
    Convert a segment to a labeled dictionary with start, end, speaker, and text.
    """
    if len(segment["words"]) <= 2:
        return {
            "start": segment["start"],
            "end": segment["end"],
            "speaker": "",
            "text": "",
        }
    if "speaker" not in segment:
        segment["speaker"] = ""
    if "text" not in segment:
        segment["text"] = ""

    start_timestamp = segment["start"]
    end_timestamp = segment["end"]
    speaker = segment["speaker"]
    alt_speaker_name = speaker_names.get(speaker, speaker)
    text = segment["text"]

    return {
        "start": start_timestamp,
        "end": end_timestamp,
        "speaker": alt_speaker_name,
        "text": text.strip(),
    }


def get_segment_iterator(
    segments, speaker_names: dict = {}
) -> Generator[Dict[str, str], None, None]:
    return (labeled_segment(segment, speaker_names) for segment in segments)


def group_speakers(segments, speaker_names: dict = {}) -> List[Dict[str, str]]:
    """Merges consequent dialogues by the same speaker"""
    speaker_texts = []
    prev_p = {"speaker": "", "text": ""}
    for p in get_segment_iterator(segments, speaker_names):
        if p["speaker"] == prev_p["speaker"]:
            # join texts of the same speaker and update end time
            prev_p["text"] += " " + p["text"]
            prev_p["end"] = p["end"]
        else:
            speaker_texts.append(p)
            prev_p = p
    return speaker_texts


def speaker_segment(segment_text: Dict[str, str], turn_id: int = 0) -> Document:
    """
    Format a segment text for prompting and prepare a LlamaIndex Document object.
    Also adds the metadata field to specify the person to whom the transcript belongs.

    """
    start_time = segment_text["start"]
    end_time = segment_text["end"]
    speaker = segment_text["speaker"]
    text = segment_text["text"]
    human_ts = f"{start_time}s:{end_time}s"
    body = f"[{human_ts}] **{speaker}**: {text}"
    return Document(
        text=body,
        metadata={
            "speaker": speaker,
            "timestamp_s": start_time,
            "turn_id": turn_id,
        },
    )


def get_all_speakers(segments: List[Dict[str, str]]) -> List[str]:
    """
    Extract all unique speakers from the segments.
    """
    speakers = set()
    for segment in segments:
        if "speaker" in segment and segment["speaker"]:
            speakers.add(segment["speaker"])
    return list(speakers)


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
