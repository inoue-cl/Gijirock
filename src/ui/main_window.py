from __future__ import annotations

import json
import os
import logging
import sys
from pathlib import Path
from typing import Dict

try:  # pragma: no cover - import check
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import (
        QApplication,
        QHBoxLayout,
        QHeaderView,
        QLabel,
        QLineEdit,
        QMainWindow,
        QMessageBox,
        QPushButton,
        QTableWidget,
        QTableWidgetItem,
        QVBoxLayout,
        QWidget,
        QFileDialog,
    )
    from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
except ModuleNotFoundError as exc:  # pragma: no cover - CLI/GUI
    raise ModuleNotFoundError(
        "PySide6 がインストールされていません。"
        " `pip install -r requirements.txt` を実行して依存パッケージを"
        " インストールしてください。"
    ) from exc

# ``main_window.py`` is expected to be executed as a module from the
# repository root (`python -m src.ui.main_window`).  When run this way
# Python sets up the package import path automatically so no manual
# modification of ``sys.path`` is required.

# Support execution both as ``python -m src.ui.main_window`` and as a script.
if __package__ in (None, ""):  # pragma: no cover - CLI/GUI
    # When run directly (e.g. ``python src/ui/main_window.py``), ``src``
    # won't be on ``sys.path``.  Add the repository root so that the
    # ``src`` package can be imported.
    repo_root = Path(__file__).resolve().parents[2]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))

from src.core.diarize import Diarizer
from src.core.splitter import SegmentSplitter
from src.core.transcriber import Transcriber
from src.core.merger import Merger

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Speech Diarizer")
        self.resize(800, 600)
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)

        open_btn = QPushButton("Open Audio")
        open_btn.clicked.connect(self.open_audio)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Speaker", "Text"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        export_btn = QPushButton("Export TXT")
        export_btn.clicked.connect(self.export_txt)

        layout = QVBoxLayout()
        layout.addWidget(open_btn)
        layout.addWidget(self.table)
        layout.addWidget(export_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.mapping: Dict[str, str] = {}
        self.diar_json: Path | None = None
        self.trans_json: Path | None = None

    def open_audio(self) -> None:
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilters(["Audio Files (*.wav *.mp3 *.m4a)"])
        if file_dialog.exec() == QFileDialog.Accepted:
            audio_path = Path(file_dialog.selectedFiles()[0])
            try:
                self.process(audio_path)
            except Exception as exc:  # pragma: no cover - GUI
                QMessageBox.critical(self, "Error", str(exc))
                logger.exception("Processing failed")

    def process(self, audio_path: Path) -> None:
        output = Path("output")
        output.mkdir(exist_ok=True)
        diarizer = Diarizer(token=os.environ.get("HF_TOKEN", ""))
        self.diar_json = output / "diarization.json"
        diarizer.run(audio_path, self.diar_json)

        splitter = SegmentSplitter()
        segments_dir = Path("segments")
        splitter.run(audio_path, self.diar_json, segments_dir)

        transcriber = Transcriber()
        self.trans_json = output / "transcriptions.json"
        transcriber.run(segments_dir, self.trans_json)

        self.load_results()

    def load_results(self) -> None:
        if not (self.diar_json and self.trans_json):
            return
        diar = json.loads(Path(self.diar_json).read_text())
        trans = {t["file"]: t["text"] for t in json.loads(Path(self.trans_json).read_text())}
        self.table.setRowCount(len(diar))
        for i, seg in enumerate(diar):
            speaker_item = QTableWidgetItem(seg.get("speaker", ""))
            text_item = QTableWidgetItem(trans.get(f"segment_{i:04d}.wav", ""))
            self.table.setItem(i, 0, speaker_item)
            self.table.setItem(i, 1, text_item)

    def export_txt(self) -> None:
        if not (self.diar_json and self.trans_json):
            QMessageBox.warning(self, "Warning", "No data to export")
            return
        mapping = self.mapping
        output_txt = Path("output/final.txt")
        Merger().run(self.diar_json, self.trans_json, mapping, output_txt)
        QMessageBox.information(self, "Exported", f"Saved to {output_txt}")


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()