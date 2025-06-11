from __future__ import annotations

import csv
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
        output_path: Path,
    ) -> Path:
        diar = json.loads(diar_json.read_text())
        trans = {t["file"]: t["text"] for t in json.loads(trans_json.read_text())}
        results = []
        for i, seg in enumerate(diar):
            speaker = mapping.get(seg.get("speaker", ""), seg.get("speaker"))
            text = trans.get(f"segment_{i:04d}.wav", "")
            results.append({"speaker": speaker, "text": text})

        if output_path.suffix.lower() == ".json":
            output_path.write_text(json.dumps(results, ensure_ascii=False, indent=2))
        elif output_path.suffix.lower() == ".csv":
            with output_path.open("w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["speaker", "text"])
                for row in results:
                    writer.writerow([row["speaker"], row["text"]])
        else:
            lines = [f"[{r['speaker']}] {r['text']}" for r in results]
            output_path.write_text("\n".join(lines))

        logger.info("Final transcript saved to %s", output_path)
        return output_path
