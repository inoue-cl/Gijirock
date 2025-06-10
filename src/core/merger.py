from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Dict

logger = logging.getLogger(__name__)


class Merger:
    """Merge diarization and transcription results."""

    def run(
        self,
        diar_json: Path,
        trans_json: Path,
        mapping: Dict[str, str],
        output_txt: Path,
    ) -> Path:
        diar = json.loads(diar_json.read_text())
        trans = {t["file"]: t["text"] for t in json.loads(trans_json.read_text())}
        lines = []
        for i, seg in enumerate(diar):
            speaker = mapping.get(seg.get("speaker", ""), seg.get("speaker"))
            text = trans.get(f"segment_{i:04d}.wav", "")
            lines.append(f"[{speaker}] {text}")
        output_txt.write_text("\n".join(lines))
        logger.info("Final transcript saved to %s", output_txt)
        return output_txt
