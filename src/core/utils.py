from __future__ import annotations

from pathlib import Path
from tempfile import NamedTemporaryFile

from pydub import AudioSegment


def convert_to_wav(audio_path: Path) -> Path:
    """Convert input audio to WAV if needed and return path."""
    if audio_path.suffix.lower() == ".wav":
        return audio_path
    tmp = NamedTemporaryFile(suffix=".wav", delete=False)
    tmp_path = Path(tmp.name)
    tmp.close()
    AudioSegment.from_file(audio_path).export(tmp_path, format="wav")
    return tmp_path
