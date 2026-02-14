"""Audio recording utilities for journaling and soundscape capture."""

import numpy as np
import sounddevice as sd
import soundfile as sf


class AudioRecorder:
    """Record audio from microphone for voice journaling and soundscape creation."""

    def __init__(self, sample_rate: int = 44100, channels: int = 1):
        """Initialize recorder.

        Args:
            sample_rate: Sample rate in Hz (default 44100)
            channels: Number of channels (1=mono, 2=stereo)
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self._recording = False
        self._audio_buffer: list[np.ndarray] = []

    def record_audio(self, duration: float) -> np.ndarray:
        """Record audio for a fixed duration.

        Args:
            duration: Recording duration in seconds

        Returns:
            Recorded audio as numpy array
        """
        samples = int(duration * self.sample_rate)
        print(f"Recording for {duration} seconds...")
        audio = sd.rec(
            samples,
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype=np.float32,
        )
        sd.wait()
        print("Recording complete.")
        return audio.flatten() if self.channels == 1 else audio

    def record_until_silence(
        self,
        silence_threshold: float = 0.01,
        silence_duration: float = 2.0,
        timeout: float = 300.0,
        min_duration: float = 1.0,
    ) -> np.ndarray:
        """Record until silence is detected.

        Useful for voice journaling where you want to automatically stop
        when the speaker finishes.

        Args:
            silence_threshold: RMS level below which is considered silence
            silence_duration: How long silence must persist to stop (seconds)
            timeout: Maximum recording duration (seconds)
            min_duration: Minimum recording duration before checking for silence

        Returns:
            Recorded audio as numpy array
        """
        block_size = int(0.1 * self.sample_rate)  # 100ms blocks
        silence_blocks_needed = int(silence_duration / 0.1)
        max_blocks = int(timeout / 0.1)

        self._audio_buffer = []
        silence_count = 0
        total_blocks = 0
        min_blocks = int(min_duration / 0.1)

        print("Recording... (will stop after silence)")

        def callback(indata, frames, time, status):
            nonlocal silence_count, total_blocks
            self._audio_buffer.append(indata.copy())
            total_blocks += 1

            rms = np.sqrt(np.mean(indata**2))
            if rms < silence_threshold and total_blocks >= min_blocks:
                silence_count += 1
            else:
                silence_count = 0

        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype=np.float32,
            blocksize=block_size,
            callback=callback,
        ):
            while silence_count < silence_blocks_needed and total_blocks < max_blocks:
                sd.sleep(100)

        print("Recording complete.")
        audio = np.concatenate(self._audio_buffer)
        return audio.flatten() if self.channels == 1 else audio

    def start_recording(self) -> None:
        """Start continuous recording (non-blocking).

        Call stop_recording() to finish and get the audio.
        """
        if self._recording:
            raise RuntimeError("Already recording")

        self._audio_buffer = []
        self._recording = True

        def callback(indata, frames, time, status):
            if self._recording:
                self._audio_buffer.append(indata.copy())

        self._stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype=np.float32,
            callback=callback,
        )
        self._stream.start()
        print("Recording started...")

    def stop_recording(self) -> np.ndarray:
        """Stop recording and return captured audio.

        Returns:
            Recorded audio as numpy array
        """
        if not self._recording:
            raise RuntimeError("Not recording")

        self._recording = False
        self._stream.stop()
        self._stream.close()
        print("Recording stopped.")

        if not self._audio_buffer:
            return np.array([], dtype=np.float32)

        audio = np.concatenate(self._audio_buffer)
        return audio.flatten() if self.channels == 1 else audio

    def save_recording(
        self,
        audio: np.ndarray,
        path: str,
        format: str | None = None,
    ) -> None:
        """Save recorded audio to file.

        Args:
            audio: Audio data as numpy array
            path: Output file path
            format: Audio format ('WAV', 'FLAC', 'OGG'). Auto-detected from extension if None.
        """
        sf.write(path, audio, self.sample_rate, format=format)
        print(f"Saved recording to {path}")

    def get_audio_devices(self) -> dict:
        """List available audio input devices.

        Returns:
            Dict with device information
        """
        devices = sd.query_devices()
        input_devices = []

        for i, device in enumerate(devices):
            if device["max_input_channels"] > 0:
                input_devices.append(
                    {
                        "index": i,
                        "name": device["name"],
                        "channels": device["max_input_channels"],
                        "sample_rate": device["default_samplerate"],
                        "is_default": i == sd.default.device[0],
                    }
                )

        return {
            "devices": input_devices,
            "default": sd.default.device[0],
        }

    def set_input_device(self, device_index: int) -> None:
        """Set the input device to use for recording.

        Args:
            device_index: Device index from get_audio_devices()
        """
        sd.default.device[0] = device_index

    def get_input_level(self, duration: float = 0.5) -> float:
        """Get current microphone input level.

        Useful for testing microphone setup.

        Args:
            duration: Duration to sample in seconds

        Returns:
            RMS level (0.0 = silence, 1.0 = max)
        """
        samples = int(duration * self.sample_rate)
        audio = sd.rec(
            samples,
            samplerate=self.sample_rate,
            channels=1,
            dtype=np.float32,
        )
        sd.wait()
        rms = float(np.sqrt(np.mean(audio**2)))
        return min(1.0, rms * 10)  # Scale for visibility
