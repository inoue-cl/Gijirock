from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Optional

from pyannote.audio import Pipeline
from .utils import convert_to_wav

logger = logging.getLogger(__name__)


class Diarizer:
    """Run speaker diarization using pyannote.audio."""

    def __init__(self, token: str) -> None:
        self.token = token

    def run(self, audio_path: Path, output_json: Path) -> Path:
        """Run diarization and save the result as JSON."""
        logger.info("Running diarization on %s", audio_path)
        tmp_path = None
        path_to_use = audio_path
        if audio_path.suffix.lower() in {".m4a", ".mp3"}:
            path_to_use = convert_to_wav(audio_path)
            if path_to_use != audio_path:
                tmp_path = path_to_use

        pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization@2.1", use_auth_token=self.token
        )
        diarization = pipeline(path_to_use)
        if tmp_path is not None:
            tmp_path.unlink(missing_ok=True)
        segments = [
            {
                "start": s.start,
                "end": s.end,
                "speaker": s.track,
            }
            for s in diarization.itertracks(yield_label=True)
        ]
        output_json.write_text(json.dumps(segments, indent=2))
        logger.info("Diarization saved to %s", output_json)
        return output_json
