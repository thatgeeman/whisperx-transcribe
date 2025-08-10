# Notes

> This is still a WIP as of 10.08.2025 

WhisperX Transcription for Notetaking maniacs and Planners.

## Usage

After cloning the repo and setting up the env: `pip install .` to install `wxt` command.

For sample audio placed in `assets/sample`

```
wxt assets/sample/audio.mp3
```

For other supported options see `wxt --help`.


### Models 

- Summarization model: Any available on Ollama (developed with `gemma3:4b`)
- Transcription model: WhisperX Large v3
- Diarization model: 
  
In retrieval mode, based on [MTEB ranking](https://huggingface.co/spaces/mteb/leaderboard): 
- Text embedding model: Qwen3-Embedding-0.6B

## Info

Cluster backend at work does not support float16 computation (Quadro P4000)

## Environment Setup

Python 3.10.

Install `ffmpeg`, `rust`, `cudnn=8.9.7` (`faster-whisper-large-v3` looks for `libcudnn_ops_infer.so.8).

Setup `ollama` based on latest instructions from https://github.com/ollama/ollama/tree/main/docs

See `pyproject.toml` for python dependencies.

## HuggingFace

Accept terms for

- https://huggingface.co/pyannote/speaker-diarization-3.1
- https://huggingface.co/pyannote/segmentation-3.0

Add huggingface token to `.env` file:

```
MY_TOKEN=hf_xxx
```

## Alternatives

Replicate provides inference. See [colab](https://colab.research.google.com/drive/1FH50NOULkMUawgvXR7H9gSc4LpDaM5H8).

Freemium (referral): [Otter.ai](https://otter.ai/referrals/AFSQ9M7B)

## Video to mp3

To strip audio (mp3) from video file, you can use the following command:

```bash
ffmpeg -i input_video.mp4 -f mp3 -vn -ar 44100 output_audio.mp3
```

- `-vn` disables video recording, `-ar` sets the audio sample rate.
- `-f mp3` specifies the output format as mp3.


## Troubleshooting

- `ctranslate2`: `ImportError: libctranslate2-d3638643.so.4.4.0: cannot enable executable stack as shared object requires: Invalid argument` shared object error. Fixed this issue with [this](https://github.com/OpenNMT/CTranslate2/issues/1849#issuecomment-2664106316) on Manjaro-xfce.

- If the `huggingface_hub` download takes longer, found that it was easier to just [clone](https://huggingface.co/Systran/faster-whisper-large-v3/tree/main?clone=true) the repo, for example with their cli: `hf download Systran/faster-whisper-large-v3` and place it in the `cache_dir`, `model/` in this case. The `faster-whisper` also depends on an older `huggingface_hub` version that does not come with `xet`. The download only appears slower due to an inner loop with tqdm, which sometimes does not appear to update the outer, main progress bar -- probably related to `xet`'s chunked downloads.