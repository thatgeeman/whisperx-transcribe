import datetime
import json
import logging
import sys
from argparse import ArgumentParser

import torch
import utils as ut
import whisperx
from whisperx.utils import get_writer

logger = logging.getLogger("whisperx_transcribe")


parser = ArgumentParser(description="WhisperX Transcription and Diarization")
parser.add_argument(
    "audio_file",
    type=str,
    help="Path to the audio file to transcribe and diarize",
    default="assets/sample/audio.mp3",
)
parser.add_argument(
    "--device",
    type=str,
    default="cuda" if torch.cuda.is_available() else "cpu",
    help="Device to run the model on (default: cuda if available, else cpu)",
)
parser.add_argument(
    "--batch_size",
    type=int,
    default=8,
    help="Batch size for processing audio (default: 8)",
)
parser.add_argument(
    "--compute_type",
    type=str,
    default="int8",
    choices=["float16", "float32", "int8"],
    help="Compute type for the model (default: int8, change to float16 if low on GPU memory)",
)

args = parser.parse_args()
audio_file = args.audio_file
device = args.device
batch_size = args.batch_size
compute_type = args.compute_type

start_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
audio_path = audio_file.split(".")[0]
audio_parent = audio_path.rsplit("/", 1)[0]
audio_stem = audio_path.split("/")[-1]

format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler = logging.FileHandler(f"logs/{audio_stem}_{start_time}.log", mode="w")
file_handler.setFormatter(format)
stream_handler = logging.StreamHandler(stream=sys.stdout)
stream_handler.setFormatter(format)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

logger.setLevel(logging.INFO)

logger.info(
    f"Transcribing {audio_file} with batch size {batch_size} and compute type {compute_type}"
)

# save model to local path (optional)
model_dir = "model/"
model = whisperx.load_model(
    "large-v2", device, compute_type=compute_type, download_root=model_dir
)

audio = whisperx.load_audio(audio_file)
result = model.transcribe(audio, batch_size=batch_size)
logger.info("Transcription complete")

ut.cleanup(model)

# 2. Align whisper output
model_a, metadata = whisperx.load_align_model(
    language_code=result["language"], device=device
)
result = whisperx.align(
    result["segments"], model_a, metadata, audio, device, return_char_alignments=False
)

logger.info("Transcription alignment complete")  # after alignment

# delete model if low on GPU resources
ut.cleanup(model_a)

# 3. Assign speaker labels
diarize_model = whisperx.diarize.DiarizationPipeline(
    use_auth_token=ut.parse_token(), device=device
)

# add min/max number of speakers if known
diarize_segments = diarize_model(audio)
# diarize_model(audio, min_speakers=min_speakers, max_speakers=max_speakers)
logger.info("Speaker diarization complete")

result = whisperx.assign_word_speakers(diarize_segments, result)

writer = get_writer("srt", output_dir=audio_parent)
writer.write_result(
    result=result,
    file=f"{audio_path}_sub.srt",
    options={
        """
        # Options from the cli
        max_line_width: (not possible with --no_align) the maximum number of characters in a line before breaking the line
        max_line_count: (not possible with --no_align) the maximum number of lines in a segment
        "highlight_words: (not possible with --no_align) underline each word as it is spoken in srt and vtt
        """
        "max_line_width": None,
        "max_line_count": None,
        "highlight_words": False,
    },
)
logger.info(f"Subtitles saved to {audio_path}_sub.srt")

# write json to file
with open(f"{audio_path}_diarized.json", "w") as f:
    json.dump(result, f, indent=4)

logger.info(f"Diarized results saved to {audio_path}_diarized.json")
