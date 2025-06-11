#!/usr/bin/env python
from pathlib import Path
import argparse
import os
import logging

from src.core.diarize import Diarizer

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser(description="Run speaker diarization")
parser.add_argument("-i", "--input", required=True, help="Input audio file")
parser.add_argument("-o", "--output", required=True, help="Output JSON")
parser.add_argument("-t", "--token", required=False, help="HuggingFace token")
parser.add_argument("--model", default="pyannote/speaker-diarization@2023.07", help="Model name")
parser.add_argument("--use-gpu", action="store_true", help="Request GPU inference")

args = parser.parse_args()

token = args.token or os.environ.get("HF_TOKEN", "")
diarizer = Diarizer(token, model=args.model, use_gpu=args.use_gpu)
diarizer.run(Path(args.input), Path(args.output))
