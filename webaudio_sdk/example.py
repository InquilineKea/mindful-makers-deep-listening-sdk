"""Example: Generate and play binaural beats for meditation."""

from webaudio_sdk import BinauralGenerator, play_audio, save_audio


def main():
    print("=" * 60)
    print("WebAudio SDK - Binaural Beat Generation Demo")
    print("=" * 60)
    print()

    generator = BinauralGenerator(sample_rate=44100)

    # Show available presets
    print("Available Presets:")
    print("-" * 40)
    for name, description in generator.list_presets().items():
        print(f"  {name}: {description}")
    print()

    # Generate theta waves for meditation (6 Hz)
    print("Generating Theta Waves (6 Hz) for Meditation...")
    print("-" * 40)
    print("  Base frequency: 200 Hz")
    print("  Beat frequency: 6 Hz (Theta range)")
    print("  Duration: 10 seconds")
    print()

    binaural = generator.generate_binaural_beat(
        base_freq=200,
        beat_freq=6,
        duration=10,
        fade_duration=2,
    )

    print(f"  Generated audio shape: {binaural.shape}")
    print(f"  Left channel: {200} Hz")
    print(f"  Right channel: {200 + 6} Hz")
    print("  Perceived beat: 6 Hz (Theta)")
    print()

    # Generate from preset
    print("Generating from 'relaxation' preset...")
    print("-" * 40)
    relaxation = generator.generate_from_preset("relaxation", duration=10)
    print(f"  Generated {len(relaxation) / 44100:.1f} seconds of Alpha waves")
    print()

    # Generate isochronic tones
    print("Generating Isochronic Tones (10 Hz Alpha)...")
    print("-" * 40)
    print("  Tone frequency: 300 Hz")
    print("  Pulse rate: 10 Hz (Alpha range)")
    print("  Duration: 10 seconds")
    print()

    isochronic = generator.generate_isochronic_tones(
        freq=300,
        pulse_rate=10,
        duration=10,
        duty_cycle=0.5,
    )

    print(f"  Generated audio shape: {isochronic.shape}")
    print()

    # Generate layered binaural
    print("Generating Layered Binaural Beats...")
    print("-" * 40)
    layers = [
        {"base_freq": 150, "beat_freq": 4, "amplitude": 0.5},  # Theta
        {"base_freq": 300, "beat_freq": 10, "amplitude": 0.5},  # Alpha
    ]
    print("  Layer 1: 150 Hz base, 4 Hz beat (Theta)")
    print("  Layer 2: 300 Hz base, 10 Hz beat (Alpha)")
    print()

    layered = generator.generate_layered_binaural(layers, duration=10)
    print(f"  Generated layered audio shape: {layered.shape}")
    print()

    # Save to file
    output_path = "theta_meditation.wav"
    print(f"Saving theta waves to {output_path}...")
    save_audio(binaural, output_path, sample_rate=44100)
    print("  Saved successfully!")
    print()

    # Play audio
    print("Playing theta waves (10 seconds)...")
    print("  Use headphones for binaural effect!")
    print("-" * 40)
    play_audio(binaural, sample_rate=44100, blocking=True)
    print()

    print("=" * 60)
    print("Demo complete!")
    print()
    print("Tips for best results:")
    print("  - Use headphones (required for binaural beats)")
    print("  - Find a quiet, comfortable space")
    print("  - Close your eyes and focus on breathing")
    print("  - Sessions of 15-30 minutes are most effective")
    print("=" * 60)


if __name__ == "__main__":
    main()
