def merge_diarization_with_transcript(diarization, transcript):
    """
    Naive merge of diarization and transcript.
    Right now this just assigns transcript chunks to speaker turns.
    Later, can be improved with word-level alignment.
    """
    merged = []
    transcript_chunks = transcript.split(". ")  # rough split into sentences
    speakers = [label for _, _, label in diarization.itertracks(yield_label=True)]

    for i, chunk in enumerate(transcript_chunks):
        speaker = speakers[i % len(speakers)]  # rotate through speakers
        merged.append({
            "speaker": speaker,
            "text": chunk.strip()
        })
    return merged
