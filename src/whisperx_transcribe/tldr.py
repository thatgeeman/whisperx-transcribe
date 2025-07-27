import json
import os
from datetime import datetime

from langchain_core.prompts import PromptTemplate
from llama_index.core import Settings
from llama_index.llms.ollama import Ollama

import whisperx_transcribe.utils as ut
from whisperx_transcribe import logger, start_time

max_workers = os.cpu_count()


def prompter():
    prompt_template = PromptTemplate(
        template=instructions,
        template_format="jinja2",
        input_variables=["transcript"],
    )
    logger.info(f"Segments loaded: {len(grouped_segments)}")

    prompt = prompt_template.format(transcript=json.dumps(grouped_segments, indent=2))
    logger.info(f"Prompting with the following prompt:\n{prompt}")
    #! change to chat model with chat summary
    response = llm.complete(prompt, formatted=True)
    return response


if __name__ == "__main__":
    HISTORY = ".history"
    PROMPT_FILE = "prompts/instructions_01.md"
    SEG_FILE = "assets/sample/audio_diarized.json"
    GROUP_SEG_FILE = f"{SEG_FILE.split('.')[0]}_grouped.json"
    model = "qwen2.5-coder:3b-instruct-q8_0"  # gemma3:1b

    segments = ut.load_segments(segments_file=SEG_FILE)
    grouped_segments = ut.group_speakers(segments=segments, speaker_names={})
    with open(GROUP_SEG_FILE, "w") as f:
        json.dump(grouped_segments, f, indent=4)

    with open(PROMPT_FILE, "r") as f:
        instructions = f.read()

    llm = Ollama(model=model, request_timeout=1000)
    Settings.llm = llm

    logger.info(f"LLM initialized with model: {model}")
    response = prompter()
    # logger.info(response.text)
    logger.info(f"Response from LLM:\n{response.text}")
    logger.info("Summary generation complete.")
    logger.info(f"Total time taken {datetime.now() - start_time}")
