from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Optional

from pyannote.audio import Pipeline

logger = logging.getLogger(__name__)


class Diarizer:
    """Run speaker diarization using pyannote.audio."""

    def __init__(self, token: str) -> None:
        self.token = token

    def run(self, audio_path: Path, output_json: Path) -> Path:
        """Run diarization and save the result as JSON."""
        logger.info("Running diarization on %s", audio_path)
        pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization@2.1", use_auth_token=self.token
        )
        diarization = pipeline(audio_path)
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
