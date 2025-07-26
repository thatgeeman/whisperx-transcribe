# Notes

Cluster backend does not support efficient float16 computation.

- Quadro P4000

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
