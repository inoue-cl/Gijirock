# Gijirock

議事録ツールです。音声ファイルから話者分離、文字起こしを行い、GUI 上でスピーカー名を編集して最終的な議事録 (TXT) を生成します。

## セットアップ

```bash
# Python 3 を python3 として呼び出す環境では以下を使用
python3 -m venv venv
# Windows など ``python`` コマンドが Python 3 を指す場合は ``python`` でも構いません
venv\Scripts\activate   # PowerShell/CMD の場合
# (macOS/Linux の場合は source venv/bin/activate)
pip install -r requirements.txt
# diarization model requires pyannote.audio 2.x
```

`sentencepiece` のビルドに失敗する場合は `pip install --upgrade pip` を実行し、
続けて以下を個別にインストールしてください。

```bash
pip install --prefer-binary sentencepiece==0.2.0
```

音声処理には `ffmpeg` が必要です。Windows では
[FFmpeg](https://ffmpeg.org/download.html) の実行ファイルを入手して
`ffmpeg.exe` へのパスを環境変数に通してください。
`m4a` や `mp3` を読み込んだ場合は内部で WAV へ変換して処理するため、
`ffmpeg` が正しくインストールされている必要があります。
Hugging Face API トークンは環境変数 `HF_TOKEN` または CLI 引数で指定します。

## GUI 起動

```bash
python -m src.ui.main_window
```
*このモジュール形式で実行することで、パッケージのインポートパスが自動的に設定
されます。*

## 実行ファイル

Windows では `build_scripts/build_win_exe.sh` を実行して単一の EXE を生成できます。

## CMD からの実行例

初心者向けに、コマンドプロンプトでの一連の流れをまとめます。

1. リポジトリを取得して上記のセットアップを実施します。
2. `set HF_TOKEN=YOUR_TOKEN` でトークンを設定します（必要に応じて）。
3. 音声ファイルを `audio/` フォルダーに置き、以下のコマンドを順に実行します。

```cmd
python 1_diarize.py -i audio\sample.wav -o output\diarization.json
python 2_split_segments.py -i audio\sample.wav -d output\diarization.json -o segments
python 3_transcribe.py -i segments -o output\transcriptions.json
python 4_merge_results.py -d output\diarization.json -t output\transcriptions.json -o output\final.txt
```

最後に `output\final.txt` に話者ラベル付きの文字起こし結果が生成されます。

## サンプル音声

`speech_diarizer_qt/audio/sample.wav` は含まれていません。30 秒の二人話者の音声を各自用意してください。

## ライセンス

MIT