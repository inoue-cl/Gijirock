from __future__ import annotations

import json
import logging
from pathlib import Path
import time

import requests
from .utils import convert_to_wav

logger = logging.getLogger(__name__)


class Diarizer:
    """Run speaker diarization using the Hugging Face API."""

    def __init__(
        self,
        token: str,
        model: str = "pyannote/speaker-diarization@2023.07",
        use_gpu: bool = False,
    ) -> None:
        self.token = token
        self.model = model
        self.use_gpu = use_gpu

    def run(self, audio_path: Path, output_json: Path) -> Path:
        """Run diarization and save the result as JSON."""
        logger.info("Running diarization on %s", audio_path)
        tmp_path = None
        path_to_use = audio_path
        if audio_path.suffix.lower() in {".m4a", ".mp3"}:
            path_to_use = convert_to_wav(audio_path)
            if path_to_use != audio_path:
                tmp_path = path_to_use

        with open(path_to_use, "rb") as f:
            data_bytes = f.read()

        url = f"https://api-inference.huggingface.co/models/{self.model}"
        headers = {"Authorization": f"Bearer {self.token}"}
        params = {"use_gpu": str(self.use_gpu).lower(), "wait_for_model": "true"}

        response = None
        try:
            response = requests.post(url, headers=headers, params=params, data=data_bytes)
            while response.status_code == 202:
                # model is loading
                logger.info("Model loading, waiting...")
                time.sleep(5)
                response = requests.post(url, headers=headers, params=params, data=data_bytes)
            response.raise_for_status()
        except requests.RequestException as exc:
            logger.error("Diarization request failed: %s", exc)
            raise
        if tmp_path is not None:
            tmp_path.unlink(missing_ok=True)
        data = response.json()
        segments = [
            {
                "start": seg.get("start"),
                "end": seg.get("end"),
                "speaker": seg.get("label", ""),
            }
            for seg in data.get("segments", data)
        ]
        output_json.write_text(json.dumps(segments, indent=2))
        logger.info("Diarization saved to %s", output_json)
        return output_json
