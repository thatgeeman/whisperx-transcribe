"""
Meant to work with context stuffed prompting as per instructions
here prompts/instructions_01.md to create action items.
"""

import json
import os
from datetime import datetime

from langchain_core.prompts import PromptTemplate
from llama_index.core import Settings
from llama_index.llms.ollama import Ollama

import whisperx_transcribe.utils as ut
from whisperx_transcribe import logger, start_time

max_workers = os.cpu_count()


def simple_prompter(instructions, segments, log_params: dict = {}):
    prompt_template = PromptTemplate(
        template=instructions,
        template_format="jinja2",
        input_variables=["transcript"],
    )
    logger.info(f"Segments loaded: {len(segments)}")

    prompt = prompt_template.format(transcript=json.dumps(segments, indent=2))

    truncate_prompt_at = log_params["truncate_prompt_at"]
    logger.info(
        f"Prompting with the following prompt:\n{prompt[:truncate_prompt_at]}..."
    )
    # ! change to chat model with chat summary
    response = llm.complete(prompt, formatted=True)
    return response


if __name__ == "__main__":
    HISTORY = ".history"
    PROMPT_FILE = "prompts/instructions_01.md"
    SEG_FILE = "assets/sample/audio_diarized.json"
    GROUP_SEG_FILE = f"{SEG_FILE.split('.')[0]}_grouped.json"
    truncate_prompt_at = 200
    model = "gemma3:4b"  # gemma3:1b
    logger.info(f"Using audio segments file: {SEG_FILE} to merge consequent dialogues.")
    segments = ut.load_segments(segments_file=SEG_FILE)

    grouped_segments = ut.group_speakers(segments=segments, speaker_names={})
    with open(GROUP_SEG_FILE, "w") as f:
        json.dump(grouped_segments, f, indent=4)
    logger.info(
        f"Prepared merged dialogues files: {GROUP_SEG_FILE} with {len(grouped_segments)} segments"
    )
    logger.info(f"Loading prompts: {PROMPT_FILE} and model: {model}")
    with open(PROMPT_FILE, "r") as f:
        instructions = f.read()
    llm = Ollama(model=model, request_timeout=1000)
    Settings.llm = llm
    logger.info(f"Initialized with model: {model}")
    response = simple_prompter(
        instructions,
        grouped_segments,
        # ! make a config file
        log_params={
            "truncate_prompt_at": truncate_prompt_at,
        },
    )
    # logger.info(response.text)
    logger.info(f"Response from LLM:\n{response.text}")
    logger.info("Summary generation complete.")
    logger.info(f"Total time taken {datetime.now() - start_time}")
