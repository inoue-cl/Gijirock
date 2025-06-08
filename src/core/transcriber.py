from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Iterable

import whisper
from tqdm import tqdm

logger = logging.getLogger(__name__)


class Transcriber:
    """Transcribe audio segments with Whisper."""

    def __init__(self, model: str = "base") -> None:
        self.model = whisper.load_model(model)

    def run(self, segments_dir: Path, output_json: Path) -> Path:
        logger.info("Transcribing segments in %s", segments_dir)
        results = []
        for wav in tqdm(sorted(segments_dir.glob("*.wav"))):
            transcription = self.model.transcribe(str(wav))
            results.append({"file": wav.name, "text": transcription["text"]})
        output_json.write_text(json.dumps(results, indent=2))
        logger.info("Transcriptions saved to %s", output_json)
        return output_json
