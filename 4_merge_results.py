#!/usr/bin/env python
from pathlib import Path
import argparse
import logging
import json

from src.core.merger import Merger

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser(description="Merge diarization and transcripts")
parser.add_argument("-d", "--diar", required=True, help="Diarization JSON")
parser.add_argument("-t", "--trans", required=True, help="Transcription JSON")
parser.add_argument("-m", "--map", required=False, help="Mapping YAML (unused)")
parser.add_argument("-o", "--output", required=True, help="Output TXT")

args = parser.parse_args()

mapping = {}
Merger().run(Path(args.diar), Path(args.trans), mapping, Path(args.output))
