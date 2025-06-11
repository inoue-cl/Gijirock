from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Optional

import os
from pyannote.audio import Pipeline

from .utils import convert_to_wav

logger = logging.getLogger(__name__)


class Diarizer:
    """Run speaker diarization using the Hugging Face API."""

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

        # 環境変数からトークンを取得
        token = os.environ["HF_TOKEN"]

        # ローカル推論用 Pipeline インスタンスの作成
        pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization",
            use_auth_token=token,
        )

        # 音声ファイルを入力して推論実行
        diar = pipeline(str(path_to_use))

        if tmp_path is not None:
            tmp_path.unlink(missing_ok=True)

        # JSON形式で出力
        with open(output_json, "w") as f:
            f.write(diar.to_json())
        logger.info("Diarization saved to %s", output_json)
        return output_json
