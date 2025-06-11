# Gijirock

議事録ツールです。音声ファイルから話者分離、文字起こしを行い、GUI 上でスピーカー名を編集して最終的な議事録 (TXT) を生成します。

## セットアップ

このプロジェクトは **Python 3.10** での利用が必須です。`pyannote.audio` 2.x は `torchaudio<1.0` に依存しているため、Python 3.11 以降ではインストールに失敗します。`pyenv` などを使って 3.10 系の Python を準備してください。

```bash
# 例: pyenv を利用した環境構築
pyenv install 3.10.12      # 未インストールの場合
pyenv local 3.10.12
python -m venv venv
# Windows の場合 ``venv\Scripts\activate``
source venv/bin/activate
pip install -r requirements.txt

### macOS (Apple Silicon) での hmmlearn インストール

Apple Silicon 環境では `hmmlearn` 0.2 系のビルドが失敗することがあります。
その場合は下記のように Universal2 wheel が公開されている
`hmmlearn==0.3.0` を先にインストールし、その後で残りの依存関係を
`--no-deps` オプション付きで入れてください。

```bash
pip install --no-deps hmmlearn==0.3.0
pip install -r requirements.txt --no-deps
```

`pyannote.audio` 2.1.1 は `hmmlearn<0.3` を要求しますが、通常は 0.3.0 でも問題なく
動作します。

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
