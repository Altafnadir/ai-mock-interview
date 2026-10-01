import os
import shutil
import subprocess
import logging
from pathlib import Path
from typing import Optional, Tuple

logger = logging.getLogger(__name__)

class MediaNormalizer:
    """Normalizes candidate audio and video recordings to standardized formats for analysis.
    
    Audio is normalized to 16 kHz mono 16-bit PCM WAV (optimal for Whisper & Librosa).
    Video is normalized to standard H.264 / AAC MP4 with faststart flags.
    """

    def __init__(self):
        self._ffmpeg_bin = shutil.which("ffmpeg")

    @property
    def is_ffmpeg_available(self) -> bool:
        return self._ffmpeg_bin is not None

    def normalize_audio(self, input_path: str, output_path: Optional[str] = None) -> str:
        """Extracts and normalizes audio track to 16 kHz mono WAV."""
        if not input_path or not os.path.exists(input_path):
            return input_path

        if not self.is_ffmpeg_available:
            logger.warning("ffmpeg not detected on system; skipping audio normalization.")
            return input_path

        if not output_path:
            p = Path(input_path)
            output_path = str(p.parent / f"{p.stem}_normalized_16k.wav")

        try:
            cmd = [
                self._ffmpeg_bin,
                "-y",
                "-i", input_path,
                "-vn",
                "-acodec", "pcm_s16le",
                "-ar", "16000",
                "-ac", "1",
                output_path
            ]
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
            if res.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                logger.info(f"Normalized audio saved to: {output_path}")
                return output_path
            else:
                logger.warning(f"ffmpeg audio normalization returned code {res.returncode}: {res.stderr.decode('utf-8', errors='ignore')[:200]}")
        except Exception as e:
            logger.warning(f"Audio normalization exception: {e}")

        return input_path

    def normalize_video(self, input_path: str, output_path: Optional[str] = None) -> str:
        """Normalizes video to H.264 baseline/main profile MP4 for consistent OpenCV/DeepFace playback."""
        if not input_path or not os.path.exists(input_path):
            return input_path

        if not self.is_ffmpeg_available:
            logger.warning("ffmpeg not detected on system; skipping video normalization.")
            return input_path

        if not output_path:
            p = Path(input_path)
            output_path = str(p.parent / f"{p.stem}_normalized.mp4")

        try:
            cmd = [
                self._ffmpeg_bin,
                "-y",
                "-i", input_path,
                "-c:v", "libx264",
                "-preset", "fast",
                "-crf", "23",
                "-pix_fmt", "yuv420p",
                "-c:a", "aac",
                "-b:a", "128k",
                "-movflags", "+faststart",
                output_path
            ]
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
            if res.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                logger.info(f"Normalized video saved to: {output_path}")
                return output_path
            else:
                logger.warning(f"ffmpeg video normalization returned code {res.returncode}: {res.stderr.decode('utf-8', errors='ignore')[:200]}")
        except Exception as e:
            logger.warning(f"Video normalization exception: {e}")

        return input_path

    def normalize_media_pair(
        self,
        audio_path: Optional[str],
        video_path: Optional[str]
    ) -> Tuple[Optional[str], Optional[str]]:
        """Convenience method to normalize both audio and video streams before pipeline execution."""
        norm_audio = self.normalize_audio(audio_path) if audio_path else None
        norm_video = self.normalize_video(video_path) if video_path else None
        return norm_audio, norm_video

media_normalizer = MediaNormalizer()
