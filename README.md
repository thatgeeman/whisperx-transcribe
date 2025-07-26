# Notes

## Usage

For sample audio placed in `assets/sample`

```
python src/whisperx_transcribe/infer.py assets/sample/audio.mp3
```

## Info

Cluster backend at work does not support float16 computation (Quadro P4000)

## Environment Setup

Python 3.10.

Install `ffmpeg`, `rust`, `cudnn=8.9.7` from conda.

Future me: `conda install cudnn=8.9.7` installed:

```
cuda-nvrtc-12.9.86
cuda-version-12.9
cudnn-8.9.7.29
libcublas-12.9.1.4
libcudnn-8.9.7.29
libcudnn-dev-8.9.7.29
```

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

## Video to mp3

To strip audio (mp3) from video file, you can use the following command:

```bash
ffmpeg -i input_video.mp4 -f mp3 -vn -ar 44100 output_audio.mp3
```

- `-vn` disables video recording, `-ar` sets the audio sample rate.
- `-f mp3` specifies the output format as mp3.
