import whisper
from pyannote.audio import Pipeline
import argparse
import utils
import os  # <-- you need this to use os.getenv

# Set environment variables to avoid symlink issues on Windows
os.environ["SPEECHBRAIN_LOCAL_STRATEGY"] = "COPY"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

# Monkey patch to disable symlink usage completely
import speechbrain.utils.fetching as sb_fetch
from speechbrain.utils.fetching import LocalStrategy

# Force the fetching to use COPY strategy
original_fetch = sb_fetch.fetch
def patched_fetch(*args, **kwargs):
    if 'local_strategy' in kwargs:
        kwargs['local_strategy'] = LocalStrategy.COPY
    else:
        kwargs['local_strategy'] = LocalStrategy.COPY
    return original_fetch(*args, **kwargs)

sb_fetch.fetch = patched_fetch

def main(audio_file, whisper_model_size="base"):
    hf_token = os.getenv("HF_TOKEN")
    if not hf_token:
        raise ValueError("Hugging Face token not found. Set HF_TOKEN as an environment variable.")

    # Load Whisper
    print("Loading Whisper model...")
    whisper_model = whisper.load_model(whisper_model_size)

    # Load Pyannote pipeline
    print("Loading Pyannote pipeline...")
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization@2.1", use_auth_token=hf_token)

    # Run Whisper transcription
    print("Running Whisper transcription...")
    result = whisper_model.transcribe(audio_file)
    transcript = result["text"]

    # Run Pyannote diarization
    print("Running Pyannote diarization...")
    diarization = pipeline(audio_file)

    # Merge results
    merged_transcript = utils.merge_diarization_with_transcript(diarization, transcript)

    # Print results
    print("\n===== MERGED TRANSCRIPT =====\n")
    for entry in merged_transcript:
        print(f"[{entry['speaker']}] {entry['text']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Whisper + Pyannote transcriber")
    parser.add_argument("audio_file", type=str, help="Path to audio file")
    parser.add_argument("--whisper_model", type=str, default="base", help="Whisper model size (tiny, base, small, medium, large)")
    args = parser.parse_args()

    main(args.audio_file, args.whisper_model)
