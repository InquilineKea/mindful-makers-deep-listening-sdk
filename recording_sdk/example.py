"""Example: Record a voice journal entry."""

from recording_sdk import AudioRecorder


def main():
    print("=" * 60)
    print("Recording SDK - Voice Journaling Demo")
    print("=" * 60)
    print()

    recorder = AudioRecorder(sample_rate=44100, channels=1)

    # List available devices
    print("Available Input Devices:")
    print("-" * 40)
    devices = recorder.get_audio_devices()
    for device in devices["devices"]:
        default = " (default)" if device["is_default"] else ""
        print(f"  [{device['index']}] {device['name']}{default}")
    print()

    # Test input level
    print("Testing microphone level...")
    print("-" * 40)
    print("  Speak into your microphone...")
    level = recorder.get_input_level(duration=2.0)
    bars = int(level * 20)
    print(f"  Level: [{'=' * bars}{' ' * (20 - bars)}] {level:.2f}")
    print()

    # Record a short sample
    print("Recording a 5-second voice journal entry...")
    print("-" * 40)
    print("  Speak your reflection or intention for today.")
    print()
    audio = recorder.record_audio(duration=5)
    print(f"  Recorded {len(audio) / 44100:.1f} seconds")
    print(f"  Audio shape: {audio.shape}")
    print()

    # Save the recording
    output_path = "journal_entry.wav"
    print(f"Saving to {output_path}...")
    recorder.save_recording(audio, output_path)
    print()

    # Demonstrate auto-stop recording
    print("Demo: Record until silence (auto-stop)...")
    print("-" * 40)
    print("  This will record until 2 seconds of silence.")
    print("  Press Ctrl+C to skip this demo.")
    print()

    try:
        audio = recorder.record_until_silence(
            silence_threshold=0.01,
            silence_duration=2.0,
            timeout=30.0,
            min_duration=2.0,
        )
        print(f"  Recorded {len(audio) / 44100:.1f} seconds")

        if len(audio) > 0:
            recorder.save_recording(audio, "journal_auto.wav")
    except KeyboardInterrupt:
        print("  Skipped.")
    print()

    print("=" * 60)
    print("Demo complete!")
    print()
    print("Voice Journaling Tips:")
    print("  - Find a quiet space for clarity")
    print("  - Speak your intentions, reflections, or gratitude")
    print("  - Review recordings during meditation")
    print("  - Use recordings to track your mindfulness journey")
    print("=" * 60)


if __name__ == "__main__":
    main()
