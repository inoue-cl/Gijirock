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

args = parser.parse_args()

token = args.token or os.environ.get("HF_TOKEN", "")
diarizer = Diarizer(token)
diarizer.run(Path(args.input), Path(args.output))