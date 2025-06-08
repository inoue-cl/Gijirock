# Gijirock

議事録ツールです。音声ファイルから話者分離、文字起こしを行い、GUI 上でスピーカー名を編集して最終的な議事録 (TXT) を生成します。

## セットアップ

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

別途 `ffmpeg` をインストールしてください。
Hugging Face API トークンは環境変数 `HF_TOKEN` または CLI 引数で指定します。

## GUI 起動

```bash
python src/ui/main_window.py
```

## 実行ファイル

Windows では `build_scripts/build_win_exe.sh` を実行して単一の EXE を生成できます。

## サンプル音声

`speech_diarizer_qt/audio/sample.wav` は含まれていません。30 秒の二人話者の音声を各自用意してください。

## ライセンス

MIT
