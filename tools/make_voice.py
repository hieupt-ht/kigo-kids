"""Generate English narration clips with Kokoro (Apache-2.0), offline.

Usage: python tools/make_voice.py [voice] [speed]
Models live in models/ (not committed): kokoro-v1.0.onnx, voices-v1.0.bin
"""
import sys
from pathlib import Path

import soundfile as sf
from kokoro_onnx import Kokoro

CLIPS = {
    "intro": "Hello! I'm Kigo. Let's learn English with a story!",
    "king_s": "A long time ago, King Hung had a kind and beautiful daughter.",
    "king": "king", "princess": "princess", "daughter": "daughter",
    "suitor_s": "Son Tinh lives on a mountain. He can make hills!",
    "mountain": "mountain", "hill": "hill",
}

voice = sys.argv[1] if len(sys.argv) > 1 else "af_heart"
speed = float(sys.argv[2]) if len(sys.argv) > 2 else 0.9
out = Path(sys.argv[3]) if len(sys.argv) > 3 else Path("kigo-video/public/voice")
out.mkdir(parents=True, exist_ok=True)
k = Kokoro("models/kokoro-v1.0.onnx", "models/voices-v1.0.bin")
for name, text in CLIPS.items():
    samples, sr = k.create(text, voice=voice, speed=speed, lang="en-us")
    sf.write(out / f"{name}.wav", samples, sr)
    print(f"{name}: {len(samples) / sr:.1f}s")
