"""Example: Generate AI meditation music with ElevenLabs."""

import os

from dotenv import load_dotenv

from elevenlabs_sdk import MeditationGenerator


def main():
    print("=" * 60)
    print("ElevenLabs SDK - AI Meditation Music Demo")
    print("=" * 60)
    print()

    # Check for API key
    load_dotenv()
    if not os.getenv("ELEVENLABS_API_KEY"):
        print("ELEVENLABS_API_KEY not set!")
        print()
        print("To use this SDK:")
        print("1. Get an API key at: https://elevenlabs.io")
        print("2. Add to .env file: ELEVENLABS_API_KEY=your_key_here")
        print()
        print("Demo will show available features without API calls.")
        print("-" * 40)
        print()

        # Show presets even without API key
        print("Available Meditation Presets:")
        for name, config in MeditationGenerator.PRESETS.items():
            print(f"  {name}: {config['description']}")
        print()
        return

    generator = MeditationGenerator()

    # Show available presets
    print("Available Meditation Presets:")
    print("-" * 40)
    for name, description in generator.list_presets().items():
        print(f"  {name}: {description}")
    print()

    # Generate a short meditation sound
    print("Generating meditation music (30 seconds)...")
    print("-" * 40)
    print("  Prompt: gentle ambient piano with soft rain")
    print()

    audio = generator.generate_meditation_music(
        prompt="gentle ambient piano with soft rain",
        duration_seconds=30,
    )

    output_path = "meditation_music.mp3"
    audio.save(output_path)
    print(f"  Saved to: {output_path}")
    print()

    # Generate nature sounds
    print("Generating nature sound (20 seconds)...")
    print("-" * 40)
    print("  Description: peaceful forest stream")
    print()

    nature = generator.generate_nature_sound(
        description="peaceful forest stream with birds",
        duration_seconds=20,
    )

    nature.save("forest_stream.mp3")
    print()

    # Generate transition sound
    print("Generating transition bell...")
    print("-" * 40)

    bell = generator.generate_transition_sound(
        sound_type="bowl",
        duration_seconds=5,
    )

    bell.save("meditation_bell.mp3")
    print()

    # Generate from preset
    print("Generating from 'morning_meditation' preset...")
    print("-" * 40)

    preset_audio = generator.generate_from_preset(
        preset="morning_meditation",
        duration_seconds=30,
    )

    preset_audio.save("morning_meditation.mp3")
    print()

    print("=" * 60)
    print("Demo complete!")
    print()
    print("Generated files:")
    print("  - meditation_music.mp3")
    print("  - forest_stream.mp3")
    print("  - meditation_bell.mp3")
    print("  - morning_meditation.mp3")
    print()
    print("Try generating longer sessions for actual meditation!")
    print("=" * 60)


if __name__ == "__main__":
    main()
