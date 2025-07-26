import sys
from argparse import ArgumentParser

import torch

from whisperx_transcribe.infer import main


def cli():
    parser = ArgumentParser(
        description="WhisperX Transcription for Notetaking maniacs and Planners."
    )
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
    parser.add_argument(
        "--max_speakers",
        type=int,
        default=None,
        help="Maximum number of speakers to detect in the audio (default: None, no limit)",
    )
    parser.add_argument(
        "--min_speakers",
        type=int,
        default=1,
        help="Minimum number of speakers to detect in the audio (default: 1)",
    )

    args = parser.parse_args()
    audio_file = args.audio_file
    device = args.device
    batch_size = args.batch_size
    compute_type = args.compute_type
    max_speakers = args.max_speakers
    min_speakers = args.min_speakers

    sys.exit(
        main(
            audio_file=audio_file,
            device=device,
            batch_size=batch_size,
            compute_type=compute_type,
            max_speakers=max_speakers,
            min_speakers=min_speakers,
        )
    )
