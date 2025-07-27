import json
from datetime import datetime

import whisperx
from whisperx.utils import get_writer

import whisperx_transcribe.utils as ut
from whisperx_transcribe import logger, start_time


def main(audio_file, device, batch_size, compute_type, max_speakers, min_speakers):
    audio_path = audio_file.split(".")[0]
    audio_parent = audio_path.rsplit("/", 1)[0]

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

    # Align whisper output → second model for CTC alignment
    model_alignment, metadata = whisperx.load_align_model(
        language_code=result["language"], device=device
    )
    result_aligned = whisperx.align(
        result["segments"],
        model_alignment,
        metadata,
        audio,
        device,
        return_char_alignments=False,
    )

    logger.info("Transcription alignment complete")  # after alignment

    # delete model if low on GPU resources
    ut.cleanup(model_alignment)

    writer = get_writer("srt", output_dir=audio_parent)
    """ 
    max_line_width: the maximum number of characters in a line before breaking the line
    max_line_count: the maximum number of lines in a segment
    highlight_words: underline each word as it is spoken in srt and vtt
    """
    result_aligned["language"] = result["language"]
    with open(f"{audio_path}_sub.srt", "w") as file_out:
        writer.write_result(
            result=result_aligned,
            file=file_out,
            options={
                "max_line_width": None,
                "max_line_count": None,
                "highlight_words": False,
            },
        )
    logger.info(f"Subtitles saved to {audio_path}_sub.srt")

    # Diarization
    diarize_model = whisperx.diarize.DiarizationPipeline(
        use_auth_token=ut.parse_token(), device=device
    )
    diarize_segments = diarize_model(
        audio, min_speakers=min_speakers, max_speakers=max_speakers
    )
    logger.info("Speaker diarization complete")

    # we get "word_segments" and "segments" in this result, others are lost
    result_diarized = whisperx.assign_word_speakers(diarize_segments, result_aligned)
    # write json to file
    with open(f"{audio_path}_diarized.json", "w") as f:
        json.dump(result_diarized, f, indent=4)

    ut.cleanup(diarize_model)
    logger.info(f"Diarized results saved to {audio_path}_diarized.json")
    logger.info("Transcription and diarization complete")
    logger.info(f"Total time taken: {datetime.now() - start_time}")
    return 0
