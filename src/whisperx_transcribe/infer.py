import datetime
import gc
import json
import logging

import torch
import utils as ut
import whisperx

logger = logging.getLogger(__name__)

device = "cuda"
audio_file = "assets/sample/audio.mp3"
batch_size = 8  # reduce if low on GPU mem
compute_type = "int8"  # change to "int8" if low on GPU mem (may reduce accuracy)
start_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
audio_path = audio_file.split(".")[0]
audio_stem = audio_path.split("/")[-1]

format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
file_handler = logging.FileHandler(f"logs/{audio_stem}_{start_time}.log", mode="w")
file_handler.setFormatter(logging.Formatter(format))
logger.addHandler(file_handler)

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

# delete model if low on GPU resources
gc.collect()
torch.cuda.empty_cache()
del model

# 2. Align whisper output
model_a, metadata = whisperx.load_align_model(
    language_code=result["language"], device=device
)
result = whisperx.align(
    result["segments"], model_a, metadata, audio, device, return_char_alignments=False
)

logger.info("Transcription alignment complete")  # after alignment

# delete model if low on GPU resources

gc.collect()
torch.cuda.empty_cache()
del model_a

# 3. Assign speaker labels
diarize_model = whisperx.diarize.DiarizationPipeline(
    use_auth_token=ut.parse_token(), device=device
)

# add min/max number of speakers if known
diarize_segments = diarize_model(audio)
# diarize_model(audio, min_speakers=min_speakers, max_speakers=max_speakers)
logger.info("Speaker diarization complete")

result = whisperx.assign_word_speakers(diarize_segments, result)

# write json to file
with open(f"{audio_path}_diarized.json", "w") as f:
    json.dump(result, f, indent=4)

logger.info(f"Diarized results saved to {audio_path}_diarized.json")

# 4. Write segments to file
with open(f"{audio_path}_segments.txt", "w") as f:
    for segment in result["segments"]:
        f.write(f"{segment['start']:.2f} --> {segment['end']:.2f}\n")
        f.write(f"{segment['text']}\n\n")

logger.info(f"Segments saved to {audio_path}_segments.txt")
