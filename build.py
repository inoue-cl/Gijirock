import sys
import subprocess
import shutil
from pathlib import Path


def build_windows() -> None:
    cmd = [
        "pyinstaller",
        "-F",
        "-w",
        "-n",
        "speech_diarizer",
        "src/ui/main_window.py",
    ]
    subprocess.run(cmd, check=True)


def build_others() -> None:
    dist = Path("dist")
    dist.mkdir(exist_ok=True)
    files = [
        "1_diarize.py",
        "2_split_segments.py",
        "3_transcribe.py",
        "4_merge_results.py",
        "src",
        "requirements.txt",
        "README.md",
        "LICENSE",
    ]
    for f in files:
        src = Path(f)
        dst = dist / src.name
        if src.is_dir():
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)
    print(f"Distribution files saved to {dist}")


def main() -> None:
    if sys.platform.startswith("win32"):
        build_windows()
    else:
        build_others()


if __name__ == "__main__":
    main()
