"""Audio playback and export utilities."""

import numpy as np
import sounddevice as sd
import soundfile as sf


def play_audio(
    audio: np.ndarray,
    sample_rate: int = 44100,
    blocking: bool = True,
) -> None:
    """Play audio through the default output device.

    Args:
        audio: Audio data as numpy array (mono or stereo)
        sample_rate: Sample rate in Hz
        blocking: If True, wait for playback to complete
    """
    sd.play(audio, sample_rate)
    if blocking:
        sd.wait()


def stop_playback() -> None:
    """Stop any currently playing audio."""
    sd.stop()


def save_audio(
    audio: np.ndarray,
    path: str,
    sample_rate: int = 44100,
) -> None:
    """Save audio to a file.

    Args:
        audio: Audio data as numpy array
        path: Output file path (supports .wav, .flac, .ogg)
        sample_rate: Sample rate in Hz
    """
    sf.write(path, audio, sample_rate)


def get_audio_devices() -> dict:
    """Get available audio input and output devices.

    Returns:
        Dict with 'input' and 'output' device lists
    """
    devices = sd.query_devices()
    input_devices = []
    output_devices = []

    for i, device in enumerate(devices):
        info = {
            "index": i,
            "name": device["name"],
            "sample_rate": device["default_samplerate"],
        }
        if device["max_input_channels"] > 0:
            info["channels"] = device["max_input_channels"]
            input_devices.append(info)
        if device["max_output_channels"] > 0:
            info["channels"] = device["max_output_channels"]
            output_devices.append(info)

    return {"input": input_devices, "output": output_devices}
