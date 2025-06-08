#!/usr/bin/env python
from pathlib import Path
import argparse
import logging

from src.core.transcriber import Transcriber

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser(description="Transcribe segments")
parser.add_argument("-i", "--input", required=True, help="Segments directory")
parser.add_argument("-o", "--output", required=True, help="Output JSON")

args = parser.parse_args()

Transcriber().run(Path(args.input), Path(args.output))
