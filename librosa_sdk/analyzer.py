"""Audio analysis for mindfulness qualities using librosa."""

from typing import Optional

import librosa
import numpy as np


class MindfulAnalyzer:
    """Analyze audio files for meditation and mindfulness qualities."""

    def __init__(self, audio_path: Optional[str] = None):
        """Initialize analyzer with optional audio file.

        Args:
            audio_path: Path to audio file to analyze
        """
        self.audio_path = audio_path
        self.y: Optional[np.ndarray] = None
        self.sr: Optional[int] = None

        if audio_path:
            self.load(audio_path)

    def load(self, audio_path: str) -> None:
        """Load an audio file for analysis.

        Args:
            audio_path: Path to audio file
        """
        self.audio_path = audio_path
        self.y, self.sr = librosa.load(audio_path)

    def load_from_array(self, y: np.ndarray, sr: int) -> None:
        """Load audio from numpy array.

        Args:
            y: Audio time series
            sr: Sample rate
        """
        self.y = y
        self.sr = sr

    def analyze_tempo(self) -> dict:
        """Detect BPM and categorize as calming, moderate, or energizing.

        Returns:
            dict with 'bpm', 'category', and 'description'
        """
        if self.y is None:
            raise ValueError("No audio loaded. Call load() first.")

        tempo, _ = librosa.beat.beat_track(y=self.y, sr=self.sr)
        bpm = float(tempo) if np.isscalar(tempo) else float(tempo[0])

        if bpm < 70:
            category = "calming"
            description = "Slow tempo ideal for deep relaxation and sleep meditation"
        elif bpm < 120:
            category = "moderate"
            description = (
                "Balanced tempo suitable for mindful movement or light meditation"
            )
        else:
            category = "energizing"
            description = (
                "Upbeat tempo better suited for active meditation or focus sessions"
            )

        return {
            "bpm": round(bpm, 1),
            "category": category,
            "description": description,
        }

    def analyze_spectral_warmth(self) -> dict:
        """Measure brightness/warmth for mood assessment.

        Returns:
            dict with 'centroid_hz', 'warmth_score', and 'character'
        """
        if self.y is None:
            raise ValueError("No audio loaded. Call load() first.")

        # Spectral centroid indicates brightness
        centroid = librosa.feature.spectral_centroid(y=self.y, sr=self.sr)
        mean_centroid = float(np.mean(centroid))

        # Normalize to 0-1 scale (higher = brighter/colder, lower = warmer)
        # Typical speech/music centroid range: 500-4000 Hz
        warmth_score = max(0, min(1, 1 - (mean_centroid - 500) / 3500))

        if warmth_score > 0.7:
            character = "warm"
            description = "Rich, warm tones that promote relaxation and comfort"
        elif warmth_score > 0.4:
            character = "balanced"
            description = (
                "Balanced frequency spectrum suitable for various meditation styles"
            )
        else:
            character = "bright"
            description = "Bright, airy tones that may promote alertness and clarity"

        return {
            "centroid_hz": round(mean_centroid, 1),
            "warmth_score": round(warmth_score, 2),
            "character": character,
            "description": description,
        }

    def extract_meditation_features(self) -> dict:
        """Extract comprehensive features for meditation suitability.

        Returns:
            dict with tempo, warmth, dynamics, and overall assessment
        """
        if self.y is None:
            raise ValueError("No audio loaded. Call load() first.")

        # Tempo analysis
        tempo_info = self.analyze_tempo()

        # Spectral warmth
        warmth_info = self.analyze_spectral_warmth()

        # MFCCs for timbral texture
        mfccs = librosa.feature.mfcc(y=self.y, sr=self.sr, n_mfcc=13)
        mfcc_variance = float(np.mean(np.var(mfccs, axis=1)))

        # Zero-crossing rate (higher = more percussive/noisy)
        zcr = librosa.feature.zero_crossing_rate(self.y)
        mean_zcr = float(np.mean(zcr))

        # RMS energy for dynamics
        rms = librosa.feature.rms(y=self.y)
        rms_std = float(np.std(rms))
        dynamics = "stable" if rms_std < 0.05 else "dynamic"

        # Overall meditation suitability score
        score = 0.0
        if tempo_info["category"] == "calming":
            score += 0.4
        elif tempo_info["category"] == "moderate":
            score += 0.2
        if warmth_info["warmth_score"] > 0.5:
            score += 0.3
        if dynamics == "stable":
            score += 0.2
        if mean_zcr < 0.1:
            score += 0.1

        if score >= 0.7:
            suitability = "excellent"
        elif score >= 0.5:
            suitability = "good"
        elif score >= 0.3:
            suitability = "moderate"
        else:
            suitability = "low"

        return {
            "tempo_bpm": tempo_info["bpm"],
            "tempo_category": tempo_info["category"],
            "warmth_score": warmth_info["warmth_score"],
            "warmth_character": warmth_info["character"],
            "dynamics": dynamics,
            "timbral_complexity": round(mfcc_variance, 4),
            "percussiveness": round(mean_zcr, 4),
            "meditation_score": round(score, 2),
            "suitability": suitability,
        }

    def detect_silence_gaps(
        self, min_silence_ms: int = 500, silence_thresh_db: float = -40
    ) -> list[dict]:
        """Find natural pause points for guided meditation.

        Args:
            min_silence_ms: Minimum silence duration in milliseconds
            silence_thresh_db: Threshold below which audio is considered silence

        Returns:
            List of dicts with 'start_sec', 'end_sec', 'duration_sec'
        """
        if self.y is None:
            raise ValueError("No audio loaded. Call load() first.")

        # Convert to dB
        rms = librosa.feature.rms(y=self.y)[0]
        db = librosa.amplitude_to_db(rms, ref=np.max)

        # Find frames below threshold
        hop_length = 512
        frame_duration = hop_length / self.sr
        min_frames = int(min_silence_ms / 1000 / frame_duration)

        silent_frames = db < silence_thresh_db
        gaps = []
        start_frame = None

        for i, is_silent in enumerate(silent_frames):
            if is_silent and start_frame is None:
                start_frame = i
            elif not is_silent and start_frame is not None:
                if i - start_frame >= min_frames:
                    gaps.append(
                        {
                            "start_sec": round(start_frame * frame_duration, 2),
                            "end_sec": round(i * frame_duration, 2),
                            "duration_sec": round(
                                (i - start_frame) * frame_duration, 2
                            ),
                        }
                    )
                start_frame = None

        # Handle trailing silence
        if start_frame is not None and len(silent_frames) - start_frame >= min_frames:
            gaps.append(
                {
                    "start_sec": round(start_frame * frame_duration, 2),
                    "end_sec": round(len(silent_frames) * frame_duration, 2),
                    "duration_sec": round(
                        (len(silent_frames) - start_frame) * frame_duration, 2
                    ),
                }
            )

        return gaps

    def separate_harmonic_percussive(self) -> tuple[np.ndarray, np.ndarray]:
        """Isolate ambient textures from rhythmic elements.

        Returns:
            Tuple of (harmonic_audio, percussive_audio) numpy arrays
        """
        if self.y is None:
            raise ValueError("No audio loaded. Call load() first.")

        harmonic, percussive = librosa.effects.hpss(self.y)
        return harmonic, percussive

    def get_duration(self) -> float:
        """Get duration of loaded audio in seconds."""
        if self.y is None:
            raise ValueError("No audio loaded. Call load() first.")
        return librosa.get_duration(y=self.y, sr=self.sr)
