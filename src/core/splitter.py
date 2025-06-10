from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Iterable

from pydub import AudioSegment
from .utils import convert_to_wav

logger = logging.getLogger(__name__)


class SegmentSplitter:
    """Split audio into segments according to diarization JSON."""

    def run(self, audio_path: Path, diar_json: Path, output_dir: Path) -> Iterable[Path]:
        logger.info("Splitting %s into segments", audio_path)
        segments = json.loads(diar_json.read_text())
        path_to_use = convert_to_wav(audio_path)
        audio = AudioSegment.from_file(path_to_use)
        cleanup = path_to_use != audio_path
        output_dir.mkdir(parents=True, exist_ok=True)
        paths = []
        for i, seg in enumerate(segments):
            start_ms = int(seg["start"] * 1000)
            end_ms = int(seg["end"] * 1000)
            piece = audio[start_ms:end_ms]
            out_path = output_dir / f"segment_{i:04d}.wav"
            piece.export(out_path, format="wav")
            paths.append(out_path)
        logger.info("Saved %d segments to %s", len(paths), output_dir)
        if cleanup:
            Path(path_to_use).unlink(missing_ok=True)
        return paths