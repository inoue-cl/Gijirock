#!/bin/bash
pyinstaller -F -w -n speech_diarizer \
  --add-data "src/ui/resources:resources" \
  --add-data "models:models" \
  src/ui/main_window.py
