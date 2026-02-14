"""Binaural beat and isochronic tone generation."""

import numpy as np


class BinauralGenerator:
    """Generate binaural beats and isochronic tones for meditation.

    Brainwave Frequency Ranges:
    - Delta (0.5-4 Hz): Deep sleep, healing
    - Theta (4-8 Hz): Meditation, creativity, REM sleep
    - Alpha (8-14 Hz): Relaxation, calm focus
    - Beta (14-30 Hz): Active concentration, alertness
    """

    # Preset configurations for common meditation states
    PRESETS = {
        "deep_sleep": {
            "base_freq": 150,
            "beat_freq": 2.0,
            "description": "Delta waves for deep sleep",
        },
        "meditation": {
            "base_freq": 200,
            "beat_freq": 6.0,
            "description": "Theta waves for deep meditation",
        },
        "relaxation": {
            "base_freq": 200,
            "beat_freq": 10.0,
            "description": "Alpha waves for relaxation",
        },
        "focus": {
            "base_freq": 250,
            "beat_freq": 18.0,
            "description": "Beta waves for concentration",
        },
        "creativity": {
            "base_freq": 180,
            "beat_freq": 7.5,
            "description": "Theta-Alpha border for creativity",
        },
    }

    def __init__(self, sample_rate: int = 44100):
        """Initialize generator with sample rate.

        Args:
            sample_rate: Audio sample rate in Hz (default 44100)
        """
        self.sample_rate = sample_rate

    def generate_binaural_beat(
        self,
        base_freq: float,
        beat_freq: float,
        duration: float,
        fade_duration: float = 2.0,
    ) -> np.ndarray:
        """Generate binaural beats as stereo audio.

        Binaural beats work by playing slightly different frequencies in each ear.
        The brain perceives a third frequency equal to the difference.

        Args:
            base_freq: Base carrier frequency in Hz (100-400 recommended)
            beat_freq: Desired binaural beat frequency in Hz (0.5-30)
            duration: Duration in seconds
            fade_duration: Fade in/out duration in seconds

        Returns:
            Stereo numpy array of shape (samples, 2)
        """
        samples = int(duration * self.sample_rate)
        t = np.linspace(0, duration, samples)

        # Left ear: base frequency
        # Right ear: base frequency + beat frequency
        left = np.sin(2 * np.pi * base_freq * t)
        right = np.sin(2 * np.pi * (base_freq + beat_freq) * t)

        # Apply fade in/out
        audio = np.column_stack([left, right])
        audio = self._apply_fade(audio, fade_duration)

        return audio.astype(np.float32)

    def generate_isochronic_tones(
        self,
        freq: float,
        pulse_rate: float,
        duration: float,
        duty_cycle: float = 0.5,
        fade_duration: float = 2.0,
    ) -> np.ndarray:
        """Generate isochronic tones (rhythmic pulses).

        Unlike binaural beats, isochronic tones work through mono speakers.
        The brain entrains to the pulsing rhythm.

        Args:
            freq: Tone frequency in Hz
            pulse_rate: Pulses per second (same as brainwave target frequency)
            duration: Duration in seconds
            duty_cycle: Fraction of time the tone is on (0-1)
            fade_duration: Fade in/out duration in seconds

        Returns:
            Mono numpy array
        """
        samples = int(duration * self.sample_rate)
        t = np.linspace(0, duration, samples)

        # Generate carrier tone
        carrier = np.sin(2 * np.pi * freq * t)

        # Generate pulse envelope
        pulse_period = 1.0 / pulse_rate
        pulse_on_time = pulse_period * duty_cycle
        envelope = np.zeros(samples)

        for i, time in enumerate(t):
            phase = time % pulse_period
            if phase < pulse_on_time:
                # Smooth pulse shape using sine
                envelope[i] = np.sin(np.pi * phase / pulse_on_time)

        audio = carrier * envelope
        audio = self._apply_fade(audio.reshape(-1, 1), fade_duration).flatten()

        return audio.astype(np.float32)

    def generate_from_preset(
        self, preset: str, duration: float, fade_duration: float = 2.0
    ) -> np.ndarray:
        """Generate binaural beats from a preset configuration.

        Args:
            preset: One of "deep_sleep", "meditation", "relaxation", "focus", "creativity"
            duration: Duration in seconds
            fade_duration: Fade in/out duration in seconds

        Returns:
            Stereo numpy array
        """
        if preset not in self.PRESETS:
            available = ", ".join(self.PRESETS.keys())
            raise ValueError(f"Unknown preset '{preset}'. Available: {available}")

        config = self.PRESETS[preset]
        return self.generate_binaural_beat(
            base_freq=config["base_freq"],
            beat_freq=config["beat_freq"],
            duration=duration,
            fade_duration=fade_duration,
        )

    def generate_layered_binaural(
        self,
        layers: list[dict],
        duration: float,
        fade_duration: float = 2.0,
    ) -> np.ndarray:
        """Generate layered binaural beats with multiple frequencies.

        Args:
            layers: List of dicts with 'base_freq', 'beat_freq', and optional 'amplitude'
            duration: Duration in seconds
            fade_duration: Fade in/out duration in seconds

        Returns:
            Stereo numpy array
        """
        samples = int(duration * self.sample_rate)
        combined = np.zeros((samples, 2))

        for layer in layers:
            amplitude = layer.get("amplitude", 1.0 / len(layers))
            audio = self.generate_binaural_beat(
                base_freq=layer["base_freq"],
                beat_freq=layer["beat_freq"],
                duration=duration,
                fade_duration=0,  # Apply fade to combined signal
            )
            combined += audio * amplitude

        # Normalize to prevent clipping
        max_val = np.max(np.abs(combined))
        if max_val > 0:
            combined = combined / max_val * 0.9

        combined = self._apply_fade(combined, fade_duration)
        return combined.astype(np.float32)

    def _apply_fade(self, audio: np.ndarray, fade_duration: float) -> np.ndarray:
        """Apply fade in and fade out to audio.

        Args:
            audio: Audio array (1D or 2D)
            fade_duration: Fade duration in seconds

        Returns:
            Audio with fades applied
        """
        fade_samples = int(fade_duration * self.sample_rate)
        fade_samples = min(fade_samples, len(audio) // 4)  # Max 25% of duration

        if fade_samples > 0:
            fade_in = np.linspace(0, 1, fade_samples)
            fade_out = np.linspace(1, 0, fade_samples)

            if audio.ndim == 2:
                audio[:fade_samples] *= fade_in[:, np.newaxis]
                audio[-fade_samples:] *= fade_out[:, np.newaxis]
            else:
                audio[:fade_samples] *= fade_in
                audio[-fade_samples:] *= fade_out

        return audio

    @staticmethod
    def get_frequency_band(freq: float) -> str:
        """Get the brainwave band name for a frequency.

        Args:
            freq: Frequency in Hz

        Returns:
            Band name: "delta", "theta", "alpha", or "beta"
        """
        if freq < 4:
            return "delta"
        elif freq < 8:
            return "theta"
        elif freq < 14:
            return "alpha"
        else:
            return "beta"

    @staticmethod
    def list_presets() -> dict:
        """List available presets with descriptions.

        Returns:
            Dict of preset name to description
        """
        return {
            name: config["description"]
            for name, config in BinauralGenerator.PRESETS.items()
        }
