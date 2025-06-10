#!/usr/bin/env python
from pathlib import Path
import argparse
import logging

from src.core.splitter import SegmentSplitter

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser(description="Split audio into segments")
parser.add_argument("-i", "--input", required=True, help="Input audio file")
parser.add_argument("-d", "--diar", required=True, help="Diarization JSON")
parser.add_argument("-o", "--output", required=True, help="Output directory")

args = parser.parse_args()

splitter = SegmentSplitter()
splitter.run(Path(args.input), Path(args.diar), Path(args.output))
