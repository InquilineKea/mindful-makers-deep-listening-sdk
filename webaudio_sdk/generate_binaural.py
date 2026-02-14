"""Command-line tool to generate binaural beat audio files."""

import argparse
import sys
import numpy as np
from webaudio_sdk import BinauralGenerator
import soundfile as sf


def save_audio(audio: np.ndarray, path: str, sample_rate: int = 44100) -> None:
    """Save audio to a file without requiring sounddevice."""
    sf.write(path, audio, sample_rate)


def main():
    parser = argparse.ArgumentParser(
        description="Generate binaural beat audio files for meditation"
    )
    parser.add_argument(
        "--base-freq",
        type=float,
        default=200,
        help="Base frequency in Hz (default: 200)",
    )
    parser.add_argument(
        "--beat-freq",
        type=float,
        default=6,
        help="Beat frequency in Hz (default: 6 - Theta waves)",
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=10,
        help="Duration in seconds (default: 10)",
    )
    parser.add_argument(
        "--fade-duration",
        type=float,
        default=2,
        help="Fade in/out duration in seconds (default: 2)",
    )
    parser.add_argument(
        "--sample-rate",
        type=int,
        default=44100,
        help="Sample rate in Hz (default: 44100)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="binaural_beat.wav",
        help="Output file path (default: binaural_beat.wav)",
    )
    parser.add_argument(
        "--tone-type",
        type=str,
        choices=["binaural", "isochronic"],
        default="binaural",
        help="Type of tone to generate (default: binaural)",
    )

    args = parser.parse_args()

    # Validate arguments
    if args.base_freq <= 0:
        print("Error: base-freq must be positive", file=sys.stderr)
        sys.exit(1)
    if args.beat_freq <= 0:
        print("Error: beat-freq must be positive", file=sys.stderr)
        sys.exit(1)
    if args.duration <= 0:
        print("Error: duration must be positive", file=sys.stderr)
        sys.exit(1)

    print("=" * 60)
    print("Binaural Beat Generator")
    print("=" * 60)
    print(f"Base frequency: {args.base_freq} Hz")
    print(f"Beat frequency: {args.beat_freq} Hz")
    print(f"Duration: {args.duration} seconds")
    print(f"Fade duration: {args.fade_duration} seconds")
    print(f"Sample rate: {args.sample_rate} Hz")
    print(f"Tone type: {args.tone_type}")
    print()

    # Generate audio
    print(f"Generating {args.tone_type} tones...")
    generator = BinauralGenerator(sample_rate=args.sample_rate)

    if args.tone_type == "binaural":
        audio = generator.generate_binaural_beat(
            base_freq=args.base_freq,
            beat_freq=args.beat_freq,
            duration=args.duration,
            fade_duration=args.fade_duration,
        )
    else:  # isochronic
        audio = generator.generate_isochronic_tone(
            freq=args.base_freq,
            beat_freq=args.beat_freq,
            duration=args.duration,
            fade_duration=args.fade_duration,
        )

    print(f"Generated audio shape: {audio.shape}")

    # Save to file
    print(f"Saving to {args.output}...")
    save_audio(audio, args.output, sample_rate=args.sample_rate)
    print(f"✓ Successfully saved to {args.output}")
    print("=" * 60)


if __name__ == "__main__":
    main()
